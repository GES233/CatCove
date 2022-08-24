from datetime import timedelta
from sanic import Request, Blueprint
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView

from .....entities.tables.users import Users

# from ..forms.user import ...

from .....usecase.users import UserService
from .....usecase.auth import AuthService
from .....services.render import render_template

me_bp = Blueprint("me")


# @place_a_decorator_here()
async def get(request: Request):
    user_ser = UserService(request.ctx.db_session)
    auth_ser = request.ctx.cookie_ser
    
    # Query current user.
    db_user = await user_ser.check_user_token(
        request.ctx.current_user
    )
    if db_user == False:
        # 401.
        ...

    user_meta = user_ser.user

    # Return data and render.
    ...
