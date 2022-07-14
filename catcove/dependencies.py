import click
import yaml
import os
from contextvars import ContextVar

from sanic import Sanic
from sanic.response import json

from catcove.model.schemas import (
    MessageBody,
    return_6700
)

app_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))

# ==== Configure ==== #

def padding_instance_file(instance_path: str):
    from mako.template import Template

    instance_template = Template(
        filename=f"{app_path}/catcove/setting/instance.yaml.mako",
        )
    click.secho("Generate SECRET_KEY ...")
    ssl_code = str(os.popen("openssl rand -base64 32").readline().strip('\n'))
    click.secho(f"SECRET_KEY:{ssl_code}")
    content = instance_template.render(openssl_key=ssl_code)
    file = open(f"{app_path}/{instance_path}", "x")
    file.write(content)



def load_config(app: Sanic, instance_path: str | None = None) -> None:
    """ Usage:
        >>> app = Sanic(__name__)
        >>> load_config(app)
            or
        >>> load_config(app, "instance.yaml")
    """
    if app.config["ENV"] == "dev" or app.config["ENV"] == "development":
        from setting.dev import DevelopmentConfig
        app.update_config(DevelopmentConfig)
    elif app.config["ENV"] == "test":
        from setting.test import TestConfig
        app.update_config(TestConfig)
    else:  # production
        from setting.pro import ProductionConfig
        app.update_config(ProductionConfig)
        if not instance_path:
            click.secho("[WARN]: In production enviorment, please use instence.yaml at root path.", fg="yellow")

    app.update_config({"APP_ROOT_PATH": app_path})

    if instance_path:
        if not os.path.exists(f"{app_path}/{instance_path}"):
            # os.makedirs(f"{app_path}/{instance_path}")
            padding_instance_file(instance_path)
        
        with open(f"{app_path}/{instance_path}") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        
        app.update_config(data)

# ==== Static file ==== #

def register_static(app: Sanic):

    # Static file at root path.
    app.static("/favicon.ico", f"{app_path}/static/favicon.ico")

# ==== Responce ==== #

about_content = [
"欢迎来到 `CatCove` ，这里是为了给某些拥有特定爱好的人（我们通常称其为「同好」\
，而「我们」特指网站管理员，恕下面不再对此添加方括号）交流相对私密的爱好而被设立\
的论坛。",
"由于用户的属性以及用户讨论内容的私密性，恕不对外人开放，我们对此感到非常抱歉。如\
果有异议或是对圈子有兴趣，请通过电邮与我联系。",
"如果您是圈内人（标志之一是了解我所说的这些「黑话」）的话，可以和已经成为 `CatCo\
ve` 成员的其他同好联系以获得邀请码。"
]

def register_basic_responce(app: Sanic):
    
    from catcove.model.schemas.content.anounce import AnouncementBody, Anouncement

    # Index responce: Hello world.
    @app.route("/")
    async def index(request):
        return json(body=return_6700(MessageBody(body="Hello World!")).dict())


    @app.route("/about")
    async def about(request):
        return json(return_6700(
            AnouncementBody(
                    body=Anouncement(title="关于🐱Cave",
                    author="administrator",
                    content=about_content
                )
            )
        ).dict())

# ==== Middleware ==== #

def register_middleware(app: Sanic):

    # === Database === #

    from catcove.db import async_sessoin

    _base_model_session_ctx = ContextVar("session")
    
    @app.on_request
    async def inject_session(request):
        request.ctx.session = async_sessoin()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)
    
    @app.on_response
    async def close_session(request, responce):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()
    
    # ==== UserLogin === #

    # Create after login or register.
    _current_user_ctx = ContextVar("current_user")
    
    # === UserToken === #

    ...

    # === CORS === #

    from catcove.service.cors import add_cors_headers
    from catcove.service.cors.options import setup_options

    app.register_listener(setup_options, "before_server_start")
    app.register_middleware(add_cors_headers, "response")

# ==== Routers ==== #

def register_routers(app: Sanic):
    from api import app_api as api_route

    app.blueprint(api_route)


