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

    ecc_prk = Path(instance_path/"eckey.pem")
    ecc_puk = Path(instance_path/"ecpubkey.pem")
    
    # Config YAML file.
    if not config_yaml.exists():
        from mako.template import Template
    
        template = Template(filename=f"{PRJ_PATH}/catcove/settings/config.yml.mako")
    
        # SECRET: $ openssl rand -base64 32
        str_key = (os.popen("openssl rand -base64 32").readline().strip("\n"))

        config_yaml.touch(exist_ok=True)
        instance_content = template.render(
            openssl_key=str_key,
            ecc_prk_path=ecc_prk,
            ecc_puk_path=ecc_puk,
            **other_settings)
        config_yaml.write_text(instance_content.replace("\r\n", "\n"), encoding="latin1")
    
    update_instance(app, config_yaml)
        

def update_instance(app: Sanic, config_yaml: Path) -> None:
    # Read from it.
    
    with open(config_yaml) as f:
        instance_config = yaml.load(f, Loader=yaml.FullLoader)
    
    app.update_config(instance_config) if instance_config else ...


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


def register_configure(app: Sanic) -> None:
    
    # Set mode from enviorment firstly.
    # **This Setting IS NOT used for running.**
    # `APP_ENV`
    if not app.config.get("ENV"):
        app_mode = "pro"
        # It will be production if not set to development.
    else: app_mode = app.config.ENV

    # Use the default config firstly.
    if app_mode == "dev" or app_mode == "development":
        app.update_config(DevConfig)
    elif app_mode == "test" or \
        app_mode == "tesing":
        app.update_config(DevConfig)  # Heritage seems not work.
        app.update_config(TestConfig)
    else:
        app.update_config(ProConfig)
    
    # Using instance if `INSTANCE` is True.
    if app.config["INSTANCE"] == True:
        padding_instance(app)
