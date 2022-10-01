from pathlib import Path
from mistune import create_markdown, Markdown, HTMLRenderer
from sanic import Sanic


def setup_md_renderer(app: Sanic) -> None:
    """Setup series of renderer instance to render html."""

    from mistune.plugins import (
        # plugin_strikethrough,  # Pico.css's <del></del> is red, so replace it.
        plugin_footnotes,
        plugin_table,
        plugin_task_lists,
    )
    from .renderer import CatCoveMarkdownParser
    from .url import plugin_url
    from .highlight import plugin_highlight
    from .utils import plugin_strikethrough

    # custome_renderer = CatCovePostsRenderer()
    from .renderer import CustomeRenderer

    app.ctx.post_renderer: Markdown = CatCoveMarkdownParser(
        renderer=CustomeRenderer(),
        plugins=[
            plugin_strikethrough,  # ~~delete~~
            plugin_footnotes,  # [^footnote]
            plugin_table,  # | TABLE |
            plugin_task_lists,  # - [x] tasks
            plugin_url,  # av170001
            plugin_highlight,  # ==Highlight from Obsidian==
        ],
    )

    # Render code.
    app.ctx.code_renderer: Markdown = create_markdown(
        renderer=CustomeRenderer(),
    )

    # No `section` in comment.
    # No update.
    app.ctx.comment_renderer: Markdown = CatCoveMarkdownParser(
        renderer=CustomeRenderer(),
        plugins=[
            plugin_strikethrough,  # ~~delete~~
            plugin_task_lists,  # - [x] tasks
            plugin_url,  # av170001
            plugin_highlight,  # ==Highlight from Obsidian==
        ],
    )


def render_from_str(raw: str, instance: Markdown) -> str:
    return instance(raw)
