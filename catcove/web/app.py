from sanic import Sanic
from sanic.exceptions import SanicException

from ..settings import register_configure
from ..dependencies import register_dependencies
from ..services import register_services
from .errorhanders import custom_error
from .blueprints import register_routers
from .static import load_static


def create_app() -> Sanic:
    """Create a Sanic application to serving."""
    app = Sanic("Meow", env_prefix="APP_")

    register_configure(app)

    register_dependencies(app)

    register_services(app)

    custom_error(app)

    register_routers(app)

    load_static(app)

    return app


def create_config_app() -> Sanic:
    """Create a Sanic instance to set config."""
    try:
        app = Sanic.get_app("Meow")
        return app
    except SanicException:
        # The name must be same, some instruction will run this twice even third time.
        app = Sanic("Meow", env_prefix="APP_")
        register_configure(app)
        register_dependencies(app)
        register_services(app)
        return app
