import requests
import json
from typing import Iterator

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import GET_ACTIVES_URL, ACTIVES
from app.utils.periodic import Periodic
from .active import ActivesService
from .point import PointService


class RatesService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.active_service = ActivesService(db)
        self.point_service = PointService(db)

    async def _init(self):
        items = await self.active_service.find_items()
        self.actives = {}
        async for item in items:
            self.actives[item.symbol] = item.id

    async def get_actives_from_main_source(self) -> list:
        # Ответ приходит не в формате json
        #  пример: 'null({"Rates":[]})'
        #  поэтому добавлена сооветсвующая обработка: response.text[5:-3]
        #  В реалиях разработки я бы задала вопрос не ошибка ли это
        response = requests.get(GET_ACTIVES_URL)
        return json.loads(response.text[5:-3])

    def count_value(self, bid, ask) -> float:
        # значение котировки
        return (bid + ask)/2

    def _filter_content(self, content: dict) -> Iterator:
        return filter(lambda item: item['Symbol'] in ACTIVES, content['Rates'])

    async def write_rates_to_db(self, content) -> None:
        # TODO добавить массовую вставку элементов
        for item in self._filter_content(content):
            value = self.count_value(item['Bid'], item['Ask'])
            await self.point_service.create_item({'active': self.actives[item['Symbol']], 'value': value})

    async def run(self) -> None:
        content = await self.get_actives_from_main_source()
        await self.write_rates_to_db(content)
        
    async def subscribe(self) -> None:
        await self._init()
        p = Periodic(self.run, 1)
        await p.start()


async def subscribe_rates_service(db: AsyncIOMotorDatabase) -> None:
    rates_service = RatesService(db)
    await rates_service.subscribe()
