import datetime
import re

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, TIMESTAMP


@as_declarative()
class Base:
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow(),
                        onupdate=datetime.datetime.utcnow())
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
