from typing import Any
from pydantic import BaseModel

from . import ServiceBase
from ..entities.schemas.api import BaseAPI, OriginContentModel


class APIServise(ServiceBase):
    def __init__(self, status: None = None) -> None:
        super().__init__(status)
        self.api = BaseAPI
        self.org = OriginContentModel

    def base_resp(self, code: int, info: str, type: str, data: Any) -> BaseAPI:
        _rsp: dict = {
            "code": code,
            "info": info,
            "type": type,
            "data": data
        }
        return self.api(
            code=_rsp["code"],
            info=_rsp["info"],
            org=self.org(
                content_type=_rsp["type"],
                data=_rsp["data"]
            )
        )
    
    def not_found(self, target):
        # Generate a dict here.
        return self.base_resp(
            ...
        )
