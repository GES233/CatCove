from datetime import datetime, timedelta
from sanic import Request
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView

from .....entities.tables.users import Users

from ..forms.user import SignUpForm, check_signup_form, common_nickname, common_email
from .....usecase.users import UserService
from .....usecase.auth import AuthService
from .....entities.schemas.user.request import SignUpModel
from .....services.render import render_page_template


class RegisterView(HTTPMethodView):
    def signup_render(self, form, **kwargs) -> HTTPResponse:
        return html(
            render_page_template(
                "account/signup.html", role="SignUp", form=form, **kwargs
            )
        )

    async def get(self, request: Request) -> HTTPResponse:
        return self.signup_render(
            SignUpForm(),
            user=request.ctx.current_user,
        )

    async def post(self, request: Request) -> HTTPResponse:
        # Check form firstly.
        form_data = request.form
        if not form_data:
            return self.signup_render(
                SignUpForm(),
                user=request.ctx.current_user,
            )

        temp_form = SignUpForm(
            data={
                "nickname": form_data.get("nickname"),
                "email": form_data.get("email"),
                "password": form_data.get("password"),
                "confirm": form_data.get("confirm"),
                "agree_policy": form_data.get("agree_policy"),
            }
        )
        model: SignUpModel = check_signup_form(temp_form)
        if isinstance(model, SignUpForm):
            return self.signup_render(
                model,
                user=request.ctx.current_user,
            )

        # Other check.
        # email, invitation code, etc.

        # Query.
        user_ser = UserService(db_session=request.ctx.db_session)

        common = await user_ser.check_common_user(
            nickname=model.nickname, email=model.email
        )

        if common:
            common_user = user_ser.user
            if (
                model.nickname == common_user.nickname
                or model.nickname == common_user.email
            ):
                return self.signup_render(
                    common_nickname(temp_form),
                    user=request.ctx.current_user,
                )
            elif model.email == common_user.email:
                return self.signup_render(
                    common_email(temp_form),
                    user=request.ctx.current_user,
                )
            else:
                return self.signup_render(
                    SignUpForm(),
                    user=request.ctx.current_user,
                )

        # Insert.
        newbie: Users = await user_ser.create_user(
            model.nickname, model.email, model.password
        )

        """
        # Redirect.
        if model.auto_login == True:
            # Add cookie.
            cookie = AuthService(exp=timedelta(days=14))
            cookie.gen_payload(newbie)
            _ = cookie.dict_to_str()
            _ = cookie.encrypt()
            # Return to index.
            response = redirect("/")
            return cookie.set_cookie(response)
        else:
            # Move the request.
            return redirect("/login")
        """

        # Add cookie.
        cookie = AuthService(exp=timedelta(days=14))
        cookie.gen_payload(newbie)
        _ = cookie.dict_to_str()
        _ = cookie.encrypt()
        # Return to index.
        response = redirect("/")
        return cookie.set_cookie(response)
