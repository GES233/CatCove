from datetime import datetime, date
from pydantic import BaseModel


class UserAbstract(BaseModel):
    id: int
    nickname: str
    status: str


class UserProfile(UserAbstract):
    role: str
    username: str | None
    avatar_id: str | None
    join_time: datetime
    # Optional info.
    gender: str | None
    birth: date | None
    info: str | None
