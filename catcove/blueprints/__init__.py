from sanic import Blueprint

from .index import index_bp

views = Blueprint("views").group(
    index_bp
)