from sanic import Sanic
from pathlib import Path
import yaml
import os

from .dev import DevConfig
from .pro import ProConfig


def padding_instance(app_path) -> str:
    from mako.template import Template
    
    template = Template(filename=f"{app_path}/catcove/settings/config.yaml.mako")
    # SECRET: $ openssl rand -base64 32
    str_key = (os.popen("openssl rand -base64 32").readline().strip("\n"))
    return template.render(openssl_key=str_key)



def register_configure(app: Sanic) -> str:
    # set path.
    APP_PATH = Path(__file__).cwd()
    
    # Set mode from enviorment firstly.
    # **This Setting IS NOT used for running.**
    # `APP_ENV`
    if not app.config.get("ENV"):
        app_mode = None
    else: app_mode = app.config.ENV

    if app_mode == "dev" or app_mode == "development":
        # print("Configure Mode: Dev")
        app.update_config(DevConfig)
    else:
        # It will be production if not set to development.
        # print("Configure Mode: Pro")
        app.update_config(ProConfig)
    
    # About instance file
    if app.config["INSTANCE"] is True:
        instance_path = Path(APP_PATH / "instance/")
        config_yaml = Path(instance_path/"config.yml")
        
        
        # Folder.
        if not instance_path.is_dir():
            # Create a new folder.
            instance_path.mkdir()

            # Create_Key file.
            os.popen(f"cd {instance_path} && \
                openssl ecparam -genkey -name secp112r1 -out eckey.pem -text && \
                openssl ec -in eckey.pem -pubout -out ecpubkey.pem")
        
        # Config YAML file.
        if not config_yaml.exists():
            config_yaml.touch(exist_ok=True)
            ...
            config_yaml.write_text(padding_instance(APP_PATH), encoding="utf-8")
        
        with open(config_yaml) as f:
            instance_config = yaml.load(f, Loader=yaml.FullLoader)
        
        app.update_config(instance_config)
