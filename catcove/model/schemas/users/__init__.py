from pydantic import BaseModel, validator
from enum import Enum
from datetime import date, datetime


class Status(Enum):
    """ User status.
        
        only this.
    """
    normal:  str = "normal"
    blocked: str = "blocked"
    freeze:  str = "freeze"
    newbie:  str = "newbie"
    deleted: str = "deleted"


class Gender(Enum):
    """ User's gender.
        
        If you think you are a lesbian who have d*ck, you are.
    """
    male:   str = "M"
    female: str = "F"
    other:  str = "O"


class UserEditableInfo(BaseModel):
    nickname: str
    gender: Gender | None = Gender.other
    info: str | None = None


class UserInfo(UserEditableInfo):
    id: int
    status: Status
    jion_time: datetime
    username: str | None = None


class UserDB(BaseModel):
    id: int
    status: Status
    jion_time: datetime
    nickname: str
    email: str
    password: str
    username: str | None = None
    gender: Gender | None = Gender.other
    birth: date | None = None
    info: str | None = None
    is_spectator: bool

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    username: int | str
    password: str
    


class UserCreateInfo(BaseModel):
    nickname: str
    email: str
    password: str
    confirm_password: str

    @validator("confirm_password")
    def passwd_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("You give me 2 differente passwords, idk which one is yours.")
