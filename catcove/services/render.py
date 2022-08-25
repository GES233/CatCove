from sanic import Sanic
from jinja2.environment import Template


def render_page_template(template_name: str, **kwargs) -> str:
    # For "views" route.
    template: Template = Sanic.get_app("Meow").\
        ctx.static_template_env.get_template(template_name)
    
    html_content = template.render(**kwargs)
    return html_content


def render_app_template(template_name: str, **kwargs) -> str:
    template: Template = Sanic.get_app("Meow").\
        ctx.template_env.get_template(template_name)
    
    html_content = template.render(**kwargs)
    return html_content
