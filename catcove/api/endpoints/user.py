import pprint
from flask import redirect
from pydantic import ValidationError
from sanic import Blueprint, Request
from sanic.views import HTTPMethodView
from sanic.response import json

from json import loads

from sqlalchemy.sql import select, or_

from db import engine_bind
from db.curd import insert_data
from model.schemas import APIResponseBody, MessageBody, ErrorBody
from model.schemas.users import UserCreateInfo
from model.tables import Base
from model.tables.users import Users
from service.security import token_required

user_v_0_1 = Blueprint("api_v_0_1_user", "/user")
sign_up_v_0_1 = Blueprint("signup", "/")


class UserInfoView(HTTPMethodView):

    @token_required
    async def get(self, request, id):
        """ Return User infomation. """
        ...
    
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
            raw_data = loads(request.json)
            data = UserCreateInfo(
                nickname = raw_data["nickname"],
                email = raw_data["email"],
                password = raw_data["password"],
                confirm_password = raw_data["confirm_password"])
        except TypeError as internal_error:
            ...
            return json(APIResponseBody(
                code=0000,
                data="Error when process login form.",
                detail=MessageBody(
                    body=str(internal_error)
                )).dict(), 500)
        except ValidationError as format_error:
            ...
            return json(APIResponseBody(
                code=0000,
                data="Error when process login form.",
                detail=ErrorBody(
                    body=format_error.errors()
                )).dict(), 400)
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
                            # users.c["username"] == data.username
                        )
                    )
                user_common_name = await session.execute(sql)
                result = user_common_name.scalars()
                session.expunge(result) if result else ...
        
            if not result: return json()  # Register failer -- common name.
            else:
                pre_register_user = Users(
                    nickname=data.nickname,
                    email=data.email
                )
                pre_register_user.encrypt_passwd(data.password)
                user = await insert_data(request, data=pre_register_user)
                # add request.conn_info.ctx.current_user.
                ...
                return redirect("/api/v0.1/getRefreshToken")


user_v_0_1.add_route(UserInfoView.as_view(), "/<id>", version=0.1)
sign_up_v_0_1.add_route(UserCreateView.as_view(), "/sign_up", version=0.1)
