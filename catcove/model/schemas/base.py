from pydantic import BaseModel
from typing import Any, List


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

# ---- A instance ---- #

def return_6700(data: BaseModel | str):
    return APIResponseBody(
        code=6700,
        data="Responce successfully",
        detail=data
    )
