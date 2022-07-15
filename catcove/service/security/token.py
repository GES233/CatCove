from datetime import datetime, timedelta
from jose import jwe, jwt
from jose.exceptions import JWEError, JWTError

from model.schemas import TokenPrePayloadModel



def get_token(data: TokenPrePayloadModel, key: str, expire_time: timedelta | None = None):
    payload = data.dict()
    expire_time = datetime.utcnow() + timedelta(minutes=25) if not expire_time else \
        expire_time + datetime.utcnow()
    payload.update({"exp": expire_time})
    return str(jwt.encode(
            str(payload),
            key,
            "HS256"
            ), "utf-8")


def generate_refresh_token(data: TokenPrePayloadModel, key: str, expire_time: timedelta | None = None):
    payload = data.dict()
    expire_time = datetime.utcnow() + timedelta(minutes=25) if not expire_time else \
        expire_time + datetime.utcnow()
    payload.update({"exp": expire_time})
    return str(jwe.encrypt(
            str(payload), key,
            encryption="A256GCM",  # So the SECRET_KEY is 32 base64 character.
            algorithm="dir"), "utf-8")  # bytes -> string.


def get_token_payload(token: str, key: str) -> dict | None:
    if not token: return None
    try:
        payload = eval(str(jwt.decode(token, key, algorithms="HS256"), "utf-8"))
    except JWTError: return None
    else:
        return payload


def get_refreshtoken_payload(token: str, key: str) -> dict | None:
    if not token: return None
    try:
        payload = eval(str(jwe.encrypt(token, key), "utf-8"))
    except JWEError: return None
    else: return payload


def get_user(payload: dict | None) -> dict | None:
    if payload == None: return None
    exp = payload.pop("exp")
    return None if exp - datetime.utcnow() < 0 else payload
