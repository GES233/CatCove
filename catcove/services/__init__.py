from sanic import Sanic


def register_services(app: Sanic) -> None:

    # CORS

    from ..services.cors import add_cors_headers
    from ..services.cors.options import setup_options

    app.register_listener(setup_options, "before_server_start")
    app.register_middleware(add_cors_headers, "response")

    # Render

    async def setup_templates(app: Sanic):
        from pathlib import Path, PurePath
        from jinja2 import Environment, FileSystemLoader

        static_template_path = PurePath(
            Path(__file__).cwd() / "catcove/web/blueprints/web/templates"
        )

        app.ctx.static_template_env = Environment(
            loader=FileSystemLoader(static_template_path)
        )

        # Globlas functions:
        # app.ctx.template_env.globals["..."] = ...

        # - user check with cookie.

    app.register_listener(setup_templates, "before_server_start")

    # Key
    from .security.crypto import register_key

    register_key(app)
