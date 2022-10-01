from mistune.util import ESCAPE_TEXT


HIGHLIGHT_PATTERN: str = (
    r"==(?=[^\s~])(" r"(?:\\~|[^~])*" r"(?:" + ESCAPE_TEXT + r"|[^\s~]))=="
)


def parse_highlight(inline, m, state):
    text = m.group(1)
    return "highlight", inline.render(text, state)


def plugin_highlight(md):
    md.inline.register_rule("highlight", HIGHLIGHT_PATTERN, parse_highlight)

    index = md.inline.rules.index("codespan")
    if index != -1:
        md.inline.rules.insert(index + 1, "highlight")
    else:  # pragma: no cover
        md.inline.rules.append("highlight")

    if md.renderer.NAME == "html":
        md.renderer.register("highlight", lambda x: "<mark>" + x + "</mark>")
