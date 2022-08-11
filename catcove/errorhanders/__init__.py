from sanic.handlers import ErrorHandler
from sanic.request import Request
from sanic.errorpages import (
    exception_response,
    BaseRenderer,
    TextRenderer,
    RENDERERS_BY_CONTENT_TYPE,
    CONTENT_TYPE_BY_RENDERERS,
    RENDERERS_BY_CONFIG

)
from sanic.response import HTTPResponse
from sanic.exceptions import BadRequest
import typing as t

from .render import HTMLRendererWithStyle
from .api import CustomJSONRenderer

class CostumErrorHander(ErrorHandler):

    def default(self, request, exception):
        self.log(request, exception)
        fallback = request.app.config.FALLBACK_ERROR_FORMAT
        return exception_response(
            request,
            exception,
            debug=self.debug,
            base=self.base,
            fallback=fallback,
        )


def exception_response(
    request: Request,
    exception: Exception,
    debug: bool,
    fallback: str,
    base: t.Type[BaseRenderer],
    renderer: t.Type[t.Optional[BaseRenderer]] = None,
) -> HTTPResponse:
    """
    Use custom Render.
    """
    content_type = None

    if not renderer:
        renderer = base
        render_format = fallback

        if request:
            if request.route:
                try:
                    if request.route.ctx.error_format:
                        render_format = request.route.ctx.error_format
                except AttributeError:
                    ...

            content_type = request.headers.getone("content-type", "").split(
                ";"
            )[0]

            acceptable = request.accept

            # If the format is auto still, make a guess
            if render_format == "auto":
                if acceptable and acceptable[0].match(
                    "text/html",
                    allow_type_wildcard=False,
                    allow_subtype_wildcard=False,
                ):
                    renderer = HTMLRendererWithStyle

                elif (
                    acceptable
                    and acceptable.match(
                        "application/json",
                        allow_type_wildcard=False,
                        allow_subtype_wildcard=False,
                    )
                    or content_type == "application/json"
                ):
                    renderer = CustomJSONRenderer

                elif not acceptable:
                    renderer = TextRenderer
                else:
                    try:
                        renderer = CustomJSONRenderer if request.json else base
                    except BadRequest:
                        renderer = base
            else:
                renderer = RENDERERS_BY_CONFIG.get(render_format, renderer)

            if acceptable:
                type_ = CONTENT_TYPE_BY_RENDERERS.get(renderer)  # type: ignore
                if type_ and type_ not in acceptable:
                    for accept in acceptable:
                        mtype = f"{accept.type_}/{accept.subtype}"
                        maybe = RENDERERS_BY_CONTENT_TYPE.get(mtype)
                        if maybe:
                            renderer = maybe
                            break
                    else:
                        renderer = base

    renderer = t.cast(t.Type[BaseRenderer], renderer)
    return renderer(request, exception, debug).render()

