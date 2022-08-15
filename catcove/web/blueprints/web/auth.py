from sanic import Blueprint, Request
from sanic.response import html, redirect, HTTPResponse
from sanic.views import HTTPMethodView

from ....services.render import render_template
from .forms.auth import (
    LoginForm,
    user_not_exist_front,
    password_not_match_front
)

auth_bp = Blueprint("auth")


class UserLoginView(HTTPMethodView):

    form = LoginForm()

    async def get(self, request: Request):
        # Render
        return self.login_render(self.form)

    async def post(self, request: Request):
        # Submit -> POST
        ...
    
    def login_render(self, form) -> HTTPResponse:
        return html(render_template(
            'auth/login.html',
            role="Login",
            form=form))
