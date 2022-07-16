from sanic import Sanic
from catcove.dependencies import (
    load_config,
    register_basic_responce,
    register_routers,
    register_static,
    register_middleware,
    register_extensions
)


def create_app(mode: str | None):
    app = Sanic("CatCove")

    # Register application.
    mode = "dev" if mode == None else mode
    app.update_config({"ENV": mode})
    load_config(app, "instance")

    # Extensions
    register_extensions(app)

    # Linsteners and Middleware.
    register_middleware(app)
    
    # Static
    register_static(app)
    
    # ERROR handler.
    ...

    # Responce.
    register_basic_responce(app)

    # Routers.
    register_routers(app)

    return app


def create_config_app(mode: str | None = None):
    db_app = Sanic.get_app("CatCove", force_create=True)

    # Register application.
    mode = "dev" if mode == None else mode
    db_app.update_config({"ENV": mode})
    load_config(db_app)

    # return app.
    return db_app
