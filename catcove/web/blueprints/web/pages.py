from sanic import Blueprint, Request, html
from sanic.response import HTTPResponse

from ....services.render import render_page_template

index_bp = Blueprint("index")
""" I'll using Markdown renderer to replace this. """


@index_bp.route("/")
async def index(request: Request) -> HTTPResponse:

    return html(render_page_template("index.html", user=request.ctx.current_user))


@index_bp.route("/about")
async def about(request: Request) -> HTTPResponse:
    return html(
        render_page_template("about.html", role="About", user=request.ctx.current_user)
    )


@index_bp.route("/help")
async def about(request: Request) -> HTTPResponse:
    return html(
        render_page_template("markdown-demo.html", title="Help About Markdown", user=request.ctx.current_user)
    )


@index_bp.route("/use-policy")
async def use_policy(request: Request) -> HTTPResponse:
    return html(
        render_page_template("use-policy.html", title="Read before signup", user=request.ctx.current_user)
    )
