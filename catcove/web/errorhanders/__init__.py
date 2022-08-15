from sanic import Request, Sanic
from sanic.handlers import ErrorHandler
from sanic.errorpages import exception_response
import re

from .render import HTMLRendererWithStyle
from .api import CustomJSONRenderer

class CostumErrorHander(ErrorHandler):

    def default(self, request: Request, exception: Exception):
        self.log(request, exception)
        fallback = request.app.config.FALLBACK_ERROR_FORMAT
        url = request.path
        '''if re.match(r"/api", url):  # from api
            return exception_response(
                request,
                exception,
                debug=self.debug,
                base=self.base,
                fallback=fallback,
                renderer=CustomJSONRenderer
            )
        else:'''
        if True:
            return exception_response(
                request,
                exception,
                debug=self.debug,
                base=self.base,
                fallback=fallback,
                renderer=HTMLRendererWithStyle
            )


def custom_error(app: Sanic) -> None:
    # Custom errorhander.
    from ..errorhanders import CostumErrorHander
    app.error_handler = CostumErrorHander()

