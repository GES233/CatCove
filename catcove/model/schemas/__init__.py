from pydantic import BaseModel
from typing import Any, List, Union
from datetime import datetime

# ==== Body of API ==== #

class APIResponseBody(BaseModel):
    code: int
    data: str
    detail: BaseModel | str | None

# === Body in body === #

class APIResponceDetail(BaseModel):
    abstract: str
    body: BaseModel | str | None


class MessageBody(APIResponceDetail):
    abstract = "Message"
    body: str

class ErrorBody(APIResponceDetail):
    abstract = "Error feedback"
    body: str | BaseModel | List | Any

# ---- A instance ---- #

def return_6700(data: BaseModel | str):
    return APIResponseBody(
        code=6700,
        data="Responce successfully",
        detail=data
    )

# ==== Body of token ==== #

class TokenPrePayloadModel(BaseModel):
    """ The payload to generate the token. """
    uid: int

class AccessTokenPayloadModel(TokenPrePayloadModel):
    """ Mature token. """
    exp: Union[datetime, str, None]
