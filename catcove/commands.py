import os, sys
from pathlib import Path
import click
from sanic import Sanic
from sanic.exceptions import SanicException

PROJECT_PATH = Path().cwd()
APP_PATH = Path( PROJECT_PATH / "catcove" )

@click.command()
def set_instance():
    """ Installation the application. """
    try:
        from .settings import (
            padding_instance,
            set_database_uri
        )
    except ImportError:
        raise SanicException("Do not run this from commands.py.")
    
    # ...
    ...
    
    _app = Sanic("__temprory_app")
    padding_instance(_app,
        databeses = f"SQLALCHEMY_URL: {set_database_uri()}"
    )

@click.command()
def init_db():
    try:
        ...
    except ImportError:
        raise SanicException("Do not run this from commands.py.")
