from sanic import Blueprint

index_bp = Blueprint("index", version=0.1)

@index_bp.route("/")
async def index(request):
    from ....entities.schemas.api import OriginContentModel
    from ....services.render import render_api_resp
    from .helper import code as api_code
    return render_api_resp(
        api_code.RESOURCE_FETCHED_DEFAULT,
        "OK",
        OriginContentModel(
            content_type="Test", data="All's OK."
        )
    )
