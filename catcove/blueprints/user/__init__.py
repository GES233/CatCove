from sanic import Blueprint

user_bp = Blueprint("user")

from .signup import SignUpView

user_bp.add_route(SignUpView.as_view(), "/signup")
