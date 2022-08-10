from sanic import Blueprint

from ...response import model2json, code
from .....models.schemas.response import APIResp
from .....business.about import about_model

api_about = Blueprint("about")

@api_about.route("/about")
async def about(request):
    return model2json(
        body=APIResp(
            code=code.RETURNED_RESOURCE,
            info="SUCCESS",
            org=about_model()
        )
    )