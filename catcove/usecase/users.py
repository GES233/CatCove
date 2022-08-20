from sqlalchemy.sql import select, update, or_
from sqlalchemy.orm import sessionmaker

from . import ServiceBase
from ..entities.tables.users import Users
from ..entities.schemas.auth import UserTokenPayload


class UserService(ServiceBase):
    """ Usecase related to user. """
    def __init__(
        self,
        db_session: sessionmaker,
        status: dict | None = None,
        user: Users | None = None,
        # User with others.
    ) -> None:
        """ Usage:
            a = UserService(
                config=None,
                db_session=request.ctx.session,
                user=Users(id=2)
            )
            a.get_user()
            a.user = Users(id=2, nickname="2", ...)
        """
        super().__init__(status)
        self.db_session = db_session
        if user:
            self.user: Users = user
        else: self.user = None

    async def get_user(self, id: int | None = None) -> Users | None:

        query_id = id if id else self.user.id

        async with self.db_session.begin():
            sql = select(Users).where(
                Users.id == query_id
            )
            users = await self.db_session.execute(sql)
            user = users.scalars().first()
            self.db_session.expunge(user) if user else ...
        
        self.user = user
        return self.user

    async def check_user_token(self, token: dict) -> bool:
       
       # Check expire firstly.

        async with self.db_session.begin():
            sql = select(Users).where(Users.id==token["id"])
            users = await self.db_session.execute(sql)
            user: Users = users.scalars().first()
            self.db_session.expunge(user)
        
        if not user:
            self.service_status["errors"].append("User Not Exist")
            return False

        if token["status"] == user.status and \
            ((user.is_spectator == True and token["role"] == "spectator") or \
                (user.is_spectator == False and token["role"] == "normal")) and \
                (user.nickname == token["nickname"]):
            return True
        else:
            self.service_status["errors"].append("User Info Error")
            return False
    
    def get_user_token(self) -> dict:
        """ Get user token from database.
            
            Usage:
            When update user in database.
        """
        return UserTokenPayload(
            id = self.user.id, nickname = self.user.nickname,
            status = self.user.status, role = "spectator" if \
                self.user.is_spectator == True else "normal"
        ).dict()

    async def check_common_user(self, nickname, email) -> bool:

        async with self.db_session.begin():
            sql = select(Users).where(
                or_(
                    Users.nickname == nickname,
                    Users.email == nickname,
                    Users.email == email
                )
            )
            users = await self.db_session.execute(sql)
            user: Users | None = users.scalars().first()
            self.db_session.expunge(user) if user else ...
        if user:
            self.user = user
            return True
        else:
            # self.service_status["errors"].append("User Not Exist")
            return False

    async def create_user(self, nickname, email, password) -> Users:

        async with self.db_session.begin():
            newbie = Users(
                nickname=nickname,
                email=email,
            )
            newbie.encrypt_passwd(password)
            self.db_session.add(newbie)
            await self.db_session.flush()
            self.db_session.expunge(newbie)
        
        self.user = newbie
        return self.user
    
    async def change_user_status(self, status) -> bool:
        async with self.db_session.begin():
            '''
            sql = update(Users).\
                where(Users.id == self.user.id).\
                values(status=status)
            await self.db_session.execute(sql)
            '''
            result = await self.db_session.execute(select(Users).where(id=self.user.id))
            now_user: Users = result.scalars().first()

            # Return None if not existed.
            if not now_user:
                # self.service_status["errors"].append("User Not Exist")
                return False
            now_user.status = status

            # Update.
            # ?
            await self.db_session.flush()
            self.db_session.expunge(now_user)

        self.user = now_user
        return True
    
    async def change_user_profile(self, **profile) -> bool:
        """ Change user's profile.

            There're 2 ways to implementate this:
            
            - update as a `Users` model
            - update to the database

            I choose the second one.
        """
        # No person exist.
        if not isinstance(self.user) or not self.user.id:
            # self.service_status["errors"].append("User Not Load or Exist")
            return False

        data = {k: v for k, v in profile.items() if v is not None}
        async with self.db_session.begin():
            sql = update(Users).where(Users.id==self.user.id).\
                values(data)
            await self.db_session.execute(sql)
        
        return True
    
    async def update_password(self, password) -> bool:
        """ Update user's password. """
        # No person in instance.
        if not isinstance(self.user) or not self.user.id:
            # self.service_status["errors"].append("User Not Load or Exist")
            return False
        async with self.db_session.begin():
            result = await self.db_session.\
                execute(select(Users).where(id=self.user.id))
            user = result.scalars().first()

            # Not in database.
            if not user:
                # self.service_status["errors"].append("User Not Exist")
                await self.db_session.close()
                return False
            else:
                user.encrypt_passwd(password)
                await self.db_session.flush()

        return True
    
    def get_user_post_permission(self) -> bool:
        """ Permission for all websites, every request which 
            its method is `POST`.
        """
        return False if self.user.status == "freeze" \
            or self.user.status == "blocked"  \
            or self.user.status == "delete" else True

