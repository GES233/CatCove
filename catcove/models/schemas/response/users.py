from enum import Enum
from datetime import datetime, date
from typing import List
from pydantic import BaseModel


class Status(Enum):
    normal = "normal",
    blocked = "blocked",
    freeze = "freeze",
    newbie = "newbie",
    deleted = "deleted"


class Gender(Enum):
    male = "M"
    female = "f"
    other = "O"


class UserInfoAbstrct(BaseModel):
    id: int
    nickname: str
    status: Status


class UserInfo(UserInfoAbstrct):
    join_time: datetime
    gender: Gender
    birth: date | None
    info: List[str] | str | None
    is_spectator: bool
