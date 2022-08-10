from sanic import Sanic
from sanic.response import text

def register_routers(app: Sanic):
    # API
    from .blueprints.api import api
    app.blueprint(api)

    # Views
    from .blueprints import views
    app.blueprint(views)
