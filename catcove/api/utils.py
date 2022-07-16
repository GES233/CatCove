from pydantic import BaseModel, ValidationError
from sanic import HTTPResponse, Request
from json import loads
from typing import Any

from catcove.utils import schemasjson
from ..model.schemas import SingleSchemasErrorModel, APIResponseBody, ErrorBody


def body2model_via_json(request: Request, model: BaseModel) -> BaseModel | HTTPResponse | None | Any:
    try:
        raw_data = request.body
        if not raw_data: return None
        json_content = loads(request.body)
        result = model(**json_content)
        result = model(**result)
    except TypeError or ValueError:
         return schemasjson(APIResponseBody(
                code=6002,
                data="Ooops",
                detail=ErrorBody(
                    body="JSON解码过程中发生错误"
                )
            ))
    except ValidationError as to_model:
        error_list = []
        for e in to_model.errors():
            error_list.append(
                SingleSchemasErrorModel(**e)
            )
        return schemasjson(APIResponseBody(
                code=6002,
                data="Ooops",
                detail=ErrorBody(
                    body=error_list
                )
            ))
    except: return schemasjson(APIResponseBody(
                code=6002,
                data="Ooops",
                detail=ErrorBody(
                    body="一些未知错误发生了"
                )
            ))
    else: return result.json()


def body2model_via_form(request: Request, model: BaseModel) -> BaseModel | HTTPResponse | None | Any: ...
