from typing import Dict, Optional
from sanic import Sanic
from sanic.response import HTTPResponse, json
from ..entities.schemas.api import OriginContentModel
from jinja2.environment import Template


def render_template(template_name: str, **kwargs) -> str:
    template: Template = Sanic.get_app("Meow").\
        ctx.template_env.get_template(template_name)
    
    html_content = template.render(**kwargs)
    return html_content


def render_api_resp(
    body_code: int,
    body_info: str,
    body_org: OriginContentModel,
    status: int = 200,
    headers: Optional[Dict[str, str]] = None
) -> HTTPResponse:
    return json(
        {"code": body_code, "info": body_info, "origin": body_org.dict()},
        status,
        headers,
        content_type = "application/json"
    )
