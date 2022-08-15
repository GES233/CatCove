from pydantic import BaseModel


class UserTokenPayload(BaseModel):
    id: int
    nickname: str
    status: str
    role: str
