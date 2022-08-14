from sanic import Sanic
from pathlib import Path
import yaml
import os

from .dev import DevConfig
from .test import TestConfig
from .pro import ProConfig


def padding_instance(prj_path) -> str:
    from mako.template import Template
    
    template = Template(filename=f"{prj_path}/catcove/settings/config.yaml.mako")
    
    # SECRET: $ openssl rand -base64 32
    str_key = (os.popen("openssl rand -base64 32").readline().strip("\n"))
    return template.render(
        openssl_key=str_key,
        instance_path=f"{prj_path}/instance")



def register_configure(app: Sanic) -> str:
    # set path.
    PRJ_PATH = Path(__file__).cwd()
    
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
        app.update_config(TestConfig)
    else:
        # print("Configure Mode: Pro")
        app.update_config(ProConfig)
    
    # About instance file
    if app.config["INSTANCE"] == True:
        instance_path = Path(PRJ_PATH / "instance/")
        config_yaml = Path(instance_path/"config.yml")
        
        
        # Folder.
        if not instance_path.is_dir():
            # Create a new folder.
            instance_path.mkdir()

            # Create_Key file.
            os.popen(f"cd {instance_path} && \
                openssl ecparam -genkey -noout -name prime256v1 -out eckey.pem -text && \
                openssl ec -in eckey.pem -pubout -out ecpubkey.pem")
        
        # Config YAML file.
        if not config_yaml.exists():
            config_yaml.touch(exist_ok=True)
            ...
            config_yaml.write_text(padding_instance(PRJ_PATH), encoding="utf-8")
        
        with open(config_yaml) as f:
            instance_config = yaml.load(f, Loader=yaml.FullLoader)
        
        app.update_config(instance_config)
