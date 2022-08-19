from sanic import Request
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView

from catcove.entities.tables.users import Users

from ..forms.user import (
    SignUpForm,
    check_signup_form,
    common_user
)
from .....usecase.users import UserService
from .....entities.schemas.user.request import SignUpModel
from .....services.render import render_template

class RegisterView(HTTPMethodView):

    form = SignUpForm()

    def signup_render(self, form) -> HTTPResponse:
        return html(render_template(
            'signup.html',
            role="SignUp",
            form=form))

    async def get(self, request: Request) -> HTTPResponse:
        return self.signup_render(self.form)

    async def post(self, request: Request) -> HTTPResponse:
        # Check form firstly.
        form_data = request.form
        if not form_data:
            return self.signup_render(self.form)

        temp_form = SignUpForm(data={
                "nickname": form_data.get("nickname"),
                "email": form_data.get("email"),
                "password": form_data.get("password"),
                "confirm": form_data.get("confirm"),
                "auto_login": form_data.get("auto_login")}
        )
        model: SignUpModel = check_signup_form(temp_form)
        if isinstance(model, SignUpForm): return self.signup_render(model)

        # Other check.
        # email, invitation code, etc.

        # Query.
        user_ser = UserService(db_session=request.ctx.db_session)
        
        common = await user_ser.check_common_user(nickname=model.nickname)

        if common: return self.signup_render(
            common_user(self.form))

        # Insert.
        newbie = await user_ser.create_user(
            model.nickname,
            model.email,
            model.password
        )

        print(newbie)

        # Add cookie.
        # ...

        # Redirect.
        return redirect("/")
    