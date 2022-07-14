from functools import wraps

from sanic.request import Request

from catcove.utils import schemasjson
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
                request.cookies.get("AuthorizationToken"),
                request.app.config.SECRET_KEY,
                "u"
            )

            if authenticated_info == 2:
                return schemasjson(
                    APIResponseBody(
                        code=4500,
                        data="UNAUTHORIZED",
                        detail=MessageBody(
                            body="疑验丁真，鉴定为假。"
                        )
                    ), 401
                )
            elif authenticated_info == 1:
                return schemasjson(
                    APIResponseBody(
                        code=4500,
                        data="UNAUTHORIZED",
                        detail=MessageBody(
                            body="需要登录捏。"
                        )
                    ), 401
                )
            elif authenticated_info == 3:
                # re-excute the gettoken.
                if request.headers.get("AuthRefreshToken"):
                    refresh_token_info = check_token(
                        request.headers.get("AuthRefreshToken"),
                        request.app.config.SECRET_KEY,
                        "r"
                    )
                    if refresh_token_info != 0:
                        # if refresh token expired or invalid:
                        return schemasjson(
                            APIResponseBody(
                                code=4500,
                                data="UNAUTHORIZED",
                                detail=MessageBody(
                                    body="您太久没登录了，需要重新登录"
                                )
                            ), 401
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
                        # request.headers.update(token = f"Authorization: Token {token}")
                        # response.cookie.get
                        request.cookies["AuthorizationToken"] = token
                        response = await func(request, *args, **kwargs)
                        # Use Set-cookie.
                        response.cookies["AuthorizationToken"] = token
                        return response
            elif authenticated_info == 0:
                response = await func(request, *args, **kwargs)
                return response
            
        return decorated_func
    return decorator(wrapped)