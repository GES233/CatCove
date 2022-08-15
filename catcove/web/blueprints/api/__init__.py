from sanic import Blueprint

from .index import index_bp

""" Return as API. """
api = Blueprint.group(
    index_bp,
    version_prefix="/api/v"
)
