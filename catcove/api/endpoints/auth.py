from datetime import timedelta
from sanic import Blueprint, Request
from sanic.response import json
from sanic_ext import openapi

from catcove.service.security import (
    get_token,
    check_token,
    token_required
)
from catcove.model.schemas import (
    APIResponseBody,
    MessageBody,
    return_6700
)
from catcove.model.schemas.users import UserInfo, UserLoginSchema
from catcove.model.tables.users import Users

# ==== Routers ==== #

auth_v_0_1 = Blueprint("api_v_0_1_auth")

@auth_v_0_1.get("/getUserToken")
async def get_user_token(request: Request):
    # `/api/v1/getUserToken`
    if request.headers.getone("X-Auth-RefreshToken", None):
        refresh_token_info = check_token(
            request.headers.get("X-Auth-RefreshToken", None),
            request.app.config.SECRET,
            "r"
        )
        if refresh_token_info != 0:
            # if refresh token expired or invalid:
            return json(
                APIResponseBody(
                    code=4500,
                    data="UNAUTHORIZED",
                    detail=MessageBody(
                    body="您太久没登录了，需要重新登录"
                    )
                    ).dict(), 401
                )
        else:
            request.headers.update(token = f"Authorization: Token {get_token()}")
            return json(return_6700("当当当当！新的令牌已备好！！").dict(), 201)
    else:
        return json(
                APIResponseBody(
                    code=4500,
                    data="UNAUTHORIZED",
                    detail=MessageBody(
                    body="您太久没登录了，需要重新登录"
                    )
                    ).dict(), 401
                )


@auth_v_0_1.get("/getRefreshToken")
async def get_refresh_token(request: Request):
    if not hasattr(request.conn_info.ctx, "current_user"):
        # need login.
        return json(APIResponseBody(
            code=4500,
            data="UNAUTHORIZED",
            detail=MessageBody(
                body="您太久没登录了，需要重新登录"
            )
        ).dict(), 401)
    
    uid = request.conn_info.ctx.current_user.id

    if request.conn_info.ctx.current_user.is_spectator:
        role = "spectator"
    else:
        role = "normal"
    
    token = get_token(
        data={
            "uid": uid,
            "role": role
        },
        key=request.app.config.SECRET_KEY,
        expire_time=timedelta(days=45),
        sign=False  # Using encrypt.
    )
    request.headers.add("X-Auth-RefreshToken", token)
    del request.conn_info.ctx.current_user
    return json(return_6700("New User Token generated.").dict(), 201)

@auth_v_0_1.post("/login")
@openapi.definition(
    summary=" Login and get the token. "
    )
async def login(request: Request):
    ...
    if not hasattr(request.conn_info.ctx, "current_user"):
        request.conn_info.ctx.current_user = ...
