from datetime import datetime
from sanic import Blueprint, Request

from .pages import index_bp
from .auth import auth_bp
from .user import user_bp

""" Render with Jinja2. """
views = Blueprint.group(
    index_bp,
    auth_bp,
    user_bp
)

# Add a middleware to parse the cookie.
# And render the result.

from ....usecase.auth import AuthService

@views.middleware("request")
async def fetch_cookie(request: Request) -> None:
    request.ctx.cookie_ser = AuthService()
    if not request.cookies.get(request.ctx.cookie_ser.service_status["config"]["cookie"]):
        # Do nothing.
        request.ctx.current_user = None
    else:
        request.ctx.cookie_ser = AuthService(
            cookie = request.cookies.get(request.ctx.cookie_ser.service_status["config"]["cookie"])
        )
        de_cookie = request.ctx.cookie_ser.decrypt()
        de__cookie = request.ctx.cookie_ser.str_to_dict()
        if de_cookie == True and de__cookie == True:
            _payload = request.ctx.cookie_ser.payload
            if _payload["exp"] < datetime.timestamp(datetime.utcnow()):
                request.ctx.current_user = None
            else:
                request.ctx.current_user = request.ctx.cookie_ser.payload
        else:
            request.ctx.current_user = None
            request.ctx.cookie_ser = AuthService()
