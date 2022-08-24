from sanic import Blueprint, Request, html
from ....services.render import render_template

index_bp = Blueprint("index")

@index_bp.route("/")
async def index(request: Request):
    
    return html(render_template(
        "index.html",
        user=request.ctx.current_user
    ))
