from datetime import datetime

from umongo import Document, fields

from .db import instance


# Модель активов
@instance.register
class Active(Document):
    symbol = fields.StringField(required=True, unique=True)


# Модель точек
@instance.register
class Point(Document):
    active = fields.ReferenceField('Active', required=True)
    value = fields.FloatField(required=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)

    class Meta:
        indexes = ['-created_at']


async def ensure_indexes() -> None:
    await Active.ensure_indexes()
    await Point.ensure_indexes()
