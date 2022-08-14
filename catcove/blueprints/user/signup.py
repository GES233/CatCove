from sanic import Request
from sanic.response import html, redirect
from sanic.views import HTTPMethodView


from ...services.security.cookie import generate_cookie, add_login_cookie
from ...services.render import render_template
from ...models.tables.users import Users
from ...models.forms.user import SignUpForm, check_signup_form, common_user_front
from ...business.user.signup import common_user_query, insert_user

def signup_render(form) -> HTTPMethodView:
        return html(
            body = render_template(
            'signup.html',
            role="Sign up",
            form=form)
        )


class SignUpView(HTTPMethodView):

    form = SignUpForm()

    async def get(self, request):
        return signup_render(self.form)
    
    async def post(self, request: Request):
        form_data = request.form
        if not form_data:
            # Bad request.
            return signup_render(self.form)

        temp_form = SignUpForm(data={
                "nickname": form_data.get("nickname"),
                "email": form_data.get("email"),
                "password": form_data.get("password"),
                "confirm": form_data.get("confirm"),
                "auto_login": form_data.get("auto_login")})
        model = check_signup_form(temp_form)
        if isinstance(model, SignUpForm):
            # Which field's error?
            return signup_render(model)
        # model: SignUpModel

        # InviteCode check.
        ...

        # Query.
        unique = await common_user_query(model, request.ctx.session)
        if not unique:
            # Common nickname.
            return signup_render(common_user_front(temp_form))
        
        # E-mail check.
        ...

        # Add.
        user: Users = await insert_user(model, request.ctx.session)

        # Add Cookie and redirect.
        auto_login: bool = temp_form.auto_login
        if auto_login == True:  # Not work yet.
            return add_login_cookie(redirect("/"), user)
        else:
            # NOT GET methos.
            return redirect("/login?from=sg")
