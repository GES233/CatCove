from functools import wraps
from pydantic import ValidationError
from sanic import Request, json

from ....usecase.api import APIServise
from ...blueprints.api.helper import code, info


def api_validator(wrapped):
    def decorated(func):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):
            try:
                response = await func(request, *args, **kwargs)
            except ValidationError as val_error:
                api = APIServise()
                ...
                return json(
                    api.base_resp(code=..., info=..., type=..., data={...}).json(),
                    status=...,
                    dumps=lambda x: x,
                )
            else:
                return response

        return decorated_function

    return decorated(wrapped)
