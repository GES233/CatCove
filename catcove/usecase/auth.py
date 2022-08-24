from datetime import datetime, timedelta
from jwt import PyJWT
from Crypto.PublicKey import ECC
from sanic.request import Request
from sanic.response import HTTPResponse
import base64

from . import ServiceBase

from ..entities.tables.users import Users
from ..entities.schemas.auth import UserTokenPayload
from ..services.security.user import user2payload

class AuthService(ServiceBase):
    """ Service about auth. """
    def __init__(
        self,
        status: dict | None = None,
        token: str | None = None,
        cookie: str | None = None,
        exp: timedelta = timedelta(days=7)
    ) -> None:
        super().__init__(status)
        # Put cookie/token here, plz.
        if token:
            self.token = token
            self.cookie = None
        elif cookie:
            self.token = None
            self.cookie = cookie
        else: self.token = self.cookie = None

        self.raw: str = ""
        self.payload: dict = {}
        # payload["id"]: int
        # payload["nickname"]: str
        # >> Update when change.
        # payload["status"]: str | Enum\
        # >> Update when change.
        # payload["role"]: str | Enum
        # >> Update when change.
        # payload["timezone"]: int | (-12, 12)
        # payload["exp"]: float
        self.exp: datetime = datetime.utcnow() + exp
    
    def gen_payload(self, user: Users, exp: timedelta | None = None) -> dict:
        # May need return as bool.
        # Set exp first.
        if exp:
            self.exp = datetime.utcnow() + exp
        self.payload = user2payload(user, datetime.timestamp(self.exp))
        return self.payload

    def encrypt(self) -> bool:
        """ From payload/raw to token/cookie. """
        if not (self.raw or self.payload):
            # Not have raw/payload.
            return False
        if not self.raw and self.payload:
            _ = self.dict_to_str()
            return False if _ == False else ...
        self.cookie = base64.b64encode(self.raw.encode("utf-8")).decode("latin1")
        self.token = ...
        return True
    
    def decrypt(self) -> bool:
        """ From token/cookie to payload. """
        if self.token:
            self.raw = self.token
        elif self.cookie:
            self.raw = base64.b64decode(self.cookie.encode("latin1")).decode("utf-8")
        return True
    
    def str_to_dict(self) -> bool:
        """ raw -> payload """
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
        """ payload -> raw """
        if not self.payload: return False
        self.raw = self.payload.__str__()
        return True
    
    def set_cookie(self, response: HTTPResponse) -> HTTPResponse:
        response.cookies["UserMeta"] = self.cookie
        response.cookies["UserMeta"]["path"] = "/"
        response.cookies["UserMeta"]["httponly"] = True
        response.cookies["UserMeta"]["expires"] = self.exp

        return response
    
    def del_cookie(self, request: Request, response: HTTPResponse)\
        -> HTTPResponse:
        if request.cookies.get("UserMeta"):
            response.cookies["UserMeta"] = ""
            response.cookies["UserMeta"]["max-age"] = 0
        
        return response
    
    def set_key(self) -> str:
        """ Hard to be import services.render.render_api_resp. """
        return self.token
