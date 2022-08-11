from typing import Tuple, Any
from sanic import Request
from sanic.response import HTTPResponse, redirect

from ...models.tables.users import Users

COOKIE_MAX_AGE = 3600 * 24 * 45


def add_login_cookie(response: HTTPResponse, user: Users) -> HTTPResponse:

    # set Cookie.
    response.cookies["UserMeta"] = ...
    response.cookies["UserMeta"]["path"] = "/"
    response.cookies["UserMeta"]["httponly"] = True
    response.cookies["UserMeta"]["expires"] = ...
        # CurrentTime + COOKIE_MAX_AGE

    return response


def delete_login_cookie(response: HTTPResponse) -> HTTPResponse:
    if response.cookies.get("UserMeta"):
        response.cookies["UserMeta"]["max-age"] = 0
        return response
    else: return redirect("https://www.bilibili.com/")
    # return response


def check_cookie(request: Request) -> Tuple[bool, Any]:
    try:
        cookie = request.cookies.get("UserMeta")
        ...
    except TypeError or ValueError:
        return False, None
    else:
        return True, ...


def generate_cookie() -> str:
    ...
