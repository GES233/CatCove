from sanic import Blueprint, Request, html
from sanic.response import HTTPResponse

from ....services.render import render_page_template

index_bp = Blueprint("index")
""" I'll using Markdown render to replace this. """

@index_bp.route("/")
async def index(request: Request) -> HTTPResponse:
    
    return html(render_page_template(
        "index.html",
        user=request.ctx.current_user
    ))


@index_bp.route("/about")
async def about(request: Request) -> HTTPResponse:
    return html(render_page_template(
        "about.html",
        role = "About",
        user=request.ctx.current_user
    ))


@index_bp.route("/help")
async def about(request: Request) -> HTTPResponse:
    return html(render_page_template(
        "markdown-demo.html",
        user=request.ctx.current_user
    ))