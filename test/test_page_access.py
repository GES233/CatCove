import os
import pytest
import requests


class TestAccess(object):
    def init(self):
        # Run the application.
        from catcove import create_app

        os.environ["APP_ENV"] = "dev"
        app = create_app()
        app.run(port=6969)

    def test_index(self):
        self.init()

        # Return index.
        idx = requests.get("http://127.0.0.1:6969")

        assert idx.ok == True
        assert idx.apparent_encoding == "utf-8"

        # API.
        api_idx = requests.get("http://127.0.0.1:6969/api/v0.1/")

        assert api_idx.ok == True

    def test_login(self):
        self.init()

        ...

    def test_api_login(self):
        self.init()

        ...
