from pathlib import Path
import re
from typing import Dict, List, Type
from mistune import create_markdown
from mistune.renderers import BaseRenderer
from sanic import Sanic

def setup_md_renderer(app: Sanic) -> None:
    """Setup series of renderer instance to render html."""

    from .url import plugin_url

    app.ctx.post_renderer = create_markdown(
        plugins=[
            "strikethrough", # ~~delete~~
            "footnotes",     # [^footnote]
            "table",         # | TABLE |
            "task_lists",    # - [x] tasks
            plugin_url,      # av170001
        ]
    )

    # Render code.
    from .code import HighlightRenderer
    app.ctx.code_renderer = create_markdown(renderer=HighlightRenderer())

    # No `section` in comment.
    # No update.
    app.ctx.comment_renderer = create_markdown(
        plugins=[
            "strikethrough", # ~~delete~~
            "task_lists",    # - [x] tasks
            plugin_url,      # av170001
        ]
    )


def _parse_content(raw: str) -> List[Dict[int, Dict[type, str]]]:
    # 几个原则：
    # - ...
    ...


def render_from_str(raw: str) -> str:
    ...
    content = []
    for paragraph in re.split(raw, r"\n\n"):
        ...
    return "".join(content)


def render_from_file(path: Path) -> str:
    ...
    return render_from_file()
