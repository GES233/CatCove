from sqlalchemy import select
from sqlalchemy.sql import or_
from sanic import Request
from typing import List, Any
from pydantic import BaseModel

from ..db import async_session
from ..models.schemas.request import UserLoginModel

'''fake_db = [
    {"nickname": "00000", "password": "12345"},
    {"nickname": "ALG", "password": "admin"}
]'''


async def login_authentication_logic(
    request_model: UserLoginModel,
    db_session: async_session) -> bool:

    # Simple Read.
    
    from ..models.tables.users import Users
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
        db_session.expunge(user) if user else None
    # Commit over.
    
    # user = fake_db[request_model.nickname]
    if not user: return False  # 查无此人

    if user.check_passwd(request_model.password):
    # if user["password"] == request_model.password:
        return True
    else: return False
