from sanic import Sanic
from pathlib import Path
import yaml
import os

from .dev import DevConfig
from .test import TestConfig
from .pro import ProConfig


def padding_instance(app: Sanic, **other_settings) -> None:
    # set path.
    PRJ_PATH = Path(__file__).cwd()

    instance_path = Path(PRJ_PATH / "instance")
    config_yaml = Path(instance_path/"config.yml")
    
    
    # Folder.
    if not instance_path.is_dir():
        # Create a new folder.
        instance_path.mkdir()

        # Create_Key file.
        os.popen(f"cd {instance_path} && \
            openssl ecparam -genkey -noout -name prime256v1 -out eckey.pem -text && \
            openssl ec -in eckey.pem -pubout -out ecpubkey.pem")

    # ====

    from mako.template import Template
    
    template = Template(filename=f"{PRJ_PATH}/catcove/settings/config.yaml.mako")
    
    # SECRET: $ openssl rand -base64 32
    str_key = (os.popen("openssl rand -base64 32").readline().strip("\n"))
    instance_content = template.render(
        openssl_key=str_key,
        instance_path=instance_path,
        **other_settings)
    
    # Config YAML file.
    if not config_yaml.exists():
        config_yaml.touch(exist_ok=True)
        ...
        config_yaml.write_text(instance_content, encoding="utf-8")
        
    with open(config_yaml) as f:
        instance_config = yaml.load(f, Loader=yaml.FullLoader)
    
    app.update_config(instance_config)


def set_database_uri(
    dialect: str,
    username: str, password: str,
    host: str, port: str,
    path: str
) -> str:
    if dialect == "sqlite":
        driver = "aiosqlite"
        return f"{dialect}+{driver}:///{path}"
    elif dialect == "mysql" or dialect == "mariadb":
        driver = "aiopymysql"
    elif dialect == "postgresql":
        driver = "asyncpg"
    return f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{path}"


def register_configure(app: Sanic) -> str:
    
    # Set mode from enviorment firstly.
    # **This Setting IS NOT used for running.**
    # `APP_ENV`
    if not app.config.get("ENV"):
        app_mode = "pro"
        # It will be production if not set to development.
    else: app_mode = app.config.ENV
    
    # print(app_mode)

    if app_mode == "dev" or app_mode == "development":
        # print("Configure Mode: Dev")
        app.update_config(DevConfig)
    elif app_mode == "test" or \
        app_mode == "t" or \
        app_mode == "tesing":
        app.update_config(DevConfig)  # Heritage seems not work.
        app.update_config(TestConfig)
    else:
        # print("Configure Mode: Pro")
        app.update_config(ProConfig)
    
    # About instance file
    if  True:#app.config["INSTANCE"] ==
        padding_instance(app)
