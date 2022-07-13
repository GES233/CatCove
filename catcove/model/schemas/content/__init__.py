from pydantic import BaseModel
from typing import List, Any, Union

paragraph = Union[
    str,
    BaseModel,
    Any,
    None
]