from datetime import timedelta
from sanic import Blueprint, HTTPResponse, Request
from sanic.response import redirect
from sanic_ext import openapi

from catcove.utils import schemasjson
from catcove.service.security import (
    get_token as generate_user_token,
    generate_refresh_token,
    get_refreshtoken_payload,
    get_token_payload,
)
from catcove.service.security.decorator import return_invalid
from catcove.model.schemas import (
    APIResponseBody,
    MessageBody,
    return_6700
)

# ==== Routers ==== #

auth_v_0_1 = Blueprint("api_v_0_1_auth")


@auth_v_0_1.get("/getToken")
async def get_token(request: Request):
    response: HTTPResponse = schemasjson(return_6700())
    if request.args.get("type") != "refresh":
        # Login required.
        if not ...:
            return schemasjson(return_invalid())
        ...
        refresh_token = generate_refresh_token(
            data=...,
            key=request.app.config.SECRET_KEY,
            expire_time=timedelta(days=45))
        response.cookies["AuthRefreshToken"] = refresh_token
        response.cookies["AuthRefreshToken"]["httponly"] = True
        response.cookies["AuthRefreshToken"]["path"] = "/api/v0.1/"
    
    # refresh.
    if request.cookies.get("AuthRefreshToken") or response.cookies.get("AuthRefreshToken"):
        token = generate_user_token(
            data=...,
            key=request.app.config.SECRET_KEY
        )
        response.cookies["AuthorizationToken"] = token
    else:
        return schemasjson(return_invalid())
        # search_for login auth.
    return schemasjson(return_invalid())


@auth_v_0_1.post("/login")
@openapi.definition(
    summary=" Login and get the token. "
    )
async def login(request: Request):
    if request.body == None:
        return schemasjson(APIResponseBody(
            code=4700,
            data="Bad request",
            detail=MessageBody(body="Login data required")
        ))
    ...
    if not hasattr(request.conn_info.ctx, "current_user"):
        request.conn_info.ctx.current_user = ...
    ...
    # return redirect("/api/v0.1/auth/getRefrashToken", content_type="application/json")
