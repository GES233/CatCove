from sanic import Blueprint

from .index import index_bp
from .auth import auth_bp
from .user import user_bp

views = Blueprint("views").group(
    index_bp,
    auth_bp,
    user_bp
)