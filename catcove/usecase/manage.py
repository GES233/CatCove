from . import ServiceBase

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, update

from ..entities.tables.users import (
    Users,
    Moderator,
    Spectator,
)


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
        async with self.db_session() as session:
            # async with session.begin():
            stmt_for_spectator = select(Spectator).where(
                Spectator.user_id == self.user.id
            )
            stmt_for_moderator = select(Moderator).where(
                Moderator.user_id == self.user.id
            )
            _as_spectator = await session.execute(stmt_for_spectator)
            _as_spectator = _as_spectator.scalars().first()
            session.expunge(_as_spectator) if _as_spectator else ...
            _as_moderator = await session.execute(stmt_for_moderator)
            _as_moderator = _as_moderator.scalars().first()
            session.expunge(_as_moderator) if _as_spectator else ...

        self.user_as_spectator = _as_spectator
        self.user_as_moderator = _as_moderator

        return True

    async def be_spectator(self, password: str) -> Spectator | None:
        if not isinstance(self.user, Users):
            return None
        """ use `Service.get_user` before. """

        # Update role.
        async with self.db_session() as session:
            async with session.begin():
                spactator = Spectator(
                    user_id=self.user.id,
                )
                spactator.encrypt_passwd(password)

                stmt = (
                    update(Users)
                    .where(Users.id == self.user.id)
                    .values({"role": "spactator"})
                )

                session.add(spactator)
                await session.execute(stmt)
                await session.flush()
                session.expunge(spactator)

        return spactator

    async def be_moderator(self) -> Moderator | None:
        if not isinstance(self.user, Users):
            return None
        """ use `Service.get_user` before. """

        ...
