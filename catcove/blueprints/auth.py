from sanic import Blueprint, Request
from sanic.response import html, redirect
from sanic.views import HTTPMethodView
from sanic.exceptions import MethodNotAllowed

from ..business.auth import login_authentication_logic
from ..services.security.cookie import delete_login_cookie
from ..services.render import render_template
from ..models.forms.auth import LoginForm, validate_login_form
from ..models.schemas.request import UserLoginModel

auth_bp = Blueprint("auth")

from pprint import pprint

class UserLoginView(HTTPMethodView):

    async def get(self, request: Request):
        # Render
        return self.login_render(self, LoginForm())

    async def post(self, request: Request):
        # Submit -> POST

        # Initial work.
        form_data = request.form
        if not form_data:
            raise MethodNotAllowed(
                "Post method need a form."
            )  # BadRequest better.

        model = validate_login_form(LoginForm(data=form_data))

        # Check here.
        if not isinstance(model, UserLoginModel):
            return self.login_render(self, model)  # html_content
        
        # Business Logic.
        if login_authentication_logic(model, request.ctx.session):
            # Set-cookie.
            ...
            return redirect("/")
        else:
            # 查无此人/密码错误
            # Re-render.'''
            ...
            return self.login_render()
        # return await self.get(request)
    
    def login_render(self, form) -> HTTPMethodView:
        return html(render_template(
            'login.html',
            role="Login",
            form=form))

@auth_bp.route("/logout", methods=["GET"])
async def log_out(request):
    content = html(render_template('logout.html'))
    return delete_login_cookie(content)

auth_bp.add_route(UserLoginView.as_view(), "/login")