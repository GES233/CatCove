from functools import wraps

from sanic import json
from sanic.request import Request

from model.schemas import (
    MessageBody,
    APIResponseBody
)
from .token import (
    check_token,
    get_payload,
    get_token
)


def token_required(wrapped):

    def decorator(func):

        @wraps(func)
        async def decorated_func(request: Request, *args, **kwargs):

            authenticated_info = check_token(
                request.token,
                request.app.config.SECRET_KEY,
                "u"
            )

            if authenticated_info == 2:
                return json(
                    APIResponseBody(
                        code=4500,
                        data="UNAUTHORIZED",
                        detail=MessageBody(
                            body="疑验丁真，鉴定为假。"
                        )
                    ).dict(), 401
                )
            elif authenticated_info == 1:
                return json(
                    APIResponseBody(
                        code=4500,
                        data="UNAUTHORIZED",
                        detail=MessageBody(
                            body="需要登录捏。"
                        )
                    ).dict(), 401
                )
            elif authenticated_info == 3:
                # re-excute the gettoken.
                if request.headers.getone("X-Auth-RefreshToken", None):
                    refresh_token_info = check_token(
                        request.headers.get("X-Auth-RefreshToken", None),
                        request.app.config.SECRET_KEY,
                        "r"
                    )
                    if refresh_token_info != 0:
                        # if refresh token expired or invalid:
                        return json(
                            APIResponseBody(
                                code=4500,
                                data="UNAUTHORIZED",
                                detail=MessageBody(
                                    body="您太久没登录了，需要重新登录"
                                )
                            ).dict(), 401
                        )
                    else:
                        dict = eval(get_payload(
                            token=request.token,
                            key=request.app.config.SECRET_KEY,
                            sign=True
                            ))
                        del dict["exp"]
                        token = get_token(
                            # Using old data.
                            data = dict,
                            sign=True)
                        request.headers.update(token = f"Authorization: Token {token}")
                        response = await func(request, *args, **kwargs)
                        return response
            elif authenticated_info == 0:
                response = await func(request, *args, **kwargs)
                return response
            
        return decorated_func
    return decorator(wrapped)