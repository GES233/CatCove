from sanic import Request
from sanic_jwt.exceptions import AuthenticationFailed
from sqlalchemy.sql import select, or_

from catcove.model.tables import engine_bind, Users
from catcove.model.schemas import UserDB


async def authenticate(request: Request, *args, **kwargs):
    nickname = request.json.get('nickname', None)
    password = request.json.get('password', None)
    if not nickname or not password:
        raise AuthenticationFailed("Missing username or password.")
    session: engine_bind = request.ctx.session
    async with session.begin():
        sql = select(Users).\
            where(
                or_(
                    Users.nickname == nickname,
                    Users.username == nickname,
                    Users.email == nickname
                )
            )
        user_name = await session.execute(sql)
        # Returned a user list or None.
        user: Users = user_name.scalars().first()
        if not user:
            AuthenticationFailed("User not found.")
        session.expunge(user)

        if user.check_passwd(password) is False:
            AuthenticationFailed("Password is incorrect.")

        return UserDB.from_orm(user).dict()


async def store_refresh_token(user_id, refresh_token, *args, **kwargs):
    key = f'refresh_token_{user_id}'
    await ... # aredis.set(key, refresh_token)
