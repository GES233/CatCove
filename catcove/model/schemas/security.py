from pydantic import BaseModel
from typing import Union
from datetime import datetime

# ==== Body of token ==== #

class TokenPrePayloadModel(BaseModel):
    """ The payload to generate the token. """
    uid: int

class AccessTokenPayloadModel(TokenPrePayloadModel):
    """ Mature token. """
    exp: Union[datetime, str, None]
