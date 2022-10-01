from json import dump
import os
import pytest
import requests


class TestAccess(object):

    def test_index(self):
        # Run the application.
        from catcove import create_app

        os.environ["APP_ENV"] = "dev"
        app = create_app()
        app.run(port=6969)

        # Return index.
        idx = requests.get("http://127.0.0.1:6969")

        assert idx.ok == True
        assert idx.apparent_encoding == "utf-8"

        # API.
        api_idx = requests.get("http://127.0.0.1:6969/api/v0.1/")

        assert api_idx.ok == True

        app.stop()

    def test_login(self):
        # Run the application.
        from catcove import create_app

        os.environ["APP_ENV"] = "dev"
        app = create_app()
        app.run(port=6969)

        login = requests.post(
            "http://127.0.0.1/login",
            ...
        )

        assert login.cookies.get("UserMeta")

        app.stop()

    def test_api_login(self):
        # Run the application.
        from catcove import create_app

        os.environ["APP_ENV"] = "dev"
        app = create_app()
        app.run(port=6969)

        login = requests.post(
            "http://127.0.0.1/api/v0.1/login",
            data=dump(
                {
                    "nickname": "小地瓜",
                    "password": "12345"
                }
            )
        )

        assert login.cookies.get("UserMeta")

        app.stop()
