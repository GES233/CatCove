from mistune import Markdown, HTMLRenderer, escape
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class CustomeRenderer(HTMLRenderer):
    def block_code(self, code, lang):
        # code block: highlight
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        except Exception:
            return "\n<pre><code>%s</code></pre>\n" % escape(code)


class CatCoveMarkdownParser(Markdown):
    """为了方便内容分块计划重写部分逻辑"""

    def __init__(self, renderer, block=None, inline=None, plugins=None):
        super().__init__(renderer, block, inline, plugins)

    # 最好能够去掉空格就解析成对的东西。
