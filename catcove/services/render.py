from sanic import Sanic
from jinja2.environment import Template

async def render_template(template_name: str, **kwargs):
    template: Template = Sanic.get_app("Meow").\
        ctx.template_env.get_template(template_name)
    
    html_content = await template.render_async(**kwargs)
    return html_content
