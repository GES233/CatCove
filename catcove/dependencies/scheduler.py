from typing import Callable
from pytz import utc

from sanic import Sanic

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.pool import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)


jobstores = {
    # Datebase with web app using async mode.
    "default": SQLAlchemyJobStore("sqlite:///tinycat_job.db"),
}
executors = {
    "default": AsyncIOExecutor(),
}
job_defaults = {
    "coalesce": False,
    "max_instances": 8,
}

scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc,
)
"""
Put instance here to running.
"""

# ==== Listeners ==== #

# == Configure the logger == #


def error_linstener(event):
    ...


# ==== Functions ==== #


def addjob_in_app(
    app: Sanic, func: Callable, job_id: str, name: str | None = None, **kwargs
) -> None:
    """Add job in Sanic env."""
    app.ctx.scheduler: AsyncIOScheduler = scheduler
    app.ctx.scheduler.add_job(
        func=func,
        id=job_id,
        name=name,
        **kwargs,
    )


def updatejob_in_app(app: Sanic, **kwargs) -> None:
    ...
