from sanic import Blueprint, json

from ....usecase.api import APIServise
from .helper import code as api_code
from .helper import info as api_info

index_bp = Blueprint("api_index", version=0.1)

@index_bp.route("/")
async def index(request):
    api = APIServise()
    return json(
        body = api.base_resp(
            code=api_code.RESOURCE_FETCHED_DEFAULT,
            info=api_info.OK,
            type="message",
            data="Hello, API."
        ).json(),
        dumps = lambda x: x
    )
