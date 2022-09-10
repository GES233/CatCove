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


class TestUserService:
    """Test user service without authentation and others."""

    ser = UserService(db_session())
    m_ser = ManageService(db_session())

    def test_create_user(self):
        # Initialize first.
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)

        # Check an un-exitsted user.
        common_user = async_as_sync(
            self.ser.check_common_user(nickname="12345", email="12345@zz.top")
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
            self.ser.check_common_user(nickname="None", email="12345@zz.top")
        )
        assert hasattr(self.ser.user, "id")
    
    def test_user_role(self):
        # Initialize first.
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)
        _ = async_as_sync(
            self.ser.create_user("12345", "12345@zz.top", "123456")
        )
        # Add a role.
        _ = async_as_sync(
            self.ser.get_role()
        )

    def test_check_user(self):
        # Initialize first.
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)

        # Create user.
        _ = async_as_sync(self.ser.create_user("12345", "12345@zz.top", "123456"))

        common_user = async_as_sync(
            self.ser.check_common_user(nickname="12345", email="12345@zz.top")
        )
        if common_user == False:
            assert False

        # Check password.
        login_accept = self.ser.user.check_passwd("123456")
        login_reject = self.ser.user.check_passwd("12345")

        # Update password.
        _ = async_as_sync(self.ser.update_password("12345"))

        # Re-check.
        login_reaccpect = self.ser.user.check_passwd("12345")
        assert login_accept == True
        assert login_reject == False
        assert login_reaccpect == True

    def test_update_user(self):
        # Initialize first.
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)

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
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)

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
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)

        # Create user.
        _ = async_as_sync(self.ser.create_user("12345", "12345@zz.top", "123456"))
        _ = async_as_sync(self.ser.create_user("2345", "1245@zz.top", "123456"))
        _ = async_as_sync(self.ser.create_user("345", "145@zz.jmp", "123456"))

        # ...
        ...
