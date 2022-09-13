from . import ServiceBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, update, or_, table, values
from bcrypt import gensalt, hashpw

from ..entities.tables.users import Users, Moderator, Spectator


class ManageService(ServiceBase):
    def __init__(
        self,
        db_session: sessionmaker,
        user: Users,
        role: str = "",
        status: dict | None = None,
    ) -> None:
        super().__init__(status)
        self.db_session = db_session
        self.user = user
        self.user_as_spectator: Spectator | None = None
        self.user_as_moderator: Moderator | None = None
        self.role = role

    async def get_role(self) -> bool:
        if not isinstance(self.user, Users):
            return False
        async with self.db_session.begin():
            smpt_for_spectator = select(Spectator).where(
                Spectator.user_id == self.user.id
            )
            smpt_for_moderator = select(Moderator).where(
                Moderator.user_id == self.user.id
            )
            _as_spectator = await self.db_session.execute(smpt_for_spectator)
            # AttributeError: 'coroutine' object has no attribute 'scalars'
            _as_spectator = _as_spectator.scalars().first()
            self.db_session.expunge(_as_spectator) if _as_spectator else ...
            _as_moderator = await self.db_session.execute(smpt_for_moderator)
            _as_moderator = _as_moderator.scalars().first()
            self.db_session.expunge(_as_moderator) if _as_spectator else ...

        self.user_as_spectator = _as_spectator
        self.user_as_moderator = _as_moderator

        return True

    async def be_spectator(self, password_: str) -> Spectator | None:
        if not isinstance(self.user, Users):
            return None
        """ use `Service.get_user` before. """

        # Update role.
        async with self.db_session.begin():
            smpt = (
                update(Users)
                .where(Users.id == self.user.id)
                .values({"role": "spactator"})
            )
            spactator = Spectator(user_id=self.user.id)
            self.db_session.add(spactator)
            await self.db_session.flush()
            await self.db_session.execute(smpt)

        # Insert data.
        async with self.db_session.begin():
            result = await self.db_session.execute(
                select(Spectator).where(Spectator.user_id == self.user.id)
            )
            spactator = result.scalars().first()
            spactator.encrypt_passwd(password_)
            await self.db_session.flush()
            self.db_session.expunge(spactator)

    async def be_moderator(self) -> Moderator | None:
        if not isinstance(self.user, Users):
            return None
        """ use `Service.get_user` before. """

        ...
