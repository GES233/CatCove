from typing import Any
from pydantic import BaseModel
# Add cunstom error.


class OriginContentModel(BaseModel):
    content_type: str
    data: Any

class BaseAPI(BaseModel):
    code: int
    info: str
    org: OriginContentModel
