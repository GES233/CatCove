from sanic import Blueprint

user_bp = Blueprint("user")

from .signup import SignUpView
from .me import (
    return_me,
    freeze_account,
    delete_account,
    UserProfile
)

# SignUp.
user_bp.add_route(SignUpView.as_view(), "/signup")

# ME.
user_bp.add_route(return_me, "/me", methods=["POST"])
user_bp.add_route(freeze_account, "/me/freeze")
user_bp.add_route(UserProfile.as_view(), "/me/profile")
user_bp.add_route(delete_account, "/me/delete_account")
