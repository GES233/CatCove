from datetime import timedelta
from sanic import Request, Blueprint
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView

from .....entities.tables.users import Users
from .....entities.schemas.user import UserProfile

# from ..forms.user import ...

from .....usecase.users import UserService
from .....usecase.auth import AuthService
from .....services.render import render_page_template


async def profile(request: Request) -> HTTPResponse:
    user_ser: UserService = UserService(request.ctx.db_session)

    # Query current user.
    db_user = await user_ser.check_user_token(request.ctx.current_user)
    if db_user == False:
        # 401.
        ...
        user_profile = None
    else:
        # Transform data from db to a model.
        user_profile = UserProfile(
            **{
                item.name: getattr(user_ser.user, item.name)
                for item in user_ser.user.__table__.columns
            }
        )

    # Return data and render.
    return html(
        render_page_template(
            "account/me.html",
            cookie_user=request.ctx.current_user,
            user=user_profile
        )
    )
