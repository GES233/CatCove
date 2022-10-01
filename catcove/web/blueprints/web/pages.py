from http.client import ImproperConnectionState
from pathlib import Path
from sanic import Blueprint, Request, html
from sanic.response import HTTPResponse

from ....services.render import render_page_template
from ....services.markdown import render_from_str

index_bp = Blueprint("index")

MARKDOWN_ROOT_PATH = Path(Path(__file__).cwd() / "catcove/static/file")


@index_bp.route("/")
async def index(request: Request) -> HTTPResponse:

    return html(render_page_template("index.html", user=request.ctx.current_user))


@index_bp.route("/about")
async def about(request: Request) -> HTTPResponse:
    return html(
        # render_page_template("about.html", role="About", user=request.ctx.current_user)
        render_page_template(
            "content/raw_md_without_author.html",
            role="About",
            main_content=render_from_str(
                Path(MARKDOWN_ROOT_PATH / "about.md").read_text("utf-8"),
                request.app.ctx.post_renderer,
            ),
            user=request.ctx.current_user,
        )
    )


@index_bp.route("/signup-policy")
async def use_policy(request: Request) -> HTTPResponse:
    return html(
        render_page_template(
            "content/raw_md_without_author.html",
            title="社区守则（面向新成员）",
            main_content=render_from_str(
                Path(MARKDOWN_ROOT_PATH / "policy/newbie.md").read_text("utf-8"),
                request.app.ctx.post_renderer,
            ),
            user=request.ctx.current_user,
        )
    )
