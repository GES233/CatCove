from datetime import datetime, timedelta
from jose import jwe, jwt
from jose.exceptions import JWEError, JWTError
from pydantic import ValidationError


from ...model.schemas import AccessTokenPayloadModel


# from catcove.app import create_config_app
# app = create_config_app()
# key = app.config.SECRET_KEY

def get_token(data: dict, key: str, expire_time: timedelta | None = None, sign: bool = True):
    payload = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=25) if not expire_time else \
        expire_time + datetime.utcnow()
    payload.update({"exp": expire_time})
    if not sign:
        return str(jwe.encrypt(
            str(payload),
            key,
            encryption="A256GCM",
            algorithm="dir"
        ), "utf-8")
    else:
        return str(jwt.encode(
            str(payload),
            key,
            "HS256"
        ), "utf-8")


def get_payload(
    token: str,
    key: str | bytes,
    sign: bool = True
    ) -> str:
    if not sign:
        return str(jwe.decrypt(token, key), "utf-8")
    else:
        return str(jwt.decode(token, key, algorithms="HS256"), "utf-8")


def check_token(token, key, token_type: str = "u") -> int:
    """ 疑验丁真，鉴定为假 """
    if not token:
        return 1
    
    try:
        raw_payload: dict = eval(get_payload(
            token,
            key,
            True if token_type == "u" else False
        ))
        payload: AccessTokenPayloadModel = AccessTokenPayloadModel(
            uid=raw_payload.pop("uid"),
            exp=raw_payload.pop("exp")
        )
    except JWEError as refresh_token_error:
        # invalid for refresh token.
        ...
        return 2
    except JWTError as user_token_error:
        # invalid for user token.
        ...
        return 2
    except ValidationError as token_payload_error:
        # invalid token.
        ...
        return 2
    
    if payload.exp - datetime.utcnow() < 0:
        # expired.
        return 3
    
    return 0
