from pydantic import BaseModel
from typing import Tuple, List, Any

from .base import APIResponceDetail

class ErrorBody(APIResponceDetail):
    abstract = "Error feedback"
    body: str | BaseModel | List | Any

# ==== Errors ==== #

class SingleSchemasErrorModel(BaseModel):
    loc: Tuple[int | str]
    msg: str
    type: str
