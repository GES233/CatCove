from sanic import Blueprint

from .auth import auth_v_0_1
from .user import user_v_0_1, sign_up_v_0_1

endpoint_v_0_1 = Blueprint.group(
    auth_v_0_1,
    user_v_0_1,
    sign_up_v_0_1,
    version=0.1
)
