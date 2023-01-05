from typing import AsyncIterable, Dict

from motor.motor_asyncio import AsyncIOMotorDatabase
from umongo.fields import ObjectId


class BaseService:
    DocumentModel = None

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def find_items(self, filter: Dict = None) -> AsyncIterable[DocumentModel]:
        return self.DocumentModel.find(filter or {})

    async def find_items_limit(self, filter:Dict = None, limit: int = 10) -> AsyncIterable[DocumentModel]:
        return self.DocumentModel.find(filter or {}).limit(limit)

    async def create_item(self, data: Dict) -> DocumentModel:
        item = self.DocumentModel(**data)
        await item.commit()
        return item

    async def find_item(self, item_id: ObjectId) -> DocumentModel:
        item = await self.DocumentModel.find_one({'_id': item_id})

        return item

    async def find_item_by(self, filter: Dict) -> DocumentModel:
        item = await self.DocumentModel.find_one(filter)

        return item

    async def update_item(self, item_id: ObjectId, data: Dict) -> DocumentModel:
        item = await self.find_item(item_id)

        item.update(data)
        await item.commit()

        return item

    async def delete_item(self, item_id: ObjectId) -> None:
        item = await self.find_item(item_id)
        await item.delete()
