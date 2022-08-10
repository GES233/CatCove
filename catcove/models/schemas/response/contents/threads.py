from datetime import datetime
from typing import Any, List
from pydantic import BaseModel

from .. import OriginData
from ..users import UserInfoAbstrct
from .posts import PostInThreadModel

class ThreadHeadModel(BaseModel):
    id: int
    title: str
    po: UserInfoAbstrct  # UserModelAbstract
    timestamp: datetime
    tag: List[Any]  # TagModelABstract
    statistics: ...  # ThreadStatistics

class Thread(OriginData):
    index_head: int | None
    thread_info: ThreadHeadModel | None
    # thread_info != None if not index_head 

    thread_body: List[PostInThreadModel]
