from datetime import datetime
from typing import List
from pydantic import BaseModel

from .users import UserInfoAbstrct

class Anouncement(BaseModel):
    title: str
    author: str | UserInfoAbstrct
    timestamp: datetime
    content: List[str] | str | None