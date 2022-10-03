import os
import asyncio
from typing import Any, Callable
import click
from pathlib import Path
from sanic import Sanic
from sanic.exceptions import SanicException

PROJECT_PATH = Path().cwd()
APP_PATH = Path(PROJECT_PATH / "catcove")


def run_async(func: Callable) -> Any:
    # May have some change.
    return asyncio.get_event_loop().run_until_complete(func)


@click.group()
def manage() -> None:
    """Manage the application."""
    pass


@manage.command("init")
@click.option("--db/--no-db", is_flag=True, default=True, help="Register SQL DataBase settings.")
@click.option("--redis/--no-redis", is_flag=True, default=False, help="Register Redis settings.")
@click.option("--raw/--no-raw", is_flag=True, default=False,
            help="Set file path to store raw file automatically.")
@click.option("--db-uri", default=None, help="Use URI to connect the DB.")
@click.option("--redis-uri", default=None, help="Use URI to connect the Redis.")
def set_instance(db, redis, raw, db_uri, redis_uri) -> None:
    """Installation the application."""
    click.secho("[INFO]    Welcome to use CatCove!\n", fg="magenta")
    try:
        from .settings import padding_instance, set_database_uri, set_redis_uri
    except ImportError:
        raise SanicException("Do not run this from commands.py.")

    # Relational database.
    if db == True:
        click.secho(
            "[WARNING] Please check your database and its driver before install it.",
            fg="red",
        )
        click.echo("sqlite        : aiosqlite  [installed]")
        click.echo("mysql/mariadb : aiopymysql")
        click.echo("postgresql    : asyncpg")

        if not db_uri:
            dialect = click.prompt(
                text="Please enter the type of Database",
                default="sqlite",
                type=click.Choice(["sqlite", "mysql", "postgresql", "mariadb"]),
            )
            if dialect == "sqlite":
                path = click.prompt(text="Please enter your database's path")
                username = password = host = port = None
            else:
                host = click.prompt(
                    text="Please Enter your database's Host", default="localhost"
                )
                port = click.prompt(
                    text="Please Enter your database's Post", default="2345"
                )
                username = click.prompt(
                    text="Please Enter your database's Username", default=dialect
                )
                password = click.prompt(text="Please Enter the Password")
                path = click.prompt(
                    text="Please enter your database's Path/Database lastly"
                )

    # Add redis here.
    if redis == True:
        click.secho(
            "[WARNING] Please check your redis and aioredis package before install it.",
            fg="red",
        )

        if not redis_uri:
            url_schemes = click.prompt(
                text="Please enter the schemes of url",
                default="redis",
                type=click.Choice(["redis", "rediss", "unix"])
            )
            re_username = click.prompt(
                text="Please enter your redis's username(ENTER whitespace if you not set password.)",
            )
            re_password = click.prompt("Now enter your password") if ' ' not in re_username else None
            if ' ' in re_username:
                re_username = None
            if url_schemes != "unix":
                # Host and port.
                re_host = click.prompt(text="Enter the host", default="localhost")
                re_port = click.prompt(text="And the port", default="6379")
                re_path = None
            else:
                re_host = re_port = None
                re_path = click.prompt("Enter your unix domain socket filename")
            re_db = "0"

    if raw == True:
        click.secho(
            "[INFO]    Now we'll configurate the path to store some static file",
            fg="blue"
        )
        enter_raw_path = click.prompt(text="Enter the COMPLETE path of raw content")
        enter_avatar_path = click.prompt(
            text="Enter the COMPLETE path of avater",
            default=enter_raw_path,
        )
        if enter_avatar_path == enter_raw_path:
            enter_avatar_path = Path(enter_raw_path)/"avatar".__str__()

    _app = Sanic("__temprory_app")
    padding_instance(
        _app,
        databases=None
        if db == False
        else "SQLALCHEMY_DATABASE_URI: {}\n".format(
            db_uri
            if db_uri
            else set_database_uri(dialect, username, password, host, port, path)
        ),
        redis_uri__=None
        if redis == False
        else "REDIS_URI: {}".format(
            redis_uri
            if redis_uri
            else set_redis_uri(
                url_schemes, re_username, re_password, re_host, re_port, re_db, re_path
            )
        ),
        raw_path=None
        if raw == False
        else "RAW_CONTENT_PATH: {}\n".format(enter_raw_path),
        avatar_path=None
        if raw == False
        else "AVATAR_PATH: {}".format(enter_avatar_path),
    )


@manage.command("db")
@click.option("--dev", "mode", flag_value="dev")
@click.option("--pro", "mode", flag_value="pro", default=True)
def upgrade_db(mode) -> None:
    """Initialize the database."""
    # Set warning first.
    click.secho(
        "[WARNING] This command will running via alembic, and it will reshape your database.",
        fg="red",
    )
    click.confirm("[CONFIRM]", abort=True)
    from alembic import command
    from alembic.config import Config as AlembicConfig

    # mode -> env.
    os.environ["APP_ENV"] = mode

    # Execute the command.
    alembic_config = AlembicConfig(Path(PROJECT_PATH / "alembic.ini").__str__())
    command.upgrade(alembic_config, "head")

    # Finish.
    click.secho("[INFO]    Database initialized.", fg="green")


@manage.command("admin")
@click.option(
    "--appointment",
    "transformation",
    flag_value="apt",
    help="There's no such implication whatsoever.",
)
@click.option(
    "--create",
    "transformation",
    flag_value="crt",
    help="catcave.create(new_admin()) =>: ATM <- BTM.",
)
def create_spectator(transformation) -> None:
    """Add `spectator`(aka admin)."""
    from .dependencies.db import async_session
    from .usecase.users import UserService
    from .usecase.manage import ManageService

    user_service = UserService(async_session)

    if transformation == "apt":
        nickname_ = click.prompt("Please enter new spectator's nickname or email")
        if not isinstance(eval(nickname_), int):
            user = run_async(user_service.check_common_user(nickname_, ""))
        else:
            # Query from id.
            user = run_async(user_service.get_user(eval(nickname_)))
        
        if not user:
            click.secho("[ERROR]   Not fetch user in database.", fg="red")
    elif transformation == "crt":
        # Create a new user.
        password = ""
        confirm = "_"
        nickname = click.prompt("Please enter new spectator's nickname")
        email = click.prompt("Please enter new spectator's email")
        while password != confirm:
            password = click.prompt(
                "Please enter new spectator's password", hide_input=True
            )
            confirm = click.prompt(
                "Please confirm new spectator's password", hide_input=True
            )
        common = run_async(user_service.check_common_user(nickname, email))
        if common == True:  # common != False
            click.secho(
                "[ERROR]   Have common user, please check your nickname or email, or use `--appointment` instead.",
                fg="red",
            )
        else:
            user = run_async(user_service.create_user(nickname, email, password))
            
    manage_service = ManageService(async_session, user)
    
    # Get current user's role firstly.
    _ = run_async(manage_service.get_role())
    if manage_service.user_as_spectator:
        click.secho("[WARNING] Current user IS spectator now.", fg="yellow")
    else:
        _ = run_async(manage_service.be_spectator(
            click.prompt(
                text="Please enter password now",
                hide_input=True,
            )
        ))
        click.secho("[INFO]    Successfully now!", fg="green")


# Create an instance outside of function.
from catcove.web.app import create_app
app = create_app()

@manage.command("run")
@click.option("--dev", "mode", flag_value="dev")
@click.option("--demo", "-d", "mode", flag_value="demo", default=True)
@click.option("--pro", "mode", flag_value="pro")
def run(mode) -> None:
    """Run the application."""
    from pprint import pprint
    pprint([r for r in app.router.routes])

    if mode == "dev":
        os.environ["APP_ENV"] = "dev"
        app.run(host="127.0.0.1", port=6969, debug=True, auto_reload=True)
    elif mode == "demo":
        os.environ["APP_ENV"] = "dev"
        app.run(host="0.0.0.0", port=80, dev=True)  # `route print`
    else:
        os.environ["APP_ENV"] = "pro"
        app.run(
            host="0.0.0.0",  # `route print`
            port=80,
            debug=False,
            auto_reload=False,
            access_log=False,
            fast=True,
        )
