from sanic import Sanic

# Some contexts.
from contextvars import ContextVar

_base_model_session_ctx = ContextVar("session")


def register_service(app: Sanic) -> None:

    # CORS

    from .services.cors import add_cors_headers
    from .services.cors.options import setup_options

    app.register_listener(setup_options, "before_server_start")
    app.register_middleware(add_cors_headers, "response")

    # Database

    # load session to request.
    from .db import async_session

    @app.on_request
    async def inject_session(request):
        request.ctx.session = async_session()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)
    
    @app.on_response
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()
    
    # Render

    @app.listener("before_server_start")
    async def setup_templates(app: Sanic):
        from pathlib import Path, PurePath
        from jinja2 import (
            Environment,
            FileSystemLoader
        )

        template_path = PurePath( Path(__file__).cwd() / "templates")

        app.ctx.template_env = Environment(
            loader=FileSystemLoader(template_path),
        )

        # Globlas functions:

        # app.ctx.template_env.globals["..."] = ...

        # - user check with cookie.
    
    # Key
    # from .services.security.crypto import ...


def load_static(app: Sanic) -> None:

    from pathlib import Path, PurePath

    app_path = Path(__file__).cwd()

    favicon_path = PurePath( app_path / "static/img/favicon.ico")
    robots_path = PurePath( app_path / "static/robots.txt")
    css_path = PurePath( app_path / "static/css/")
    js_path = PurePath( app_path / "static/js/")
    static_img_path = PurePath( app_path / "static/img/")


    app.static("/favicon.ico", favicon_path)
    app.static("/robots.txt", robots_path)
    app.static("/static/css", css_path)
    app.static("/static/js", js_path)
    app.static("/static/img", static_img_path)


def custom_error(app: Sanic) -> None:
    # Custom errorhander.
    from .errorhanders import CostumErrorHander
    app.error_handler = CostumErrorHander()
