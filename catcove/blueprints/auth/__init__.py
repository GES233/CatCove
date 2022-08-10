from sanic import Sanic, Blueprint, Request
from sanic.response import html, redirect
from sanic.views import HTTPMethodView
from jinja2.environment import Environment

auth_bp = Blueprint("auth")


class UserLoginView(HTTPMethodView):

    async def get(self, request: Request):

        # Render
        template: Environment = Sanic.get_app("Meow").ctx.template_env.get_template('login.html')
        html_content = template.render(role="Log in")
        return html(html_content)

    async def post(self, request: Request):
        print(request.form)
        
        # Business Logic.
        ...

        return redirect("/")

auth_bp.add_route(UserLoginView.as_view(), "/login")