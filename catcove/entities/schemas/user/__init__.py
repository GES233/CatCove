from pydantic import BaseModel


class UserAbstract(BaseModel):
    id: int
    nickname: str
    status: str
    # ...
