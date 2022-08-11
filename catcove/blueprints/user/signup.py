from sanic import Blueprint, Request
from sanic.response import html, redirect
from sanic.views import HTTPMethodView
from sanic.exceptions import MethodNotAllowed


from ...services.security.cookie import generate_cookie, add_login_cookie
from ...services.render import render_template
from ...models.tables.users import Users
from ...models.forms.user import SignUpForm, check_signup_form
from ...business.user.signup import common_user_query, insert_user

def signup_render(form) -> HTTPMethodView:
        return html(render_template(
            'signup.html',
            role="Sign up",
            form=form))


class SignUpView(HTTPMethodView):

    async def get(self, request):
        return signup_render(SignUpForm())
    
    async def post(self, request: Request):
        form_data = request.form
        if not form_data:
            # Bad request.
            return signup_render(SignUpForm())

        model = check_signup_form(form_data)
        if isinstance(model, SignUpForm):
            # Which field's error?
            return signup_render(model)
        # model: SignUpModel

        # InviteCode check.
        ...

        # Query.
        unique = await common_user_query(model)
        if not unique:
            # Common nickname.
            return signup_render()
        
        # E-mail check.
        ...

        # Add.
        user: Users = await insert_user(model)

        # Add Cookie and redirect.
        auto_login: bool = model.auto_login
        if auto_login:
            return add_login_cookie(redirect("/"), user)
        else:
            return redirect("/login")
