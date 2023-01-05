import json
import logging

import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
from motor.motor_asyncio import AsyncIOMotorDatabase


from app.db import setup_mongo
from app.models import ensure_indexes
from app.config import Config, ACTIVES
from app.services.rates import subscribe_rates_service
from app.services.active import ActivesService
from app.websocket_handler import WebSocketHandler

logger = logging.getLogger(__name__)


async def fill_db(db: AsyncIOMotorDatabase) -> None:
    # TODO Добавлять элементы массово, а не поэлементно
    # TODO Не трогать элементы, если они уже записаны в бд
    active_service = ActivesService(db)
    items = await active_service.find_items()
    async for item in items:
        await active_service.delete_item(item['id'])
    for index, a in enumerate(ACTIVES):
        await active_service.create_item({'symbol': a})


async def echo(websocket: WebSocketServerProtocol, *args):
    ws_handler = WebSocketHandler(websocket, db)
    async for message in websocket:
        await ws_handler.handle(json.loads(message))


db = setup_mongo(Config)

start_server = websockets.serve(echo, Config.HOST, Config.PORT)
loop = asyncio.get_event_loop()
loop.run_until_complete(ensure_indexes())
loop.run_until_complete(fill_db(db))
tasks = [start_server, loop.create_task(subscribe_rates_service(db))]
wait_tasks = asyncio.wait(tasks)
loop.run_until_complete(wait_tasks)
loop.run_forever()
