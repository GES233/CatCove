# Flash like flask.
# The data only transfored when response.

from contextvars import ContextVar

def flash_push() -> None: ...

def flash_pop() -> None: ...
