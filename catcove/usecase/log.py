from sqlalchemy.sql import select, or_, update
from sqlalchemy.orm import sessionmaker

from ..entities.tables.users import Users
from ..entities.tables.log.common_log import Logs


async def add_op(session: sessionmaker, user: Users, **settings):
    async with session.begin():
        new_op = Logs(
            settings
        )
        new_op.target_user = user
        session.add(new_op)
        await session.flush()


async def app_singal_add_user(session: sessionmaker, user: Users):
    # Using at `/signup`
    await add_op(
        session,
        user,
        operator_id = None,  # None means system.
        operation_method = "CA",  # Some problem here, I need to learn sth.
        target_type = "users",
        terget_id = user.id
    )


async def app_signal_login(session: sessionmaker, user: Users):
    await add_op(
        session,
        user,
        operator_id = user.id,
        operation_method = "AO",
        target_type = "users",
        terget_id = user.id,
    )
