import json
from datetime import datetime, timedelta
from typing import Dict

from umongo.fields import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from websockets.legacy.server import WebSocketServerProtocol

from app.services.active import ActivesService
from app.services.point import PointService
from app.utils.periodic import Periodic


class WebSocketHandler:
    def __init__(self, websocket: WebSocketServerProtocol, db: AsyncIOMotorDatabase):
        self.websocket = websocket
        self.active_service = ActivesService(db)
        self.point_service = PointService(db)

    async def send_message(self, message: Dict) -> None:
        await self.websocket.send(json.dumps(message))

    async def _assets_action(self, message: Dict) -> None:
        # TODO добавить сериализатор для преобразования ответа
        actives = await self.active_service.find_items()
        message['message']['assets'] = [
            {
                'name': item['symbol'], 'id': str(item['id'])
            }
            async for item in actives
        ]
        await self.send_message(message)

    async def subscribe(self, id: ObjectId) -> None:
        async def run():
            await self.__subscribe(id)

        p = Periodic(run, 1)
        await p.start()

    async def __subscribe(self, id: ObjectId) -> None:
        # TODO 1. добавить сериализатор для преобразования ответа
        #  2. запросом получать сразу информацию по активу вместе с точкой
        item = await self.point_service.find_item_by({"active": id})
        active = await item.active.fetch()
        message = {
            "message": {
                "assetName": active.symbol, "time": datetime.timestamp(item.created_at), "assetId": str(id),
                "value": item.value
            },
            "action": "point"
        }
        await self.send_message(message)

    async def _subscribe_action(self, message: Dict) -> None:
        # TODO 1. добавить сериализатор для преобразования ответа
        #  2. запросом получать сразу информацию по активу вместе с точкой
        id = message['message']['assetId']
        object_id = ObjectId(id)
        created_at = datetime.utcnow() - timedelta(minutes=30)
        items = await self.point_service.find_items({
            "active": ObjectId(id),
            "created_at": {"$gte": created_at}
        })
        points = []
        async for item in items:
            active = await item.active.fetch()
            points.append({
                "assetName": active.symbol, "time": datetime.timestamp(item.created_at), "assetId": id,
                "value": item.value
            })
        message = {
            "message": {"points": points},
            "action": "asset_history"
        }
        await self.send_message(message)
        await self.subscribe(object_id)

    async def handle(self, message: Dict) -> None:
        action = message['action']
        if action == 'assets':
            await self._assets_action(message)
        if action == 'subscribe':
            await self._subscribe_action(message)
