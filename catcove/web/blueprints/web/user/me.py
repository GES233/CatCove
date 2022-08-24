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

class UserProfileView(HTTPMethodView):

    def common(self, request: Request):
        self.user_ser = UserService(request.ctx.db_session)
        self.auth_ser = AuthService()
        
        # Query current user.
        self.auth_ser.cookie = request.cookies.get("UserMeta")
        ...

    # @place_a_decorator_here()
    async def get(self, request: Request):
        self.common(request)

        # Query data.

    async def post(self, request: Request):
        self.common(request)
        # Update cookie, plz.
        ...
