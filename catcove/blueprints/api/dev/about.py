from sanic import Blueprint

from ..response import model2json
from ..response import code
from ....models.schemas.response import APIResp, OriginData
from ....business.about import about_model

api_about = Blueprint("about")

@api_about.route("/about")
async def about(request):
    print(about_model())
    return model2json(
        body=APIResp(
            code=code.RETURNED_RESOURCE,
            info="SUCCESS",
            org=about_model()
        )
    )