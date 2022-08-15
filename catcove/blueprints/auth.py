from sanic import Blueprint, Request
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView

from ..business.auth import login_authentication_logic
from ..services.security.cookie import delete_login_cookie, add_login_cookie
from ..services.render import render_template
from ..models.forms.auth import (
    LoginForm,
    validate_login_form,
    form_input,
    user_not_exist_front,
    password_not_match_front
)
from ..models.schemas.request import UserLoginModel

auth_bp = Blueprint("auth")


class UserLoginView(HTTPMethodView):

    form = LoginForm()

    async def get(self, request: Request):
        # Render
        return self.login_render(self.form)

    async def post(self, request: Request):
        # Submit -> POST
        status_code = request.args.get("from")
        if status_code == "sg": self.get(self.form)

        # Initial work.
        form_data = request.form
        if not form_data:
            # 怕有人开控制台搞事
            return self.login_render(form_input(self.form))

        # Check the form, if invalid, login failed.
        model = validate_login_form(LoginForm(data={
            "nickname": form_data.get("nickname"),
            "password": form_data.get("password"),
            "remember": form_data.get("remember")
        }))
        if not isinstance(model, UserLoginModel):
            return self.login_render(model)
        
        # Check.
        user = await login_authentication_logic(model, request.ctx.session)

        if user is None:
            return self.login_render(user_not_exist_front(self.form))
        elif isinstance(user, bool):
            return self.login_render(password_not_match_front(self.form))
        else:
            return add_login_cookie(redirect("/"), user)
    
    def login_render(self, form) -> HTTPResponse:
        return html(render_template(
            'auth/login.html',
            role="Login",
            form=form))


async def log_out(request):
    content = html(render_template('auth/logout.html'))
    return delete_login_cookie(request, content)


auth_bp.add_route(UserLoginView.as_view(), "/login")
auth_bp.add_route(log_out, "/logout")
