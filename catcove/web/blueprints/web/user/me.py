from datetime import timedelta
from sanic import Request, Blueprint
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView

from .....entities.tables.users import Users

# from ..forms.user import ...

from .....usecase.users import UserService
from .....usecase.auth import AuthService
from .....services.render import render_page_template


async def profile(request: Request) -> HTTPResponse:
    user_ser: UserService = UserService(request.ctx.db_session)
    auth_ser: AuthService = request.ctx.cookie_ser
    
    # Query current user.
    db_user = await user_ser.check_user_token(
        request.ctx.current_user
    )
    if db_user == False:
        # 401.
        ...

    user_meta = user_ser.user

    # Transform data from db to a model.

    # Return data and render.
    return html(
        render_page_template(
            "account/me.html",
            user=request.ctx.current_user,
            db_user=user_meta
        )
    )
