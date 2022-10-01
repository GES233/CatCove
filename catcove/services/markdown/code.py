import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class HighlightRenderer(mistune.renderers.HTMLRenderer):
    def block_code(self, code, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        except Exception:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)


def code2html(content: str):
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    return markdown(content)
