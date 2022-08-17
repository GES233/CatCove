from datetime import datetime, timedelta
from jwt import PyJWT
from Crypto.PublicKey import ECC
from sanic.request import Request
from sanic.response import HTTPResponse


class AuthService:
    def __init__(
        self,
        token: str | None = None,
        cookie: str | None = None,
        status: dict | None = None
    ) -> None:
        if token:
            self.token = token
            self.cookie = None
        elif cookie:
            self.token = None
            self.cookie = cookie
        else: self.token = self.cookie = None

        if status:
            self.service_status = status
        else:
            self.service_status = {
                "config": {},
                "errors": []
            }
        
        self.raw: str = ""
        self.payload: dict = {}
        self.exp: datetime = datetime.utcnow()
    
    def encrypt(self, request: Request) -> bool:
        """ From payload/raw to token/cookie. """
        if not (self.raw or self.payload): return False
        self.token = ...
        self.cookie = ...
        return True
    
    def decrypt(self, request: Request) -> bool:
        """ From token/cookie to payload. """
        if self.token:
            self.raw = self.token
        elif self.cookie:
            self.raw = self.cookie
        return True
    
    def str_to_dict(self) -> bool:
        if not self.raw:
            # Not encrypted.
            ...
            return False
        
        _dict = eval(self.raw)

        if not isinstance(_dict, dict):
            # Not a dict.
            ...
            return False

        self.payload = _dict
        return True
    
    def dict_to_str(self) -> bool:
        if not self.payload: return False
        self.raw = self.payload.__str__()
        return True
    
    def set_cookie(self, response: HTTPResponse) -> HTTPResponse:
        response.cookies["UserMeta"] = self.cookie
        response.cookies["UserMeta"]["path"] = "/"
        response.cookies["UserMeta"]["httponly"] = True
    
    def del_cookie(self, request: Request, response: HTTPResponse)\
        -> HTTPResponse:
        if request.cookies.get["UserMeta"]:
            response.cookies["UserMeta"] = ""
            response.cookies["UserMeta"]["max-age"] = 0
        
        return response
