from .users import UserService
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, update, or_, table

from ..entities.tables.users import Users, Moderator, Spectator

class ManageService(UserService):
    """涉及到管理的业务用这个取代原本的 `UserServies` 即可。"""

    def __init__(
        self,
        db_session: sessionmaker,
        role: str = "",
        status: dict | None = None,
        user: Users | None = None,
    ) -> None:
        super().__init__(db_session, status, user)
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
    
    async def be_spectator(self, password: str) -> Spectator | None:
        if not isinstance(self.user, Users):
            return None
        """ use `Service.get_user` before. """

        # Update role and insert data.

    async def be_moderator(self) -> Moderator | None:
        if not isinstance(self.user, Users):
            return None
        """ use `Service.get_user` before. """
        
        ...
