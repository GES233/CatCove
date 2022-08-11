from sanic import Blueprint, Request
from sanic.response import html, redirect
from sanic.views import HTTPMethodView
from sanic.exceptions import MethodNotAllowed


from ...services.security.cookie import generate_cookie, add_login_cookie
from ...services.render import render_template
from ...models.forms.user import SignUpForm
from ...models.schemas.request import SignUpModel

def signup_render(form) -> HTTPMethodView:
        return html(render_template(
            'signup.html',
            role="Sign up",
            form=form))


class SignUpView(HTTPMethodView):

    async def get(self, request):
        return signup_render(form=SignUpForm())
    
    async def post(self, request): ...

