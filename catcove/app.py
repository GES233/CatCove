from sanic import Sanic
from sanic.exceptions import SanicException

from .settings import register_configure
from .dependencies import (
    register_service,
    load_static)
from .routers import register_routers


def create_app() -> Sanic:
    """ Create a Sanic application to run. """
    app = Sanic("Meow", env_prefix="APP_")

    register_configure(app)

    register_service(app)

    register_routers(app)

    load_static(app)
    
    return app

def create_config_app() -> Sanic:
    try:
        app = Sanic.get_app("Meow")
        return app
    except SanicException:
        # The name must be same, some instruction will run this twice even third time.
        app = Sanic("Meow", env_prefix="APP_")
        register_configure(app)
        return app
