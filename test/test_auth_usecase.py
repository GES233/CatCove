from datetime import timedelta
from types import NoneType
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
    future=True,
)

db_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)


def async_as_sync(func):
    return asyncio.get_event_loop().run_until_complete(func)


async def _init(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


class TestAuthService(object):

    ser = AuthService()

    def init_db(self):
        # Initilize
        async_as_sync(_init(engine))

        # Import.
        from catcove.usecase.users import UserService

        usr = UserService(db_session())
        return async_as_sync(usr.create_user("123", "123@321.xyz", "123456"))

    def test_encrypt(self):
        # Initialize.
        user = self.init_db()

        import os

        os.environ["APP_ENV"] = "dev"
        from catcove.web.app import create_config_app

        app = create_config_app()

        self.pri_key = app.ctx.ecc_pri
        self.pub_key = app.ctx.ecc_pub

        payload = self.ser.gen_payload(user, timedelta(days=7))
        assert isinstance(payload, dict)
        raw = self.ser.dict_to_str()
        assert raw == True

        # Cookie and cookie.
        _ = self.ser.encrypt(self.pri_key)
        assert _ == True

        return self.ser.cookie, self.ser.token

    def test_decrypt(self):
        cookie, self.ser.token = self.test_encrypt()

        # Token.
        _ = self.ser.decrypt(self.pub_key)
        assert _ == True
        _ = self.ser.str_to_dict()
        assert _ == True
        assert isinstance(self.ser.payload["id"], int)

        # Cookie.
        self.ser.cookie = cookie
        self.ser.token = None
        _ = self.ser.decrypt()
        assert _ == True
        _ = self.ser.str_to_dict()
        assert _ == True
        assert isinstance(self.ser.payload["id"], int)

    def test_cookie_set(self):
        """Honestly, put it to `test_page_access.py` is better."""
        # Initialize.
        user = self.init_db()

        _ = self.ser.gen_payload(user, timedelta(days=7))
        _ = self.ser.dict_to_str()
        _ = self.ser.encrypt()

        # Create a Sanic app.
        from sanic import Sanic, text

        app = Sanic("test")

        @app.route("/")
        async def index(request):
            return self.ser.set_cookie(text("Cookie here"))

        app.run(workers=1)

        # Request.
        import requests

        index_req = requests.get("http://127.0.0.1:8000")
        cookie = index_req.cookies["UserMeta"]
        assert isinstance(cookie, NoneType) == False

        app.stop()
