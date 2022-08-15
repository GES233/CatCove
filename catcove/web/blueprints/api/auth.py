from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse

from ....usecase.users import UserService

auth_bp = Blueprint("auth", version=0.1)


@auth_bp.post("/login")
async def login(request: Request) -> HTTPResponse:
    # request json.
    data = request.json
    nickname = data["nickname"]
    password = data["password"]

    user = UserService()

    db_user = await user.check_common_user(nickname)
    
    if db_user != True:
        # User not exist.
        cause = user.service_status["error"]

        # Construct and return error.
        ...
    
    if user.user.check_passwd(password) != True:
        # Password error.
        cause = user.service_status["error"]

        # Construct and return error.
        ...
    
    # Generate_token payload.
    token_payload = user.get_user_token()

    # Encrypt token.
    ...

    # Return it.
    return ...
