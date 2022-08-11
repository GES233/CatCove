from sanic import Blueprint

# Import your code here
api_endpoint = Blueprint("api_dev")

from ..response import code
from ..response import model2json
from ....models.schemas.response import APIResp

@api_endpoint.route("/", methods=["GET"], error_format="json")
async def hello_api(request):
    return model2json(APIResp(
        code=code.RETURNED_RESOURCE,
        info="SUCCESS",
        org="Hello API!"
    ))

from .endpoints.about import api_about

api_dev = Blueprint.group(
    api_endpoint,
    api_about,
    version=0.1,
    version_prefix="/api/v"
)
