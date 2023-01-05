import asyncio
import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from umongo.frameworks import MotorAsyncIOInstance


logger = logging.getLogger(__name__)
instance = MotorAsyncIOInstance()


def init_mongo(mongodb_uri: str) -> AsyncIOMotorDatabase:
    logger.info(f'init mongo')
    loop = asyncio.get_event_loop()
    conn = AsyncIOMotorClient(mongodb_uri, io_loop=loop)
    return conn.get_database()


def setup_mongo(config) -> AsyncIOMotorDatabase:
    db = init_mongo(config.MONGODB_URI)
    instance.set_db(db)

    return db

