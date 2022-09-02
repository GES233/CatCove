import os
import asyncio
import click
from pathlib import Path
from sanic import Sanic
from sanic.exceptions import SanicException

PROJECT_PATH = Path().cwd()
APP_PATH = Path( PROJECT_PATH / "catcove" )


@click.group()
def manage():
    """ Manage the application. """
    pass

@manage.command("init")
@click.option("--db", default=False, help="DataBase settings.")
@click.option("--uri", default=None, help="Use URI to connect the DB.")
def set_instance(db, uri) -> None:
    """ Installation the application. """
    try:
        from .settings import (
            padding_instance,
            set_database_uri
        )
    except ImportError:
        raise SanicException("Do not run this from commands.py.")
    
    if db:
        click.secho("[WARNING] Please check your database's driver before nd install it.", fg="red")
        click.echo("sqlite: aiosqlite [installed]")
        click.echo("mysql/mariadb: aiopymysql")
        click.echo("postgresql: asyncpg")
    
    if db == True and not uri:
        dialect = click.prompt(
            text="Please enter the type of Database",
            default="sqlite",
            type=click.Choice(["sqlite", "mysql", "postgresql", "mariadb"])
        )
        if dialect == "sqlite":
            path = click.prompt(
                text="Please enter your database's path:"
            )
            username = password = host = port = None
        else:
            host = click.prompt(
                text="Please Enter your database's Host:",
                default="localhost"
            )
            username = click.prompt(
                text="Please Enter your database's Username:",
                default=dialect
            )
            password = click.prompt(
                text="Please Enter the Password:"
            )
            path = click.prompt(
                text="Please enter your database's Path/Database lastly:"
            )
    
    _app = Sanic("__temprory_app")
    padding_instance(
        _app,
        databeses = None if db else "SQLALCHEMY_DATABASE_URI: {}".format(
            uri if uri else set_database_uri(
                dialect,
                username, password,
                host, port, path
            )
        )
    )


@manage.command("db")
def db() -> None:
    """ Initlize the database. """
    # Add some WARNING info.
    from alembic import command
    from alembic.config import Config as AlembicConfig

    alembic_config = AlembicConfig(Path(PROJECT_PATH/"alembic.ini").__str__())
    command.upgrade(alembic_config, "head")


@manage.command("admin")
@click.option("--appointment", "transformation", flag_value="apt", help="There's no such implication whatsoever.")
@click.option("--create", "transformation", flag_value="crt", help="catcave.create(new_admin()) =>: ATM <- BTM.")
def create_spectator(transformation) -> None:
    """ Add `spectator`(aka admin). """
    ...


@manage.command("run")
@click.option("--dev", "mode", flag_value="dev")
@click.option("--demo", "-d", "mode", flag_value="demo", default=True)
@click.option("--pro", "mode", flag_value="pro")
def run(mode) -> None:
    """ Run the application. """
    if mode == "dev":
        os.environ["APP_ENV"] = "dev"

        from .web.app import create_app
        app = create_app()
        app.run(
            host="127.0.0.1",
            port="6969",
            dev=True
        )
    elif mode == "demo":
        os.environ["APP_ENV"] = "dev"

        from .web.app import create_app
        app = create_app()
        app.run(
            host="0.0.0.0",  # `route print`
            port="80",
            dev=True
        )
    else:
        from .web.app import create_app
        app = create_app()
        app.run(
            host="0.0.0.0",  # `route print`
            port="80",
            debug=False,
            auto_reload=False,
            access_log=False,
            fast=True
        )
