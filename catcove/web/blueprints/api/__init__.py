from sanic import Blueprint

from .index import index_bp as api_index_bp

""" Return as API. """
api_bp = Blueprint.group(api_index_bp, version_prefix="/api/v")
