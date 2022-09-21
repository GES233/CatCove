import base64
from datetime import datetime, timedelta
from typing import Callable
import jwt

# from jose.jwe import encrypt, decrypt\
from sanic.request import Request
from sanic.response import HTTPResponse

from . import ServiceBase

from ..entities.tables.users import Users
from ..entities.schemas.auth import UserTokenPayload


class AuthService(ServiceBase):
    """Service about auth."""

    def __init__(
        self,
        token: str | None = None,
        cookie: str | None = None,
        ser_type: str | None = None,
        exp: timedelta = timedelta(days=7),
    ) -> None:
        super().__init__()
        """ 
            {
                "config": {
                    "type": "token/cookie/null", <-- ser_type
                }
            }
        """
        # Put cookie/token here, plz.
        if token:
            # Token -> payload.
            self.service_status["config"]["type"] = "token"
            self.token = token
            self.cookie = None
        elif cookie:
            # Cookie -> payload.
            self.service_status["config"]["type"] = "cookie"
            self.service_status["config"]["cookie"] = "UserMeta"
            self.token = None
            self.cookie = cookie
        else:
            # Generate token&cookie.
            self.exp = exp + datetime.utcnow()
            self.service_status["config"]["type"] = "" if not ser_type else ser_type
            self.service_status["config"]["cookie"] = "UserMeta"
            self.token = self.cookie = None

        self.cookie_encrypt_func: Callable[[str], str] = lambda x: base64.b64encode(
            x.encode("utf-8")
        ).decode("latin1")
        self.cookie_decrypt_func: Callable[[str], str] = lambda x: base64.b64decode(
            x.encode("latin1")
        ).decode("utf-8")
        self.token_encrypt_func = jwt.encode
        self.token_decrypt_func = jwt.decode
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

    def gen_payload(self, user: Users, exp: timedelta | None = None) -> dict:
        # May need return as bool.
        # Set exp first.
        if exp:
            self.exp = datetime.utcnow() + exp
        self.payload = UserTokenPayload(
            id=user.id,
            nickname=user.nickname,
            status=user.status,
            role=user.role,
            exp=datetime.timestamp(self.exp),
        ).dict()
        return self.payload

    def encrypt(self, sk: str | None = None) -> bool:
        """From payload/raw to token/cookie."""
        if not self.payload:
            # Not have raw/payload.
            return False

        if self.service_status["config"]["type"] != "token":
            if not self.raw:
                _ = self.dict_to_str()
                return False if _ == False else ...
            self.cookie = self.cookie_encrypt_func(self.raw)
        else:
            """It will raise Error if not fetched key."""
            # From payload.
            self.token = self.token_encrypt_func(
                self.payload,
                sk,
                "ES256",
            )

        return True

    def decrypt(self, pk: str = "") -> bool:
        """From token/cookie to payload."""
        try:
            if self.service_status["config"]["type"] == "token":
                """It will raise Error if not fetched key."""
                self.payload = self.token_decrypt_func(self.token, pk, ["ES256"])
            else:
                self.raw = self.cookie_decrypt_func(self.cookie)
            return True
        except:
            return False

    def str_to_dict(self) -> bool:
        """raw -> payload"""
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
        """payload -> raw"""
        if not self.payload:
            return False
        self.raw = self.payload.__str__()
        return True

    def set_cookie(self, response: HTTPResponse, remember: bool = True) -> HTTPResponse:
        response.cookies[self.service_status["config"]["cookie"]] = self.cookie
        response.cookies[self.service_status["config"]["cookie"]]["path"] = "/"
        response.cookies[self.service_status["config"]["cookie"]]["httponly"] = True
        if remember:
            response.cookies[self.service_status["config"]["cookie"]]["expires"] = self.exp

        return response

    def del_cookie(self, request: Request, response: HTTPResponse) -> HTTPResponse:
        if request.cookies.get(self.service_status["config"]["cookie"]):
            response.cookies[self.service_status["config"]["cookie"]] = ""
            response.cookies[self.service_status["config"]["cookie"]]["max-age"] = 0

        return response

    def set_key(self) -> str:
        """Hard to be import services.render.render_api_resp."""
        return self.token
