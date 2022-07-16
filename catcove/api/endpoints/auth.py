from datetime import timedelta
from sanic import Blueprint, HTTPResponse, Request
from sanic_ext import openapi
from sqlalchemy import or_, select

from catcove.api.utils import body2model_via_json as body_to_model
from catcove.service.security import (
    get_token as generate_user_token,
    generate_refresh_token,
    get_refreshtoken_payload,
    get_user
)
from catcove.service.security.decorator import return_invalid
from catcove.model.schemas import (
    return_6700,
    TokenPrePayloadModel,
    UserLoginSchema
)
from catcove.model.tables import Users
from catcove.utils import schemasjson

# ==== Routers ==== #

auth_v_0_1 = Blueprint("api_v_0_1_auth")


@auth_v_0_1.get("/getToken")
@openapi.definition(
    description="get Token to cookie."
)
async def get_token(request: Request):
    """ Get Token: Get to token to access some sentitive and security data.
        
        ========
        reliable: login authentication(AuthRefreshToken).
            *: I moved give AuthRefreshToken to /login. 

        flowchart:
        1. check AuthRefreshToken.
        2. update AuthRefreshToken and AuthorizationToken if goted, else .
    """
    response: HTTPResponse = schemasjson(return_6700("成功获得令牌"))
    
    # refresh.
    if request.cookies.get("AuthRefreshToken") or response.cookies.get("AuthRefreshToken"):
        refresh_token = request.cookies.get("AuthRefreshToken")
        if not refresh_token:
            refresh_token = response.cookies.get("AuthRefreshToken")
        if not refresh_token: return schemasjson(return_invalid())
        payload = get_user(get_refreshtoken_payload(
            refresh_token,
            request.app.config.SECRET_KEY
        ))
        if not payload: return schemasjson(return_invalid())
        # Update refresh token.
        new_refresh_token = generate_refresh_token(
            data={
                "uid": payload.uid
            },
            key=request.app.config.SECRET_KEY,
            expire_time=timedelta(days=45))
        response.cookies["AuthRefreshToken"] = new_refresh_token
        response.cookies["AuthRefreshToken"]["httponly"] = True
        response.cookies["AuthRefreshToken"]["path"] = "/api/v0.1/"

        # Update new token.
        token = generate_user_token(
            data=TokenPrePayloadModel(
                uid=payload["uid"]
            ),
            key=request.app.config.SECRET_KEY
        )
        response.cookies["AuthorizationToken"] = token
        return response
    else:
        return schemasjson(return_invalid())


@auth_v_0_1.post("/login")
@openapi.definition(
    summary=" Login and get the token. "
)
async def login(request: Request):
    model = body_to_model(request, UserLoginSchema)
    if model == None:
        return schemasjson(return_invalid("请输入内容！"))
    nickname = model.nickname
    password = model.password
    # Query from DB.
    session = request.ctx.session
    async with session.begin():
        # Now, returned a `Users` instance instead of a primary key.
        sql = select(Users).where(
            or_(
                Users.nickname == nickname,
                Users.email == nickname,
                Users.username == nickname
            )
        )
        result = await session.execute(sql)
        data: Users | None = result.scalars().first()
        if not data:
            return schemasjson(return_invalid("宁是申必壬？"))
        session.expunge(data)
    
    if data.check_passwd(password) is False:
        return schemasjson(return_invalid("密码错了"))
    
    refresh_token = generate_refresh_token(
            data={
                "uid": data.id
            },
        key=request.app.config.SECRET_KEY,
        expire_time=timedelta(days=45))
    response.cookies["AuthRefreshToken"] = refresh_token
    response.cookies["AuthRefreshToken"]["httponly"] = True
    response.cookies["AuthRefreshToken"]["path"] = "/api/v0.1/"
    response = await get_token(request)
    return response
