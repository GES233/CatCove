from sanic.errorpages import HTMLRenderer, escape
from sanic.response import HTTPResponse, html

from ...services.render import render_template


class HTMLRendererWithStyle(HTMLRenderer):

    def minimal(self) -> HTTPResponse:
        return html(
            render_template(
                "errorpages/internal_error.html",
                title=self.title,
                error_text=self.text,
                error_body=self._generate_body(full=False)
            ),
            status=self.status,
            headers=self.headers
        )
    
    def full(self) -> HTTPResponse:
        return html(
            render_template(
                "errorpages/internal_error.html",
                title=self.title,
                error_text=self.text,
                error_body=self._generate_body(full=True)
            ),
            status=self.status,
            headers=self.headers
        )

