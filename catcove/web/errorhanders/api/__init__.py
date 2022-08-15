from sanic.errorpages import JSONRenderer
from sanic.response import HTTPResponse

from ....entities.schemas.api import OriginContentModel
from ....services.render import render_api_resp
from ...blueprints.api.helper.code import SERVER_ERROR

class CustomJSONRenderer(JSONRenderer):
    def render(self) -> HTTPResponse:
        return super().render()
    
    def minimal(self) -> HTTPResponse:
        output = self._generate_output(full=False)
        return render_api_resp(
            body_code=SERVER_ERROR,
            body_info=output["message"],
            body_org=OriginContentModel(
                content_type="error",
                data={
                    "description": output["description"]
                }
            ),
            status=self.status)
    
    def full(self) -> HTTPResponse:
        output = self._generate_output(full=True)
        return render_api_resp(
            body_code=SERVER_ERROR,
            body_info=output["message"],
            body_org=OriginContentModel(
                content_type="error detail",
                data={
                    "description": output["description"],
                    "path": output["path"],
                    "args": output["args"],
                    "exceptions": output["exceptions"]
                }
            ),
            status=self.status)
