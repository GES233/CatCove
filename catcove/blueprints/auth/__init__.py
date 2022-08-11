from sanic import Blueprint, Request
from sanic.response import html, redirect
from sanic.views import HTTPMethodView

from ...business.auth import form2model, login_authentication_logic
from ...models.schemas.request import UserLoginModel
from ...services.render import render_template

auth_bp = Blueprint("auth")


class UserLoginView(HTTPMethodView):

    async def get(self, request: Request):

        # Render
        html_content = render_template('login.html', role="Login")
        return html(html_content)

    async def post(self, request: Request):
        # Submit -> POST

        # Initial work.
        model = form2model(request)

        # Check here.
        if not isinstance(model, UserLoginModel):
            # The instance may change.
            return model
        
        # Business Logic.
        if login_authentication_logic(model):
            # Set-cookie.
            ...
            return redirect("/")
        else:
            # 查无此人/密码错误
            # Re-render.
            html_content = render_template('login.html', role="Login")
            return html(html_content)
        # return self.get(request)

@auth_bp.route("/logout", methods=["GET"])
async def log_out(request):
    # Delete Cookie.
    ...
    
    # Redirect to index.
    return redirect("https://bilibili.com")

auth_bp.add_route(UserLoginView.as_view(), "/login")