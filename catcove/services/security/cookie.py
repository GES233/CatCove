from datetime import datetime, timedelta
from typing import Tuple, Any
from Crypto.PublicKey import ECC
from sanic import Request
from sanic.response import HTTPResponse, redirect, text
import base64

from ...entities.tables.users import Users

COOKIE_MAX_AGE = 3600 * 24 * 45


def add_login_cookie(response: HTTPResponse, user: Users) -> HTTPResponse:

    # User payload.
    user_cookie, exp = generate_cookie(user)

    # set Cookie.
    response.cookies["UserMeta"] = base64.b64decode(user_cookie.encode("utf-8")).decode("latin1")
    response.cookies["UserMeta"]["path"] = "/"
    response.cookies["UserMeta"]["httponly"] = True
    response.cookies["UserMeta"]["expires"] = exp
        # CurrentTime + COOKIE_MAX_AGE

    return response


def delete_login_cookie(request: Request, response: HTTPResponse) -> HTTPResponse:
    if request.cookies.get("UserMeta"):
        response.cookies["UserMeta"] = ""
        response.cookies["UserMeta"]["max-age"] = 0
        return response
    else: return redirect("https://www.bilibili.com/")
    # return text(f"{request.cookies}")


def check_cookie(request: Request) -> Tuple[bool, Any]:
    try:
        cookie: str = request.cookies.get("UserMeta")
        if not cookie: return False, None
    except TypeError or ValueError:
        return False, None
    else:
        cookie_text = base64.b64decode(cookie.encode("latin1")).decode("utf-8")
        return True, ...


def generate_cookie(user: Users) -> Tuple[str, datetime]:
    from .user import user2payload
    exp_time = datetime.utcnow() + timedelta(days=7)
    return user2payload(user, exp_time.timestamp()).__str__(), exp_time

