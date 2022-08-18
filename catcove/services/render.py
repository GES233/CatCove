from sanic import Sanic
from jinja2.environment import Template


def render_template(template_name: str, **kwargs) -> str:
    template: Template = Sanic.get_app("Meow").\
        ctx.template_env.get_template(template_name)
    
    html_content = template.render(**kwargs)
    return html_content
