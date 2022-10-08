from sanic import Sanic


def register_stream(app: Sanic) -> None:
    if app.config.REDIS == True:
        from .stream import publisher_have_redis

        app.add_route(
            publisher_have_redis,
            "/subscribe",
            ["GET", "POST"],
            stream=True,
        )
    else:
        from .stream import publisher_no_redis

        app.add_route(
            publisher_no_redis,
            "/subscribe",
            ["GET", "POST"],
            stream=True,
        )
