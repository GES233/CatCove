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
    html_content = render_template("index.html", role="Index")

    return html(html_content)
