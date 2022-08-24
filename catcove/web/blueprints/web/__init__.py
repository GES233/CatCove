from sanic import Blueprint

index_bp = Blueprint("index")

@index_bp.route("/")
async def index(request):
    from sanic.response import html
    from ....services.render import render_template
    return html(render_template("index.html"))

from .auth import auth_bp
from .user import user_bp

""" Render with Jinja2. """
views = Blueprint.group(
    index_bp,
    auth_bp,
    user_bp
)
# Add a middleware to parse the cookie.
# And render the result.
