from typing import Tuple
from pydantic import BaseModel

class PydanticErrorModel(BaseModel):
    loc: Tuple[int | str]
    msg: str
    tpye: str
