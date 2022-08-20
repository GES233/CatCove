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

    def login_render(self, form) -> HTTPResponse:
        return html(render_template(
            'auth/login.html',
            role="Login",
            form=form))

    async def get(self, request: Request):
        # Render
        return self.login_render(LoginForm())

    async def post(self, request: Request):
        # Submit -> POST
        form_data = request.form

        model: UserLoginModel = validate_login_form(LoginForm(data={
            "nickname": form_data.get("nickname"),
            "password": form_data.get("password")
        }))
        if isinstance(model, LoginForm):
            return self.login_render(model)

        cookie = AuthService()
        user_ser = UserService(request.ctx.db_session)
        
        user_exist = await user_ser.check_common_user(model.nickname, "")
        if user_exist != True:
            return self.login_render(
                user_not_exist(LoginForm()))
        else:
            password_match = user_ser.user.check_passwd(model.password)
            if password_match == False:
                return self.login_render(
                    password_not_match(LoginForm()))
        
        cookie.payload = user_ser.get_user_token()
        _ = cookie.dict_to_str()
        if _ == False:
            raise SanicException("Some error happend when generate token.")
        _ = cookie.encrypt()
        if _ == False:
            raise SanicException("Some error happend when generate token.")
        
        response = redirect("/")
        return cookie.set_cookie(response)

auth_bp.add_route(UserLoginView.as_view(), "/login")
