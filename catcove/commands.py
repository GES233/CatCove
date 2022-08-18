import asyncio
import click
from pathlib import Path
from sanic import Sanic
from sanic.exceptions import SanicException

PROJECT_PATH = Path().cwd()
APP_PATH = Path( PROJECT_PATH / "catcove" )


@click.group()
def init():
    pass

@init.command()
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
                text="Please enter your database's Path lastly:"
            )
    
    _app = Sanic("__temprory_app")
    padding_instance(
        _app,
        databeses = "SQLALCHEMY_DATABASE_URI: {}".format(
            uri if uri else set_database_uri(
                dialect,
                username, password,
                host, port, path
            )
        )
    )


async def init_db_no_migrate():
    try:
        from catcove.entities.tables import Base
        from catcove.dependencies.db import async_session
    except ImportError:
        raise SanicException("Do not run this from commands.py.")
    except AttributeError:
        # Not get the `SQLALCHEMY_DATABSE_URI`, to the instance/config.pro to update.
        raise SanicException("Please set the configure of app.")
    
    async with async_session.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    click.secho("Database initialzed!", fg="blue")


@init.command()
@click.option("--migrate", default=False, help="Use alembic to install the database.")
def db(migrate):
    
    if migrate == True:
        # Use SQLAlchemy to initialize the database.
        asyncio.get_event_loop().run_until_complete(init_db_no_migrate())
    else:
        from alembic import command
        from alembic.config import Config as AlembicConfig

        alembic_config = AlembicConfig(Path(PROJECT_PATH/"alembic.ini").__str__())
        command.upgrade(alembic_config, "head")


@click.command("admin")
@click.option("--appointment", "transformation", flag_value="apt", help="There's no such implication whatsoever.")
@click.option("--create", "transformation", flag_value="crt", help="catcave.create(new_admin()) =>: ATM <- BTM.")
def create_spectator(transformation):
    """ Add `spectator`(aka. admin). """
    ...
