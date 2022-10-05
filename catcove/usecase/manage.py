from typing import Tuple
from . import ServiceBase

from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, update

from ..entities.tables.users import (
    Users,
    Mediator,
    Spectator,
)


class ManageService(ServiceBase):
    def __init__(
        self,
        db_session: AsyncSession,
        user: Users,
        role: str = "",
    ) -> None:
        self.db_session = db_session
        self.user = user
        self.user_as_spectator: Spectator | None = None
        self.user_as_mediator: Mediator | None = None
        self.role = role

    async def get_role(self) -> bool:
        if not isinstance(self.user, Users):
            return False
        async with self.db_session as conn:
            # async with session.begin():
            stmt_for_spectator = select(Spectator).where(
                Spectator.user_id == self.user.id
            )
            stmt_for_mediator = select(Mediator).where(
                Mediator.user_id == self.user.id
            )
            _as_spectator = await conn.execute(stmt_for_spectator)
            _as_spectator = _as_spectator.scalars().first()
            conn.expunge(_as_spectator) if _as_spectator else ...
            _as_mediator = await conn.execute(stmt_for_mediator)
            _as_mediator = _as_mediator.scalars().first()
            conn.expunge(_as_mediator) if _as_spectator else ...

        self.user_as_spectator = _as_spectator
        self.user_as_mediator = _as_mediator

        return True

    async def be_spectator(self, password: str) -> Spectator | None:
        if not isinstance(self.user, Users):
            return None
        """ use `Service.get_user` before. """

        async with self.db_session as conn:
            async with conn.begin():
                spactator = Spectator(
                    user_id=self.user.id,
                )
                spactator.encrypt_passwd(password)

                stmt = (
                    update(Users)
                    .where(Users.id == self.user.id)
                    .values({"role": "spactator"})
                )

                conn.add(spactator)
                await conn.execute(stmt)
                await conn.flush()
                conn.expunge(spactator)

        return spactator

    async def be_mediator(self) -> Mediator | None:
        if not isinstance(self.user, Users):
            return None
        """ use `Service.get_user` before. """

        async with self.db_session as conn:
            async with conn.begin():
                stmt_query = select(Users.role).where(Users.id == self.user.id)
                stmt_update = (
                    update(Users)
                    .where(Users.id == self.user.id)
                    .values({"role": "mediator"})
                )

                mediator = Mediator(
                    user_id=self.user.id,
                )

                _query_result = await conn.execute(stmt_query)
                role = _query_result.scalars().first() if _query_result else None
                if role != "spactator":
                    await conn.execute(stmt_update)
                if role:
                    conn.add(mediator)
                    await conn.flush()
                    conn.expunge(mediator)
                else:
                    mediator = None

        return mediator

    async def _check_role_in_session(self, session) -> Tuple:
        stmt_for_spectator = select(Spectator).where(Spectator.user_id == self.user.id)
        stmt_for_mediator = select(Mediator).where(Mediator.user_id == self.user.id)
        _as_spectator = await session.execute(stmt_for_spectator)
        _as_spectator = _as_spectator.scalars().first()
        _as_mediator = await session.execute(stmt_for_mediator)
        _as_mediator = _as_mediator.scalars().first()
        return _as_spectator, _as_mediator

    async def delist_spectator(self) -> bool:
        if not isinstance(self.user, Users):
            return None

        async with self.db_session as conn:
            async with conn.begin():
                spectator, mediator = self._check_role_in_session(self.db_session)

                if mediator:
                    # Move role to `mediator`.
                    ...
                else:
                    # Move role to `user`.
                    ...

                # Remove spectator.
                ...

    async def delist_mediator(self) -> bool:
        if not isinstance(self.user, Users):
            return None

        async with self.db_session as conn:
            async with conn.begin():
                spectator, mediator = self._check_role_in_session(self.db_session)

                if not spectator:
                    # Move role to `user`.
                    ...

                # Remove spectator.
                ...
