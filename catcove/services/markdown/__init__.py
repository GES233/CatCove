from pathlib import Path
import re
from typing import Dict, List, Type
from mistune import create_markdown, Markdown
from sanic import Sanic

def setup_md_renderer(app: Sanic) -> None:
    """Setup series of renderer instance to render html."""

    from .url import plugin_url
    from .highlight import plugin_highlight

    app.ctx.post_renderer: Markdown = create_markdown(
        plugins=[
            "strikethrough", # ~~delete~~
            "footnotes",     # [^footnote]
            "table",         # | TABLE |
            "task_lists",    # - [x] tasks
            plugin_url,      # av170001
            plugin_highlight,# ==Highlight from Obsidian==
        ]
    )

    # Render code.
    from .code import CodeHighlightRenderer
    app.ctx.code_renderer: Markdown = create_markdown(renderer=CodeHighlightRenderer())

    # No `section` in comment.
    # No update.
    app.ctx.comment_renderer: Markdown = create_markdown(
        plugins=[
            "strikethrough", # ~~delete~~
            "task_lists",    # - [x] tasks
            plugin_url,      # av170001
            plugin_highlight,# ==Highlight from Obsidian==
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
