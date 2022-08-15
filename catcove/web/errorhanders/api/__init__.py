from sanic.errorpages import JSONRenderer
from sanic.response import HTTPResponse

from ....models.schemas.exceptions import SanicJSONErrorModel
from ...blueprints.api.response import model2json


class CustomJSONRenderer(JSONRenderer):
    def render(self) -> HTTPResponse:
        return super().render()
    
    def minimal(self) -> HTTPResponse:
        return model2json(
            body=...,
            status=self.status,
            headers=self.headers
        )
    
    def full(self) -> HTTPResponse:
        return model2json(
            body=...,
            status=self.status,
            headers=self.headers
        )
