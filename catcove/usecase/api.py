from typing import Any
from pydantic import BaseModel

from . import ServiceBase
from ..entities.schemas.api import BaseAPI, OriginContentModel

class APIServise(ServiceBase):
    def __init__(self, status: None = None) -> None:
        super().__init__(status)
        self.api = BaseAPI
        self.org = OriginContentModel
    
    def base_resp(self, code: int, info: str, type: str, data: Any) -> BaseModel:
        return self.api(
            code=code,
            info=info,
            org=self.org(
                content_type=type,
                data=data
            )
        )
