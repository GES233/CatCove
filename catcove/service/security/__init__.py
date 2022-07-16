from functools import wraps

def token_required(wrapped):
    """ Fake function, change this func after all logic parts are over. """
    def decorator(func):
        @wraps(func)
        async def decorated_func(request, *args, **kwargs):
            response = await func(request, *args, **kwargs)
            return response
        return decorated_func
    return decorator(wrapped)
