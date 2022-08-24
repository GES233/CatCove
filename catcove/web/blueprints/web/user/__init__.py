from sanic import Blueprint

user_bp = Blueprint("user")

from .register import RegisterView

user_bp.add_route(RegisterView.as_view(), "/signup")
