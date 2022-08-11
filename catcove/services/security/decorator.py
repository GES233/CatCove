from functools import wraps
from sanic.response import redirect


def token_auth(): return True
def cookie_auth(): return True

def resp_unauth_api(): return ...


def token_required(wrapped):
    def decorated(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):

            is_authenticated = token_auth(request)

            if is_authenticated:
                response = await func(request, *args, **kwargs)
                return response
            else:
                return resp_unauth_api()
        return decorated_function
    return decorated(wrapped)


def cookie_required(wrapped):
    def decorated(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):

            is_authenticated = cookie_auth(request)

            if is_authenticated:
                response = await func(request, *args, **kwargs)
                return response
            else:
                return redirect("/login")
        return decorated_function
    return decorated(wrapped)
