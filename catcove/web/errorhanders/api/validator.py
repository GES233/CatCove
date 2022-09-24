from functools import wraps
from pydantic import ValidationError
from sanic import Request, json
from sanic.response import HTTPResponse

from ....usecase.api import APIServise
from ...blueprints.api.helper import code, info


def api_validator(wrapped):
    def decorated(func):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs) -> HTTPResponse:
            try:
                response = await func(request, *args, **kwargs)
            except ValidationError as val_error:
                api = APIServise()

                # Parse the error.
                ...

                # Render the error.
                return json(
                    api.base_resp(code=..., info=..., type=..., data={...}).json(),
                    status=...,
                    dumps=lambda x: x,
                )
            else:
                return response

        return decorated_function

    return decorated(wrapped)
