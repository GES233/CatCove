from functools import wraps

from sanic.request import Request

from catcove.utils import schemasjson
from model.schemas import (
    MessageBody,
    APIResponseBody
)
from .token import (
    generate_refresh_token,
    get_refreshtoken_payload,
    get_token_payload,
    get_user,
    get_token
)


def return_invalid(text: str | None = None):
    return APIResponseBody(
        code=4500,
        data="UNAUTHORIZED",
        detail=MessageBody(body="疑验丁真，鉴定为假。")
    ) if not text else APIResponseBody(
        code=4500,
        data="UNAUTHORIZED",
        detail=MessageBody(body=text)
    )


def token_required(wrapped):
    """ Fake function, change this func after all logic parts are over. """
    def decorator(func):
        @wraps(func)
        async def decorated_func(request: Request, *args, **kwargs):
            token_from_head = request.cookies.get("AuthorizationToken")
            token = get_token_payload(token_from_head)  # not have token, or token invalid.
            if not token:
                return schemasjson(return_invalid(), 401)
            elif not get_user(token):
                return schemasjson(return_invalid("疑验丁真，鉴定为你无法证明你是你。"), 401)
            else:
                response = await func(request, *args, **kwargs)
                return response
        return decorated_func
    return decorator(wrapped)
