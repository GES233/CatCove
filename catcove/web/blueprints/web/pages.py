from pathlib import Path
from sanic import Blueprint, Request, html
from sanic.response import HTTPResponse

from ....services.render import render_page_template
from ....services.markdown import md_render

index_bp = Blueprint("index")
policy_bp = Blueprint("policy", url_prefix="/policy")

MARKDOWN_ROOT_PATH = Path(Path(__file__).cwd() / "catcove/static/file")


@index_bp.route("/")
async def index(request: Request) -> HTTPResponse:

    return html(
        render_page_template(
            "index.html",
            role="首页",
            cookie_user=request.ctx.current_user,
        )
    )


@index_bp.route("/about")
async def about(request: Request) -> HTTPResponse:
    return html(
        # render_page_template("about.html", role="About", cookie_user=request.ctx.current_user)
        render_page_template(
            "content/raw_md_without_author.html",
            role="关于",
            main_content=md_render(
                Path(MARKDOWN_ROOT_PATH / "about.md").read_text("utf-8"),
                request.app.ctx.basic_renderer,
            ),
            cookie_user=request.ctx.current_user,
        )
    )


@policy_bp.route("/signup")
async def policy_for_newbie(request: Request) -> HTTPResponse:
    return html(
        render_page_template(
            "content/raw_md_without_author.html",
            title="社区守则（面向新成员）",
            main_content=md_render(
                Path(MARKDOWN_ROOT_PATH / "policy/newbie.md").read_text("utf-8"),
                request.app.ctx.basic_renderer,
            ),
            cookie_user=request.ctx.current_user,
        )
    )


@policy_bp.route("/")
async def policy_main(request: Request) -> HTTPResponse:
    return html(
        render_page_template(
            "content/raw_md_without_author.html",
            title="Under construction",
            cookie_user=request.ctx.current_user,
        )
    )
