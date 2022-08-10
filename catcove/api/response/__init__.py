from typing import Optional, Dict
from pydantic import BaseModel
from sanic.response import HTTPResponse


def model2json(
    body: BaseModel,
    status: int = 200,
    headers: Optional[Dict[str, str]] = None,
    content_type: str = "application/json",
    **kwargs
) -> HTTPResponse:
    """
    Returnes response object with body.
    """
    return HTTPResponse(
        body.json(),
        status=status,
        headers=headers,
        content_type=content_type
    )
