from datetime import timedelta
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from catcove.usecase.auth import AuthService
from catcove.entities.tables import Base

engine = create_async_engine(
    url="sqlite+aiosqlite:///tinycat_test.db",  # Use async.
    encoding="utf-8",
    echo=True,
    future=True
)

sync_engine = create_engine(
    url="sqlite:///tinycat_test.db",  # Use async.
    encoding="utf-8",
    echo=True,
)

db_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=True
)


def async_as_sync(func):
    return asyncio.get_event_loop().run_until_complete(func)


class TestAuthService(object):
    
    ser = AuthService()

    def init_db(self):
        # Initilize
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)

        # Import.
        from catcove.usecase.users import UserService
        usr = UserService(db_session())
        return async_as_sync(usr.create_user("123", "123@321.xyz", "123456"))


    def test_encrypt(self):
        # Initialize.
        user = self.init_db()

        payload = self.ser.gen_payload(user, timedelta(days=7))
        assert isinstance(payload, dict)
        raw = self.ser.dict_to_str()
        assert raw == True

        # Cookie.
        _ = self.ser.encrypt()
        assert _ == True

        # Token.
        ...

        return self.ser.cookie, None
    
    def test_decrypt(self):
        cookie, token = self.test_encrypt()
        self.ser.cookie = cookie
        self.ser.token = token

        # Cookie.
        _ = self.ser.decrypt()
        assert _ == True
        _ = self.ser.str_to_dict()
        assert _ == True
        assert isinstance(self.ser.payload["id"], int)

        # Token.
        ...
    
    def test_cookie_set(self):
        ...
