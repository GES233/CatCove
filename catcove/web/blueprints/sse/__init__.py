from sanic import Sanic

def register_stream(app: Sanic) -> None:
    if app.config.REDIS == True:
        ...
    else:
        ...
