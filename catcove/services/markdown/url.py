from mistune.plugins.extra import URL_LINK_PATTERN, parse_url_link


def plugin_url(md):
    # Set custome url.
    # ac___        => Acfun
    # av___/BV____ => Bilibili
    # watch?____   => YouTube
    # ...

    md.inline.register_rule('url_link', URL_LINK_PATTERN, parse_url_link)
    md.inline.rules.append('url_link')
