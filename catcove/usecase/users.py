from typing import List, Any
from sqlalchemy.sql import select, update, or_, insert
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession

from . import ServiceBase
from ..entities.tables.users import Users, following_table
from ..entities.schemas.auth import UserTokenPayload


class UserService(ServiceBase):
    """Usecase related to user."""

    def __init__(
        self,
        db_session: sessionmaker,
        status: dict | None = None,
        user: Users | None = None,
        # User with others.
    ) -> None:
        """Usage:
        ```
        a = UserService(
            config=None,
            db_session=request.ctx.session,
            user=Users(id=2)
        )
        a.get_user()
        a.user = Users(id=2, nickname="2", ...)
        ```
        """
        super().__init__(status)
        self.db_session = db_session
        if user:
            self.user: Users = user
        else:
            self.user = None

    async def get_user(self, id: int | None = None) -> Users | None:

        query_id = id if id else self.user.id

        async with self.db_session() as session:
            async with session.begin():
                sql = select(Users).where(Users.id == query_id)
                users = await session.execute(sql)
                user = users.scalars().first()
                session.expunge(user) if user else ...

                # Save userposts, following table etc.

        self.user = user
        return self.user

    async def check_user_token(self, token: dict) -> bool:

        # Check expire firstly.

        async with self.db_session() as session:
            async with session.begin():
                sql = select(Users).where(Users.id == token["id"])
                users = await session.execute(sql)
                user: Users = users.scalars().first()
                if not user:
                    return False
                session.expunge(user)

        if not user:
            return False

        if (
            token["status"] == user.status
            and (
                (user.is_spectator == True and token["role"] == "spectator")
                or (user.is_spectator == False and token["role"] == "normal")
            )
            and (user.nickname == token["nickname"])
        ):
            self.user = user
            return True
        else:
            return False

    def get_user_token(self) -> dict:
        """Get user token from database.

        Usage:
        When update user in database.
        """
        return UserTokenPayload(
            id=self.user.id,
            nickname=self.user.nickname,
            status=self.user.status,
            role=self.user.role,
        ).dict()

    async def check_common_user(self, nickname: str, email: str) -> bool:

        async with self.db_session() as session:
            async with session.begin():
                sql = select(Users).where(
                    or_(
                        Users.nickname == nickname,
                        Users.email == nickname,
                        Users.email == email,
                    )
                )
                users = await session.execute(sql)
                user: Users | None = users.scalars().first()
                session.expunge(user) if user else ...

        if user:
            self.user = user
            return True
        else:
            return False

    async def create_user(self, nickname: str, email: str, password: str) -> Users:

        async with self.db_session() as session:
            async with session.begin():
                newbie = Users(
                    nickname=nickname,
                    email=email,
                )
                newbie.encrypt_passwd(password)
                session.add(newbie)
                await session.flush()
                session.expunge(newbie)

        self.user = newbie
        return self.user

    async def change_user_status(self, status: str) -> bool:
        async with self.db_session() as session:
            async with session.begin():
                """
                sql = update(Users).\
                    where(Users.id == self.user.id).\
                    values(status=status)
                await session.execute(sql)
                """
                result = await session.execute(
                    select(Users).where(Users.id == self.user.id)
                )
                now_user: Users = result.scalars().first()

                # Return None if not existed.
                if not now_user:
                    return False
                now_user.status = status

                # Update.
                await session.flush()
                session.expunge(now_user)

        self.user = now_user
        return True

    async def change_user_profile(self, **profile) -> bool:
        """Change user's profile.

        There're 2 ways to implementate this:

        - update as a `Users` model
        - update to the database

        I choose the second one.
        """
        # No person exist.
        if not isinstance(self.user, Users) or not self.user.id:
            return False

        data = {k: v for k, v in profile.items() if v is not None}

        async with self.db_session() as session:
            async with session.begin():
                stmt = update(Users).where(Users.id == self.user.id).values(data)
                await session.execute(stmt)

        return True

    async def update_password(self, password: str) -> bool:
        """Update user's password."""

        # No person in instance.
        if not (isinstance(self.user, Users) and self.user.id):
            return False

        async with self.db_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Users).where(Users.id == self.user.id)
                )
                user = result.scalars().first()

                # Not in database.
                if not user:
                    await session.close()
                    return False
                else:
                    user.encrypt_passwd(password)
                    await session.flush()
                    # Update password to `self.user`
                    session.expunge(user)

        self.user = user
        return True

    def get_user_post_permission(self) -> bool:
        """Permission for all websites, every request which
        its method is `POST`.
        """
        return (
            False
            if self.user.status == "freeze"
            or self.user.status == "blocked"
            or self.user.status == "delete"
            else True
        )

    async def get_following(
        self, following: bool, offset: int, limit: int
    ) -> List[Any]:
        """Return User's following or fans list."""
        if offset <= 0 and limit <= 0:
            return []

        async with self.db_session() as session:
            async with session.begin():
                if following == True:
                    # return following => user AS A follower role
                    stmt = (
                        select(Users)
                        .where(following_table.c.follower_id == Users.id)
                        .limit(limit)
                        .offset(offset)
                    )
                else:
                    # return followed => user followed BY => user AS followed role
                    stmt = (
                        select(Users)
                        .where(following_table.c.followed_id == Users.id)
                        .limit(limit)
                        .offset(offset)
                    )
                result = await session.execute(stmt)
                if not result:
                    following_list = []
                else:
                    following_list = result.scalar().all()
                    session.expunge(following_list)

        return following_list

    async def follow_user(self, following_id) -> bool:
        ...

    async def unfollow_user(self, following_id) -> bool:
        ...

    async def disfollow_user(self, follower_id) -> bool:
        """AKA remove fans(this opration always exists in block)."""
        ...
