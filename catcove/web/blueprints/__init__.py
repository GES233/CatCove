from sanic import Sanic


def register_routers(app: Sanic) -> None:
    # API
    from .api import api_bp

    app.blueprint(api_bp)

    # Views
    from .web import views

    app.blueprint(views)
