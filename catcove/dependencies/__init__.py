from sanic import Sanic

# Some contexts.
from contextvars import ContextVar

_base_model_session_ctx = ContextVar("session")


def register_dependencies(app: Sanic) -> None:

    # Database

    # load session to request.
    from .db import async_session

    @app.on_request
    async def inject_session(request):
        request.ctx.db_session = async_session()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(
            request.ctx.db_session
        )

    @app.on_response
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.db_session.close()

    # Redis
    # ...

    # ...
