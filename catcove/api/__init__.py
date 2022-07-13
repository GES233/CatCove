from sanic import Blueprint
from .endpoints import endpoint_v_0_1

app_api = Blueprint.group(endpoint_v_0_1, version_prefix="/api/v")
