from sanic import Sanic


def register_services(app: Sanic) -> None:

    # CORS

    from ..services.cors import add_cors_headers
    from ..services.cors.options import setup_options

    app.register_listener(setup_options, "before_server_start")
    app.register_middleware(add_cors_headers, "response")

    # Render web content.

    from .render import setup_templates

    app.register_listener(setup_templates, "before_server_start")

    # Render Markdown to HTML.
    from .markdown import setup_md_renderer

    app.register_listener(setup_md_renderer, "before_server_start")

    # Key
    from .security.crypto import register_key

    register_key(app)
