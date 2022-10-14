from datetime import timedelta
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic_ext import openapi

from ....entities.schemas.user import SignUpModel
from ....usecase.users import UserService
from ....usecase.auth import AuthService
from ....usecase.api import APIServise
from .helper import code, info

user_bp = Blueprint("api_user", version=0.1)


@user_bp.post("/signup")
@openapi.summary("Create a new user.")
async def register(request: Request) -> HTTPResponse:
    api = APIServise()

    # Please check password at front-end.
    data = request.json
    nickname = data["nickname"]
    email = data["email"]
    # register_code = data["register_code"]
    password = data["password"]

    model = SignUpModel(
        confirm=data["password"],
        **data,
    )

    user = UserService(request.ctx.db_session)

    common = await user.query_common_user(model.nickname, model.email)

    if common == True:
        # Construct and return error.
        ...

    # not common.
    _ = await user.create_user(
        nickname=model.nickname,
        email=model.email,
        password=model.password,
    )

    # Generate_token payload.
    token = AuthService(ser_type="token", exp=timedelta(days=30))
    _ = token.gen_payload(user.user)
    _ = token.dict_to_str()
    _ = token.encrypt(request.app.ctx.ecc_pri)

    # Return it.
    return json(
        api.base_resp(
            code.GET_TOKEN,
            info.OK,
            "Token",
            token.token
        ).json()
    )


@user_bp.route("/user/<int: id>")
@openapi.summary("Fetch user from id.")
async def user(request: Request, id: int) -> HTTPResponse:
    # 鉴权
    return json({"User": id})
