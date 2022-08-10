from sanic import Blueprint, Sanic
from sanic.request import Request
from sanic.response import html
from jinja2.environment import Environment

index_bp = Blueprint("index")

@index_bp.route("/", methods=["GET"])
async def index(request: Request):
    # Fetch user first.
    ...

    # Business Logic func.
    ...

    # Render template.
    print(Sanic.get_app("Meow").ctx.template_env)
    template: Environment = Sanic.get_app("Meow").ctx.template_env.get_template('base.html')
    html_content = template.render(role="index")

    return html(html_content)
