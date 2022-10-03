from typing import Union, Optional, Dict
from sanic.response import HTTPResponse


def stream(
    body: Union[str, bytes],
    status: int = 200,
    headers: Optional[Dict[str, str]] = None,
    content_type: str = "text/event-stream",
) -> HTTPResponse:
    """
    Server-side SEE implementation.
    """
    if headers:
        headers["Cache-Control:"] = "no-cache"
    else:
        headers = {"Cache-Control: no-cache"}
    return HTTPResponse(
        body="".join("data: {}\n\n".format(item) for item in body),
        status=status,
        headers=headers,
        content_type=content_type,
    )
