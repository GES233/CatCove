from sanic import Blueprint, Request
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView
from sanic.exceptions import SanicException

from ....entities.schemas.user.request import UserLoginModel
from ....services.render import render_template
from ....usecase.users import UserService
from ....usecase.auth import AuthService
from .forms.auth import (
    LoginForm,
    validate_login_form,
    user_not_exist,
    password_not_match
)

auth_bp = Blueprint("auth")


class UserLoginView(HTTPMethodView):

    form = LoginForm()

    def login_render(self, form) -> HTTPResponse:
        return html(render_template(
            'auth/login.html',
            role="Login",
            form=form))

    async def get(self, request: Request):
        # Render
        return self.login_render(self.form)

    async def post(self, request: Request):
        # Submit -> POST
        form_data = request.form

        model = validate_login_form(self.form(data={
            "nickname": form_data.get("nickname"),
            "password": form_data.get("password"),
            "remember": form_data.get("remember")
        }))
        if not isinstance(model, UserLoginModel):
            return self.login_render(model)

        cookie = AuthService()
        user = UserService(request.ctx.db_session)
        
        user_exist = user.check_common_user(model.nickname)
        if user_exist == False:
            return self.login_render(user_not_exist(self.form))
        else:
            password_match = user.user.check_passwd(model.password)
            if password_match == False:
                return self.login_render(password_not_match(self.form))
        
        cookie.payload = user.get_user_token()
        _ = cookie.dict_to_str()
        if _ == False:
            raise SanicException("Some error happend when generate token.")
        _ = cookie.encrypt()
        if _ == False:
            raise SanicException("Some error happend when generate token.")
        
        response = redirect("/")
        return cookie.set_cookie(response)

auth_bp.add_route(UserLoginView.as_view(), "/login")
