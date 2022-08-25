from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse

from ....usecase.users import UserService
from ....usecase.auth import AuthService

auth_bp = Blueprint("auth", version=0.1)


@auth_bp.post("/login")
async def login(request: Request) -> HTTPResponse:
    # request json.
    data = request.json
    nickname = data["nickname"]
    password = data["password"]

    user = UserService(request.ctx.db_session)
    # Using `request.ctx.token_ser` to replace later.
    token = AuthService()

    user_exist = await user.check_common_user(nickname, None)
    
    if user_exist != True:
        ...
    
    password_match = user.user.check_passwd(password)
    if password_match == False:
        ...
    
    if user.user.check_passwd(password) != True:
        ...
    
    # Generate_token payload.
    token_payload = user.get_user_token()

    # Encrypt token.
    token.payload = token_payload
    _ = token.dict_to_str()
    if _ == False:
        # Payload not ready.

        # Return error.(500)
        ...
    else:
        _ = token.encrypt()
        if _ == False:
            # Return error.
            cause = token.service_status["error"]
            ...

    # Return it.
    return ...(token.token)
