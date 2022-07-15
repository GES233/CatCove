from sanic.response import HTTPResponse
from pydantic import BaseModel
from typing import Optional, Dict

def schemasjson(
    body: BaseModel,
    status: int = 200,
    headers: Optional[Dict[str, str]] = None,
    content_type: str = "application/json"
) -> HTTPResponse:
    """
    Returns response object with body in json format.

    :param body: Basemodel data, wil formated to json type.
    :param status: Response code.
    :param headers: Custom Headers.
    :param kwargs: Remaining arguments that are passed to the json encoder.
    """
    return HTTPResponse(
        body.json(),
        headers=headers,
        status=status,
        content_type=content_type,
    )
