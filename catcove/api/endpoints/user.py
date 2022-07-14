from pydantic import ValidationError
from sanic import Blueprint, Request
from sanic.views import HTTPMethodView


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
            join_time=user.join_time
            )))
            return schemasjson(info)
        else:
            return schemasjson(
                APIResponseBody(
                    code=6000,
                    data="Not Found",
                    detail="查无此人"
                ), 404
            )
    
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
            raw_data = request.json
            data = UserCreateInfo(
                nickname = raw_data["nickname"],
                email = raw_data["email"],
                password = raw_data["password"],
                confirm_password = raw_data["confirm_password"])
            print(data)
        except KeyError as lose_data:
            ...
            return schemasjson(APIResponseBody(
                code=0000,
                data="Error when process login form.",
                detail=MessageBody(
                    body=str(lose_data)
                )), 500)
        except TypeError as internal_error:
            ...
            return schemasjson(APIResponseBody(
                code=0000,
                data="Error when process login form.",
                detail=MessageBody(
                    body=str(internal_error)
                )), 500)
        except ValidationError as format_error:
            ...
            return schemasjson(APIResponseBody(
                code=0000,
                data="Error when process login form.",
                detail=ErrorBody(
                    body=format_error.errors()
                )), 400)
        else:
            # Data's ok.
            # Query the invication code firstly.
            ...
            session: engine_bind = request.ctx.session
            async with session.begin():
            # Fxxk sqlalchemy.
                users = Base.metadata.tables["users"]
                sql = select(users.c["id"]).\
                    where(
                        or_(
                            users.c["nickname"] == data.nickname,
                            users.c["email"] == data.nickname,
                            # users.c["username"] == data.nickname
                        )
                    )
                # Returned a user list or None.
                user_common_name = await session.execute(sql)
                result = user_common_name.scalars().all()
            if result: return schemasjson(APIResponseBody(
                code=0000,
                data="Error when process login form.",
                detail=ErrorBody(
                    body=f"Have the same name with {result}."
                )), 400)  # Register failer -- common name.
            else:
                pre_register_user = Users(
                    nickname=data.nickname,
                    email=data.email
                )
                pre_register_user.encrypt_passwd(password=data.password)
                _ = await insert_data(request, data=pre_register_user)
                # add request.conn_info.ctx.current_user.
                ...
                # bug: sanic.exceptions.ServerError: 
                # Invalid response type <Response 237 bytes [302 FOUND]> (need HTTPResponse)
                return schemasjson(return_6700(data="您已成功注册！"), 201)  # redirect("/api/v0.1/getRefreshToken", )


user_v_0_1.add_route(UserInfoView.as_view(), "/<id>", version=0.1)
sign_up_v_0_1.add_route(UserCreateView.as_view(), "/sign_up", version=0.1)
