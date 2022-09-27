from typing import Any
from pydantic import BaseModel
from functools import update_wrapper

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
    
    def api_add_properties(self, f):
        """打算采用装饰器的方式来加载程序，返回结果。"""
        def wrapper_func(f, *args, **kwargs):
            return f(*args, **kwargs)
        return update_wrapper(wrapper_func, f)
    
    def _not_found(self, *args, **kwargs) -> dict:
        return ...
    
    @api_add_properties
    def not_found(self, target):
        """用例：

            ```
            @not_found
            return api.base_resp("查无此人")
            ```
        """
        ...