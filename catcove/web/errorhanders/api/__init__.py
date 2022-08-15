from sanic.errorpages import JSONRenderer
from sanic.response import HTTPResponse


class CustomJSONRenderer(JSONRenderer):
    def render(self) -> HTTPResponse:
        return super().render()
    
    def minimal(self) -> HTTPResponse:
        return super().minimal(self)
    
    def full(self) -> HTTPResponse:
        return super().minimal(self)
