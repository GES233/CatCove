from sanic import Request
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView

from ..forms.user import SignUpForm
from .....entities.schemas.user.request import SignUpModel
from .....services.render import render_template

class RegisterView(HTTPMethodView):

    form = SignUpForm()

    def login_render(self, form) -> HTTPResponse:
        return html(render_template(
            'signup.html',
            role="SignUp",
            form=form))

    async def get(self, request: Request) -> HTTPResponse:
        return self.login_render(self.form)

    async def post(self, request: Request) -> HTTPResponse:
        ...
    