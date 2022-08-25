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
            'account/login.html',
            role="Login",
            form=form))

    async def get(self, request: Request):
        # Render
        return self.login_render(LoginForm())

    async def post(self, request: Request):
        # Submit -> POST
        form_data = request.form
        if form_data.get("email") or \
            form_data.get("nickname") == "" or \
            form_data.get("password") == "":
            # Case: post from `/register`;`
            # Case: not updated value.
            return self.login_render(LoginForm())

        model: UserLoginModel = validate_login_form(LoginForm(data={
            "nickname": form_data.get("nickname"),
            "password": form_data.get("password"),
            # Add remember_me here.
        }))
        if isinstance(model, LoginForm):
            return self.login_render(model)

        # cookie = AuthService()
        user_ser = UserService(request.ctx.db_session)
        
        user_exist = await user_ser.check_common_user(model.nickname, None)
        if user_exist != True:
            return self.login_render(
                user_not_exist(LoginForm()))
        else:
            password_match = user_ser.user.check_passwd(model.password)
            if password_match == False:
                return self.login_render(
                    password_not_match(LoginForm()))
        
        _ = request.ctx.cookie_ser.gen_payload(user_ser.user)
        _ = request.ctx.cookie_ser.dict_to_str()
        if _ == False:
            raise SanicException("Some error happend when generate token.")
        _ = request.ctx.cookie_ser.encrypt()
        if _ == False:
            raise SanicException("Some error happend when generate token.")
        
        response = redirect("/")
        # Add remember_me code here.
        return request.ctx.cookie_ser.set_cookie(response)


async def logout(request: Request):
    # cookie = AuthService()
    # set cookie here.
    request.ctx.cookie_ser.cookie = request.cookies.get("UserMeta")

    if not request.ctx.cookie_ser.cookie:
        return redirect("https://www.bilibili.com")
    
    content = html(render_template("account/logout.html", title="Hope your back"))
    return request.ctx.cookie_ser.del_cookie(request, content)

auth_bp.add_route(UserLoginView.as_view(), "/login")
auth_bp.add_route(logout, "/logout")
