from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tools import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database() -> Generator:
    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()
