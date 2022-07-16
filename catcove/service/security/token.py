from datetime import datetime, timedelta
from jose import jwe, jwt
from jose.utils import base64url_decode, base64url_encode
from jose.exceptions import JWEError, JWTError
from pydantic import BaseModel

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
    if isinstance(data, BaseModel):
        payload = data.dict()
    elif isinstance(data, dict):
        payload = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=25) if not expire_time else \
        expire_time + datetime.utcnow()
    payload.update({"exp": expire_time})
    return str(jwe.encrypt(
            str(payload), base64url_decode(key),
            encryption="A256GCM",  # So the SECRET_KEY is 32 base64 character.
            algorithm="dir"), "utf-8")  # bytes -> string.


def get_token_payload(token: str, key: str) -> dict | None:
    if not token: return None
    try:
        payload = eval(str(jwt.decode(token, base64url_decode(key), algorithms="HS256"), "utf-8"))
    except JWTError: return None
    else:
        return payload


def get_refreshtoken_payload(token: str, key: str) -> dict | None:
    if not token: return None
    try:
        payload = eval(str(
            jwe.decrypt(token, base64url_encode(bytes(key, "utf-8"))), "utf-8"
        ))
    except JWEError: return None
    else:
         return payload


def get_user(payload: dict | None) -> dict | None:
    if payload == None: return None
    exp = payload.pop("exp")
    print(exp)
    return None if exp - datetime.utcnow() < 0 else payload


if __name__ == "__main__":
    token = "yJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..HCnMsCqzyoN_PQubbiyt0w.9_hPSq2aPB23xvdRVfAptloiGpXQIJyO_jecF-4sFSpXOXpia9n4HbNCunGLbLNCYoTMwrKEKep-aRCMeQOUJ5Xl5w.hEuIGVPxLXGVLTayhA-37"
    key = "SRSGjUV5SNzML4DnU9ibDMYUGyQdo33SZqXi/92VLC8="
    
    print("-------")
    print(jwe.decrypt(token, base64url_decode(bytes(key, "utf-8"))))
