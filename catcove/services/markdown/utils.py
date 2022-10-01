from mistune.plugins.extra import STRIKETHROUGH_PATTERN, parse_strikethrough


def plugin_strikethrough(md):
    # ~~bla~~ => <s>bla</s>
    md.inline.register_rule("strikethrough", STRIKETHROUGH_PATTERN, parse_strikethrough)

    index = md.inline.rules.index("codespan")
    if index != -1:
        md.inline.rules.insert(index + 1, "strikethrough")
    else:  # pragma: no cover
        md.inline.rules.append("strikethrough")

    if md.renderer.NAME == "html":
        md.renderer.register("strikethrough", lambda x: "<s>" + x + "</s>")


def plugin_horizontal_rule(md):
    # = = =
    # - - -
    # * * *
    # => <hr>
    ...
