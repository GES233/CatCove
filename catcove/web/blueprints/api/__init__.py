from sanic import Blueprint, Request
from datetime import datetime

from ....usecase.auth import AuthService

from .index import index_bp as api_index_bp
from .auth import auth_bp as api_auth_bp
from .user import user_bp as api_user_bp

""" Return as API. """
api_bp = Blueprint.group(
    api_index_bp,
    api_auth_bp,
    api_user_bp,
    version_prefix="/api/v",
)


@api_bp.middleware("request")
async def fetch_token(request: Request) -> None:
    request.ctx.token_ser = AuthService(ser_type="token")
    if not request.headers.get(request.ctx.token_ser.auth_type["token"]):
        request.ctx.current_user = None
    else:
        request.ctx.token_ser.token = request.headers.get(request.ctx.token_ser.auth_type["token"])
        de_token = request.ctx.token_ser.decrypt(request.app.ctx.ecc_pub)
        if de_token == True:
            _payload = request.ctx.token_ser.payload
            if _payload["exp"] < datetime.timestamp(datetime.utcnow()):
                    request.ctx.current_user = None
            else:
                # Query from Redis if have.
                ...

                request.ctx.current_user = request.ctx.token_ser.payload
        else:
            request.ctx.current_user = None
            request.ctx.token_ser = AuthService()
