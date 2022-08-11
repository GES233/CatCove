from sanic import Request
from sanic.response import (
    html,
    redirect,
    HTTPResponse,
    file, file_stream
)
from sanic.views import HTTPMethodView

from ...services.render import render_template
from ...models.tables.users import Users


async def return_me(request: Request) -> HTTPResponse:
    """ Return me. """
    ...
    return render_template("") 


class UserProfile(HTTPMethodView):
    """ User profile form. """
    async def get(request: Request) -> HTTPResponse:
        return render_template("")
    
    async def post(request: Request) -> HTTPResponse:
        return render_template("")


async def freeze_account(request: Request) -> HTTPResponse:
    """ User status => `freeze`. """
    ...
    return redirect("/logout")


async def delete_account(request: Request) -> HTTPResponse:
    ...
    return render_template("")
