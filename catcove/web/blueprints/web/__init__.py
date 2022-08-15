from sanic import Blueprint

index_bp = Blueprint("index")

@index_bp.route("/")
async def index(request):
    from sanic.response import html
    from ....services.render import render_template
    return html(render_template("index.html"))

""" Render with Jinja2. """
views = Blueprint.group(
    index_bp,
)
