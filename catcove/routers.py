from sanic import Sanic
from sanic.response import text

def register_routers(app: Sanic):

    # Response from root
    @app.route("/", methods=["GET"])
    async def index(request):
        return text("Hello, index page here.")
    
    # API
    from .api import api
    
    app.blueprint(api)
