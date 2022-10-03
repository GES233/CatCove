from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, redirect
from sanic_ext import openapi

from ....usecase.users import UserService

user_bp = Blueprint("user", version=0.1)


@user_bp.post("/signup")
@openapi.summary("Create a new user.")
async def register(request: Request) -> HTTPResponse:

    # Please check password at front.
    data = request.json
    nickname = data["nickname"]
    email = data["email"]
    register_code = data["register_code"]
    password = data["password"]

    user = UserService()

    common_email = await user.check_common_user(email)
    common_nickname = await user.check_common_user(nickname)

    if common_email == True:
        # Construct and return error.
        ...
    elif common_nickname == True:
        # Construct and return error.
        ...

    # not common.
    _ = await user.create_user(password)

    # Generate_token payload.
    token_payload = user.get_user_token()

    # Encrypt token, zip into cookie.
    ...

    # Return it.
    return redirect()
