from sanic import Sanic
from jinja2.environment import Template

def setup_templates(app: Sanic) -> None:
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


def render_page_template(template_name: str, **kwargs) -> str:
    # For "views" route.
    template: Template = Sanic.get_app("Meow").ctx.static_template_env.get_template(
        template_name
    )

    html_content = template.render(**kwargs)
    return html_content


def render_app_template(template_name: str, **kwargs) -> str:
    template: Template = Sanic.get_app("Meow").ctx.template_env.get_template(
        template_name
    )

    html_content = template.render(**kwargs)
    return html_content
