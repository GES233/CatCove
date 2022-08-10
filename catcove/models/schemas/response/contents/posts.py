from datetime import datetime
from typing import Any
from pydantic import BaseModel

from ..users import UserInfoAbstrct


class PostModel(BaseModel):
    id: int
    owner: UserInfoAbstrct
    timestamp: datetime
    content: ...
    statistics: ...


class PostInThreadModel(PostModel):
    index: int