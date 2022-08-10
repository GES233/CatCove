from json import loads
from typing import Any
from pydantic import BaseModel, ValidationError
from sanic.request import Request
from sanic.response import HTTPResponse

from ..models.schemas.exceptions import PydanticErrorModel


def json2model(
    request: Request,
    model: BaseModel
) -> BaseModel | HTTPResponse | None | Any:
    try:
        body = request.body
        if not body: return None
        json_content = loads(body)
        result = model(**json_content)
    except TypeError or ValueError:
        # request -> json
        ...
    except ValidationError as to_model:
        # json -> model
        error_list = []
        for e in to_model.errors():
            error_list.append(
                PydanticErrorModel(**e)
            )
        ...
    except:
        ...
    else: return result
