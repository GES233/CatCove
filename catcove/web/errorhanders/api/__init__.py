from sanic.errorpages import JSONRenderer
from sanic.response import HTTPResponse, json

from ....usecase.api import APIServise

from ...blueprints.api.helper import code


class CustomJSONRenderer(JSONRenderer):
    """Rewrite Sanic's JSONRenderer with custome format."""

    def render(self) -> HTTPResponse:
        return super().render()

    def minimal(self) -> HTTPResponse:
        output = self._generate_output(full=False)
        api = APIServise()
        return json(
            api.base_resp(
                code=code.SERVER_ERROR,
                info=output["message"],
                type="ERROR",
                data={"description": output["description"]},
            ).json(),
            status=self.status,
        )

    def full(self) -> HTTPResponse:
        output = self._generate_output(full=True)
        api = APIServise()

        # Some business code to set code and info.
        ...

        return json(
            api.base_resp(
                code=code.SERVER_ERROR,
                info=output["message"],
                type="ERROR",
                data={
                    "description": output["description"],
                    "path": output["path"],
                    "args": output["args"],
                    "exceptions": output["exceptions"],
                },
            ).json(),
            status=self.status,
        )
