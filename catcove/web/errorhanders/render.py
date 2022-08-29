import sys
from traceback import extract_tb

from sanic.errorpages import HTMLRenderer, escape
from sanic.response import HTTPResponse, html

from ...services.render import render_page_template


class HTMLRendererWithStyle(HTMLRenderer):
    """ Sanic HTMLRender with Pico.css. """

    TRACEBACK_LINE_HTML = (
        "<details>"
        "<summary><code>{0.line}</code></summary>"
        "<ul>"
        "<li>File <code>{0.filename}</code>, line <code><i>{0.lineno}</i></code>, "
        "in <code><b>{0.name}</b></code></li>"
        "<li><code>{0.line}</code></li>"
        "</ul>"
        "</details>"
    )
    TRACEBACK_BORDER = (
        "<p><b>"
        "The above exception was the direct cause of the following exception:"
        "</p></b>"
    )
    
    TRACEBACK_WRAPPER_HTML = (
        "<article>"
        "<header><code><b>{exc_name}</b></code> : {exc_value}</header>"
        "{frame_html}"
        "</article>"
    )
    
    def _generate_body(self, *, full):
        if full == False:
            return super()._generate_body(full=False)
        else:
            lines = []
            _, exc_value, __ = sys.exc_info()
            exceptions = []
            while exc_value:
                exceptions.append(self._format_exc(exc_value))
                exc_value = exc_value.__cause__

            traceback_html = self.TRACEBACK_BORDER.join(reversed(exceptions))
            appname = escape(self.request.app.name)
            name = escape(self.exception.__class__.__name__).replace(">", "&gt;")
            value = escape(self.exception).replace(">", "&gt;")
            path = escape(self.request.path)
            lines += [
                f"<h4>Traceback of {appname} " "(most recent call last):</h4>",
                f"{traceback_html}",
                "<footer><p>",
                f"<kbd>{name}</kbd> <b>: {value}</b> "
                f"while handling path <code>{path}</code>",
                "</footer>",
            ]

            for attr, display in (("context", True), ("extra", bool(full))):
                info = getattr(self.exception, attr, None)
                if info and display:
                    lines.append(self._generate_object_display(info, attr))

            return "\n".join(lines)
    
    def minimal(self) -> HTTPResponse:
        return html(
            render_page_template(
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
            render_page_template(
                "errorpages/internal_error.html",
                title=self.title,
                error_text=self.text,
                error_body=self._generate_body(full=True)
            ),
            status=self.status,
            headers=self.headers
        )

