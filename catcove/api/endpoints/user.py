from sanic import Blueprint, HTTPResponse, Request
from sanic.views import HTTPMethodView
from sqlalchemy.sql import select, or_

from catcove.db import engine_bind
from catcove.db.curd import insert_data, simple_select
from catcove.model.schemas import (
    APIResponseBody,
    ErrorBody,
    return_6700,
    UserInfo,
    UserCreateInfo
)
from catcove.model.tables import Base, Users
from catcove.api.utils import schemasjson
from catcove.api.utils import body2model_via_json as body_to_model

user_v_0_1 = Blueprint("api_v_0_1_user", "/user")
sign_up_v_0_1 = Blueprint("api_v_0_1_signup")


class UserInfoView(HTTPMethodView):

    async def get(self, request, id):
        """ Get User: Return User profile.
            
            ========
            reliable:
            * Token
            * id (as a argument)

            flowchart:
            0. check token (at decorator)
            1. query user, return 404 if no result, else return info
        """
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
                    code=6401,
                    data="Not Found",
                    detail="查无此人"), 404)
    

    async def post(self, request, id):
        """ Modify: Change User's infomation.
            
            ========
            reliable:
            * Token, to get user's id and role.`
            * id (as a argument)

            flowchart: ...
        """
        ...
    

    async def delete(self, request, id):
        # delete information, not user.
        ...


class UserCreateView(HTTPMethodView):

    async def post(self, request: Request):
        """ Registration: Be a membership of website.
            
            ========
            reliable: nickname and password.

            flowchart:
            1. Is the form/json valid?
            2. Is the user existed? (if Yes)
            3. Add user or failed.
            4. End
        """
        # 1.
        data = body_to_model(request, UserCreateInfo)
        if isinstance(data, HTTPResponse):
            return data

        # 2.
        session: engine_bind = request.ctx.session
        async with session.begin():
            sql = select(Users).\
                where(
                    or_(
                        Users.nickname == data.nickname,
                        Users.username == data.nickname,
                        Users.email == data.email
                    )
                )
            user_common_name = await session.execute(sql)
            # Returned a user list or None.
            result = user_common_name.scalars().all()
        
        # 3.
        if result: return schemasjson(APIResponseBody(
            code=6250,
            data="Something happened.",
            detail=ErrorBody(
                body="你和别的用户重名了，改！"
            )), 400)  # Register failer -- common name.
        else:
            pre_register_user = Users(
                nickname=data.nickname,
                email=data.email
            )
            pre_register_user.encrypt_passwd(password=data.password)
            _ = await insert_data(request, data=pre_register_user)
            ...
            # 4.
            return schemasjson(return_6700(data="您已成功注册！"), 201)


user_v_0_1.add_route(UserInfoView.as_view(), "/<id>", version=0.1)
sign_up_v_0_1.add_route(UserCreateView.as_view(), "/sign_up", version=0.1)
