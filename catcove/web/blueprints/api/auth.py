from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json

from ....usecase.users import UserService
from ....usecase.auth import AuthService
from ....usecase.api import APIServise
from .helper import code as api_code
from .helper import info as api_info

auth_bp = Blueprint("auth", version=0.1)


@auth_bp.post("/login")
async def login(request: Request) -> HTTPResponse:
    api = APIServise()

    # request json.
    if not request.json:
        # Bad request.
        return json(
            body=api.base_resp(
                code=api_code.REQUEST_NO_JSON,
                info="Failer",
                type="message",
                data="No JSON updated.",
            ),
            status=400,
            dumps=lambda x: x,
        )
    data = request.json
    nickname = data["nickname"]
    password = data["password"]

    user = UserService(request.ctx.db_session)
    # Using `request.ctx.token_ser` to replace later.
    token = AuthService()

    user_exist = await user.check_common_user(nickname, None)

    if user_exist != True:
        return json(body=api.base_resp(...), status=404, dumps=lambda x: x)

    password_match = user.user.check_passwd(password)
    if password_match == False:
        return json(body=api.base_resp(...), status=401, dumps=lambda x: x)

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
