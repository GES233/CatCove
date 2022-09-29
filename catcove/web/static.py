from sanic import Sanic
from pathlib import Path, PurePath


def load_static(app: Sanic) -> None:
    """Load static file to server."""
    prj_path = Path(__file__).cwd()
    static_path = PurePath(prj_path / "catcove/static")

    favicon_path = PurePath(static_path / "img/favicon.ico")
    robots_path = PurePath(static_path / "robots.txt")
    css_path = PurePath(static_path / "css/")
    js_path = PurePath(static_path / "js/")
    img_path = PurePath(static_path / "img/")

    app.static("/favicon.ico", favicon_path)
    app.static("/robots.txt", robots_path)
    app.static("/static/css", css_path)
    app.static("/static/js", js_path)
    app.static("/static/img", img_path)
