from sanic import Sanic, Blueprint

demo = Blueprint("demo_index")

def register_routers(app: Sanic):
    # API
    # from .api import api
    # app.blueprint(api)

    # Views
    # from .blueprints import views
    # app.blueprint(views)
    ...
