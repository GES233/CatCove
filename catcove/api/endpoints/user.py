import pprint
from pydantic import ValidationError
from sanic import Blueprint, Request
from sanic.views import HTTPMethodView
from sanic.response import json

from json import loads

from sqlalchemy.future import select

from ...db.curd import simple_select
from ...model.schemas import APIResponseBody, MessageBody, ErrorBody
from ...model.schemas.users import UserCreateInfo
from ...model.tables.users import Users
from ...service.security import token_required

user_v_0_1 = Blueprint(__name__, "/user")
sign_up_v_0_1 = Blueprint("signup")


class UserInfoView(HTTPMethodView):

    @token_required
    async def get(self, request, id):
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
                confirm_password = raw_data["confirm_password"]
            )
        except TypeError as internal_error:
            pprint.pprint(internal_error.with_traceback)
            return json(
                APIResponseBody(
                    code=0000,
                    data="Error when process login form.",
                    detail=MessageBody(
                        body=str(internal_error)
                    )
                ).dict(), 500
            )
        except ValidationError as format_error:
            ...
            return json(
                APIResponseBody(
                    code=0000,
                    data="Error when process login form.",
                    detail=ErrorBody(
                        body=format_error.errors()
                    )
                ).dict(), 400
            )
        ...

        # Data's ok.
        # Query the invication code firstly.
        ...
        session = request.ctx.session
        async with session.begin():
            # `sql`
            # SELECT id FROM users
            # WHERE users.nickname = {username}
            # ...
            sql = select(Users).where()

user_v_0_1.add_route(UserInfoView.as_view(), "/<id>", version=0.1)
sign_up_v_0_1.add_route(UserCreateView.as_view(), version=0.1)
