from functools import wraps
from sanic.response import redirect
from sanic.request import Request


def token_auth() -> None: pass
def cookie_auth() -> None: pass


def resp_unauth_api(): return ...


def token_required(wrapped):
    def decorated(func):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):

            current_user = token_auth(request.headers.get(""))

            if isinstance(current_user, dict):
                response = await func(request, *args, **kwargs)
                return response
            else:
                return resp_unauth_api()
        return decorated_function
    return decorated(wrapped)


def cookie_required(wrapped):
    def decorated(func):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):

            current_user = cookie_auth(request.cookies.get(""))

            if isinstance(current_user, dict):
                response = await func(request, *args, **kwargs)
                return response
            else:
                return redirect("/login")
        return decorated_function
    return decorated(wrapped)
