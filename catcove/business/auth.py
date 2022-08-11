from sqlalchemy import select
from sqlalchemy.sql import or_
from sanic import Request
from typing import List, Any
from pydantic import BaseModel

from ..db import async_session
from ..models.schemas.request import UserLoginModel
from ..models.tables.users import Users

'''fake_db = [
    {"nickname": "00000", "password": "12345"},
    {"nickname": "ALG", "password": "admin"}
]'''


async def login_authentication_logic(
    request_model: UserLoginModel,
    db_session: async_session) -> Users | None | bool:

    # Simple Read.
    
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
        if user:
            db_session.expunge(user)
        else: return None
    # Commit over.

    if user.check_passwd(request_model.password):
        return user
    else: return False


async def check_invitecode(
    code: str,
    db_session: async_session) -> bool:
    # Query
    async with db_session.begin():
        ...
    
    return ...
