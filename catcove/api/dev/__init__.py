from sanic import Blueprint

# Import your code here
api_endpoint = Blueprint("api_dev")

from ..response import code
from ..response import model2json
from ...models.schemas.responce import APIResp

@api_endpoint.route("/hello", methods=["GET"])
async def hello_api(request):
    return model2json(APIResp(
        code=code.RETURNED_RESOURCE,
        info="SUCCESS",
        org="Hello API!"
    ))

api_dev = Blueprint.group(
    api_endpoint,
    version=0.1,
    version_prefix="/api/v"
)
