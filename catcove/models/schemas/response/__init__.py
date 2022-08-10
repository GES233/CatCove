from typing import Any
from pydantic import BaseModel


class OriginData(BaseModel):
    content_type: str
    detail: BaseModel | str | Any


class APIResp(BaseModel):
    code: int
    info: str
    org: OriginData | str | Any
