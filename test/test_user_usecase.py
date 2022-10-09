from datetime import date
from time import sleep
from types import NoneType
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, or_

from catcove.usecase.users import UserService
from catcove.usecase.manage import ManageService
from catcove.entities.tables import Base

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


def async_as_sync(func):
    # use `async_as_sync(func())`.
    return asyncio.get_event_loop().run_until_complete(func)


async def _init(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


class TestUserService:
    """Test user service without authentation and others."""

    ser = UserService(db_session())

    def test_create_user(self):
        # Initialize first.
        async_as_sync(_init(engine))

        # Check an un-exitsted user.
        common_user = async_as_sync(
            self.ser.query_common_user(nickname="12345", email="12345@zz.top")
        )

        if common_user == False:
            # Add user.
            user = async_as_sync(
                self.ser.create_user("12345", "12345@zz.top", "123456")
            )
            assert hasattr(user, "id")
        else:
            assert False

        # Requery.
        common_user = async_as_sync(
            self.ser.query_common_user(nickname="None", email="12345@zz.top")
        )
        assert hasattr(self.ser.user, "id")

    def test_user_role(self):
        # Initialize first.
        async_as_sync(_init(engine))

        _ = async_as_sync(self.ser.create_user("12345", "12345@zz.top", "123456"))
        # Add a role.
        _ = async_as_sync(self.ser.change_user_profile(role="spectator"))

    def test_check_user(self):
        # Initialize first.
        async_as_sync(_init(engine))

        # Create user.
        _ = async_as_sync(self.ser.create_user("12345", "12345@zz.top", "123456"))

        common_user = async_as_sync(
            self.ser.query_common_user(nickname="12345", email="12345@zz.top")
        )
        if common_user == False:
            assert False

        # Check password.
        login_accept = self.ser.user.check_passwd("123456")
        login_reject = self.ser.user.check_passwd("12345")

        # Update password.
        _ = async_as_sync(self.ser.change_password("12345"))

        # Re-check.
        login_reaccpect = self.ser.user.check_passwd("12345")
        assert login_accept == True
        assert login_reject == False
        assert login_reaccpect == True

    def test_update_user(self):
        # Initialize first.
        async_as_sync(_init(engine))

        # Create user.
        _ = async_as_sync(self.ser.create_user("12345", "12345@zz.top", "123456"))

        # Change user status.
        # Running when user queried before.
        result = async_as_sync(self.ser.change_user_status("normal"))
        # Error corrected.

        if result == True:
            # Requery.
            _ = async_as_sync(self.ser.get_user(id=self.ser.user.id))
            assert _.status == "normal"
        else:
            assert False

    def test_modify_info(self):
        # Initialize first.
        async_as_sync(_init(engine))

        # Create user.
        _ = async_as_sync(self.ser.create_user("12345", "12345@zz.top", "123456"))

        # Modify info.
        gender_update = async_as_sync(self.ser.change_user_profile(gender="M"))
        birth_update = async_as_sync(
            self.ser.change_user_profile(birth=date(year=1989, month=6, day=4))
        )
        info_update = async_as_sync(
            self.ser.change_user_profile(
                info="My name's Q, and I love fish.", username="Q"
            )  # Multiple.
        )
        assert gender_update == True
        assert birth_update == True
        assert info_update == True

    def test_follow(self):
        # Initialize first.
        async_as_sync(_init(engine))

        # Create user.
        _ = async_as_sync(self.ser.create_user("12345", "12345@zz.top", "123456"))
        _ = async_as_sync(self.ser.create_user("2345", "1245@zz.top", "123456"))
        _ = async_as_sync(self.ser.create_user("345", "145@zz.jmp", "123456"))

        # ...
        ...

    def get_user(self):
        async_as_sync(_init(engine))

        return async_as_sync(self.ser.create_user("12345", "12345@zz.top", "123456"))

    def test_be_a_spectator(self):
        # Load user.
        user = self.get_user()
        m_ser = ManageService(db_session(), user)

        async_as_sync(m_ser.be_spectator("1234"))

        user_in_db = async_as_sync(self.ser.get_user(1))
        assert user_in_db.role == "spactator"

    def test_be_a_mediator(self):
        # Load user.
        user = self.get_user()
        m_ser1 = ManageService(db_session(), user)

        async_as_sync(m_ser1.be_mediator())

        user_in_db = async_as_sync(self.ser.get_user(1))
        assert user_in_db.role == "mediator"

        # spectator & mediator.
        user2 = async_as_sync(self.ser.create_user("123456", "123456@zz.top", "123456"))

        m_ser2 = ManageService(db_session(), user2)

        async_as_sync(m_ser2.be_spectator("1234"))
        async_as_sync(m_ser2.be_mediator())

        user_in_db = async_as_sync(self.ser.get_user(2))
        assert user_in_db.role == "spactator"
