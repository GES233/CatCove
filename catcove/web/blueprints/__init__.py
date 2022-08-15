from sanic import Sanic
from sanic.response import text

def register_routers(app: Sanic):
    # API
    # from .api import api
    # app.blueprint(api)

    # Views
    # from .blueprints import views
    # app.blueprint(views)
    ...
    @app.route("/")
    async def index(request): return text("Null")
