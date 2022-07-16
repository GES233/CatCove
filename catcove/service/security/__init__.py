# Add Sanic_JWT here.
from sanic import Sanic
from sanic_jwt import Initialize
from functools import wraps
from pathlib import Path

from catcove.service.security.func import authenticate


def add_sanic_jwt(app: Sanic):

    # Configure and initialize
    if app.config["ENV"] == "dev" or\
            app.config["ENV"] == "development" or\
            app.config["ENV"] == "test":
        Initialize(
            app,
            authenticate,
            public_key=Path(app.config.APP_INSTANCE_PATH,'ecpubkey.pem'),
            private_key=Path(app.config.APP_INSTANCE_PATH,'eckey.pem')
        )
    else:  # production
        Initialize(
            app,
            authenticate,
            public_key=Path(app.config.APP_INSTANCE_PATH,'ecpubkey.pem'),
            private_key=Path(app.config.APP_INSTANCE_PATH,'eckey.pem')
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
