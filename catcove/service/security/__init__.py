# from .decorator import token_required
from .token import (
    get_payload,
    get_token,
    check_token,
    get_refreshtoken_payload,
    get_token_payload,
    generate_refresh_token,
    get_user
)
from functools import wraps

def token_required(wrapped):
    """ Fake function, change this func after all logic parts are over. """
    def decorator(func):
        @wraps(func)
        async def decorated_func(request, *args, **kwargs):
            ...
            response = await func(request, *args, **kwargs)
            return response
        return decorated_func
    return decorator(wrapped)
