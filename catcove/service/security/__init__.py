# Add Sanic_JWT here.
from sanic import Sanic
from sanic_jwt import Initialize
from functools import wraps

from catcove.service.security.func import authenticate


def add_sanic_jwt(app: Sanic):

    # Configure and initialize
    if app.config["ENV"] == "dev" or\
            app.config["ENV"] == "development" or\
            app.config["ENV"] == "test":
        from setting.dev import SanicJWTDevConfig

        Initialize(
        app,
        authenticate,
        configuration_class=SanicJWTDevConfig
        )
    else:  # production
        from setting.pro import SanicJWTProConfig

        Initialize(
        app,
        authenticate,
        configuration_class=SanicJWTProConfig
        )

def token_required(wrapped):
    """ Fake function, change this func after all logic parts are over. """
    def decorator(func):
        @wraps(func)
        async def decorated_func(request, *args, **kwargs):
            response = await func(request, *args, **kwargs)
            return response
        return decorated_func
    return decorator(wrapped)
