from pydantic import ValidationError
from sanic import Blueprint, Request
from sanic.views import HTTPMethodView
from sanic.log import logger
from sanic.exceptions import BadRequest


from sqlalchemy.sql import select, or_

from catcove.model.schemas import return_6700
from catcove.model.schemas.users import UserInfo
from db import engine_bind
from db.curd import insert_data, simple_select
from model.schemas import APIResponseBody, MessageBody, ErrorBody
from model.schemas.users import UserCreateInfo
from model.tables import Base
from model.tables.users import Users
from service.security import token_required
from catcove.utils import schemasjson

user_v_0_1 = Blueprint("api_v_0_1_user", "/user")
sign_up_v_0_1 = Blueprint("api_v_0_1_signup")


class UserInfoView(HTTPMethodView):

    @token_required
    async def get(self, request, id):
        """ Return User infomation. """
        user = await simple_select(request, Users, id)
        if user:
            info = return_6700(
                data=(UserInfo(
                    id=user.id,
                    status=user.status,
                    nickname=user.nickname,
                    username=user.username,
                    gender=user.gender,
                    info=user.info,
                    join_time=user.join_time)))
            return schemasjson(info)
        else:
            return schemasjson(
                APIResponseBody(
                    code=6000,
                    data="Not Found",
                    detail="查无此人"), 404)
    
    @token_required
    async def post(self, request, id):
        ...
    
    @token_required
    async def delete(self, request, id):
        # delete information, not user.
        ...


class UserCreateView(HTTPMethodView):

    async def post(self, request: Request):
        try:
            # in Windows:
            # curl -Uri "Addr" -Method Post -Body '{...}'
            if not request.json:
                # Still return 400 if can not parse json.
                return schemasjson(APIResponseBody(
                    code=4700,
                    data="Bad request",
                    detail=MessageBody(body="Login data required")
                ), 400)
            
            raw_data = request.json
            
            data = UserCreateInfo(
                nickname = raw_data["nickname"],
                email = raw_data["email"],
                password = raw_data["password"],
                confirm_password = raw_data["confirm_password"])
            print(data)
        except BadRequest:
            # Will replece it.
            # Using custome Exception later.
            return schemasjson(APIResponseBody(
                code=0000,
                data="Error when process register form.",
                detail=MessageBody(
                    body="JSON解析错误"
                )), 500)
        except:
            logger.info("Some error occerd when registration.")
            return schemasjson(APIResponseBody(
                code=0000,
                data="Error when process register form.",
                detail=MessageBody(
                    body=""
                )), 500)
        else:
            # Data's ok.
            # Query the invication code firstly.
            session: engine_bind = request.ctx.session
            async with session.begin():
            # Fxxk sqlalchemy.
                users = Base.metadata.tables["users"]
                sql = select(users.c["id"]).\
                    where(
                        or_(
                            users.c["nickname"] == data.nickname,
                            users.c["email"] == data.nickname,
                            users.c["username"] == data.nickname,
                            users.c["email"] == data.email
                        )
                    )
                user_common_name = await session.execute(sql)
                # Returned a user list or None.
                result = user_common_name.scalars().all()
            if result: return schemasjson(APIResponseBody(
                code=0000,
                data="Error when process login form.",
                detail=ErrorBody(
                    body="你和别人重名了，改！"
                )), 400)  # Register failer -- common name.
            else:
                pre_register_user = Users(
                    nickname=data.nickname,
                    email=data.email
                )
                pre_register_user.encrypt_passwd(password=data.password)
                _ = await insert_data(request, data=pre_register_user)
                ...
                return schemasjson(return_6700(data="您已成功注册！"), 201)


user_v_0_1.add_route(UserInfoView.as_view(), "/<id>", version=0.1)
sign_up_v_0_1.add_route(UserCreateView.as_view(), "/sign_up", version=0.1)
