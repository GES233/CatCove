from pydantic import BaseModel
from typing import List

from . import paragraph
from .. import APIResponceDetail


class Anouncement(BaseModel):
    title: str | None
    author: str | List[str] | None
    to: str | List[str] | None
    content: paragraph | List[paragraph]


class AnouncementBody(APIResponceDetail):
    abstract = "Notice"
    body: Anouncement
