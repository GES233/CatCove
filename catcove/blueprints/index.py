from sanic import Blueprint
from sanic.request import Request
from sanic.response import html

from ..services.render import render_template

index_bp = Blueprint("index")

@index_bp.route("/", methods=["GET"])
async def index(request: Request):
    # Fetch user first.
    ...

    # Business Logic func.
    ...

    # Render template.
    html_content = await render_template("index.html", role="Index")

    return html(html_content)


@index_bp.route("/about")
async def about(request: Request):
    return html(
        body = await render_template("about.html", role="About")
    )


@index_bp.route("/md-help")
async def md_help(request: Request):
    return html(
        body = await render_template("markdown-demo.html", title="如何使用Markdown？")
    )
