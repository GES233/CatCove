from datetime import timedelta
from sanic import Blueprint, HTTPResponse, Request
from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sqlalchemy import or_, select

from catcove.model.tables import Users, UserPosts
from catcove.utils import schemasjson
from catcove.service.security import token_required
from catcove.model.schemas import return_6700
from catcove.api.utils import body2model_via_json

# ==== Routers ==== #

post_v_0_1 = Blueprint("api_v_0_1_post")

class UserPostView(HTTPResponse):

    async def get(request): ...

    async def post(request): ...

    async def delete(request): ...


class UserPostList(HTTPResponse):

    async def get(request): ...
