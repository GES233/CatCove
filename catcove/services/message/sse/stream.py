from typing import List
from sanic.request import Request
from sanic.compat import Header


event = lambda id, type, retry, data: "id: {}\r\nevent: {}\r\nretry: {}\r\n{}\r\n\n".format(
    id,
    type,
    retry,
    ''.join(["data: " + item + "\n" for item in data]),
)


sse_header: List[Header] = Header(
    {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }
)

async def publisher_have_redis(request: Request):
    response = await request.respond(
        headers=sse_header,
        content_type="text/event-stream",
    )
    current_user = request.ctx.current_user
    # Fetch message push to user from redis.
    ...

    # Push message to front-end.
    retry = request.app.ctx.KEEP_ALIVE_TIMEOUT * 100
    ...
    await response.send(
        event(0, "site", retry, ["Pong"])
    )



async def publisher_no_redis(request: Request):
    response = await request.respond(
        headers=sse_header,
        content_type="text/event-stream",
    )
    await response.send(
        event(0, "site", 3000, ["Pong"])
    )
    await response.send(
        event(1, "close", 2000, [
            "Server not support SSE.",
            "because it not has Redis to store the info."
        ])
    )