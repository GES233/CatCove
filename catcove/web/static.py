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
    app.static("/css", css_path)
    app.static("/js", js_path)
    app.static("/img", img_path)

    """Custome"""
    # main
    raw_path = Path(app.config["RAW_CONTENT_PATH"])
    if not raw_path.exists():
        raw_path.mkdir()
    app.static("/raw", raw_path)
    # avatar
    avatar_path = Path(app.config["AVATAR_PATH"])
    if not avatar_path.exists():
        avatar_path.mkdir()
    app.static("/avatar", avatar_path)
