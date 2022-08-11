from sqlalchemy import select
from sqlalchemy.sql import or_
from sanic import Request
from typing import List, Any
from pydantic import BaseModel

from ...db import async_session
from ...models.schemas.request import SignUpModel

async def common_user_query(
    request_model: SignUpModel,
    db_session: async_session) -> bool:

    from ...models.tables.users import Users
    async with db_session.begin():
        sql = select(Users).where(
            or_(
                Users.nickname == request_model.nickname,
                Users.email == request_model.nickname,
                Users.id == request_model.nickname
            )
        )
        users = await db_session.execute(sql)
        user: Users | None = users.scalars().first()
        if user: return False
    
    return True


async def insert_user(
    request_model: SignUpModel,
    db_session: async_session) -> Any:

    from ...models.tables.users import Users
    async with db_session.begin():
        newbie = Users(
            nickname=request_model.nickname,
            # status="newbie",
            email=request_model.email,
        )
        db_session.add(newbie)
        await db_session.flush()
        db_session.expunge(newbie)
        return newbie
