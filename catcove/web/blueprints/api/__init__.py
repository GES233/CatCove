from sanic import Blueprint, Request

from ....usecase.auth import AuthService

from .index import index_bp as api_index_bp
from .auth import auth_bp as api_auth_bp

""" Return as API. """
api_bp = Blueprint.group(
    api_index_bp,
    api_auth_bp,
    version_prefix="/api/v",
)


@api_bp.middleware("request")
async def fetch_token(request: Request) -> None:
    request.ctx.token_ser = AuthService()

    ...
    request.ctx.current_user = ...
