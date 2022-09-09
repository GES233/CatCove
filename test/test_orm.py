import pytest
import asyncio
from catcove.entities.tables import Base, Users, UserPosts

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, or_

engine = create_async_engine(
    url="sqlite+aiosqlite:///tinycat_test.db",  # Use async.
    encoding="utf-8",
    echo=True,
    future=True,
)

sync_engine = create_engine(
    url="sqlite:///tinycat_test.db",  # Use async.
    encoding="utf-8",
    echo=True,
)

db_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)


def init_db():
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)


def sync_to_async(func):
    asyncio.get_event_loop().run_until_complete(func)


...
