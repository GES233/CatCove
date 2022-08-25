from sanic import Blueprint

user_bp = Blueprint("user")

from .register import RegisterView
from .me import profile

user_bp.add_route(RegisterView.as_view(), "/signup")
user_bp.add_route(profile, "/me")
