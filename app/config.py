import os
import re

MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
ACTIVES = ('EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD', 'USDCAD')
GET_ACTIVES_URL = os.environ.get('GET_ACTIVES_URL', 'https://ratesjson.fxcm.com/DataDisplayer')


def clean_mongodb_uri(mongodb_uri):
    """Remove username:password."""
    return re.sub(r'//.+@', '//', mongodb_uri)


class Config:
    MONGODB_URI = os.environ.get('MONGODB_URI', f'mongodb://{MONGODB_HOST}:27017/items')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 8080))
    DEBUG = bool(os.environ.get('DEBUG', False))

    def __str__(self) -> str:
        return f'mongodb_uri={clean_mongodb_uri(self.MONGODB_URI)}, debug={self.DEBUG}'
