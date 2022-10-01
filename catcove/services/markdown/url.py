from mistune.plugins.extra import URL_LINK_PATTERN, parse_url_link


# Markdown: [[av10492]]
# ==> <a href="https://www.bilibili.com/video/av10492">av10492</z>

SITE_PATTERN = r"\[\[" "{}" r"\]\]"

ACFUN_SITE_PATTERN = SITE_PATTERN.format(r"ac[\d]+?")
BILI_AV_SITE_PATTERN = SITE_PATTERN.format(r"av[\d]+?")
BILI_BV_SITE_PATTERN = SITE_PATTERN.format(r"BV[\w]+?")
# YOUTUBE_SITE_PATTERN = SITE_PATTERN.format(r"watch?=")

acfun_video = lambda vid: '<a href="https://www.acfun.cn/{0}">{0}</a>'.format(
    vid.strip("[").strip("]")
)
bili_video = lambda vid: '<a href="https://www.bilibili.com/video/{0}">{0}</a>'.format(
    vid.strip("[").strip("]")
)
# youtube_video = lambda vid: '<a href="https://youtu.be/watch?={}">{0}</a>'.format(vid.strip("[").strip("]"))

purse_acfun_url = lambda inline, m, state: ("site_acfun_url", m.group(0))
purse_bili_av_url = lambda inline, m, state: ("site_bili_av_url", m.group(0))
purse_bili_bv_url = lambda inline, m, state: ("site_bili_bv_url", m.group(0))


def plugin_url(md):
    # Set custome url.
    # ac___        => Acfun
    # av___/BV____ => Bilibili

    md.inline.register_rule("site_acfun_url", ACFUN_SITE_PATTERN, purse_acfun_url)
    md.inline.register_rule("site_bili_av_url", BILI_AV_SITE_PATTERN, purse_bili_av_url)
    md.inline.register_rule("site_bili_bv_url", BILI_BV_SITE_PATTERN, purse_bili_bv_url)
    md.inline.rules.append("site_acfun_url")
    md.inline.rules.append("site_bili_av_url")
    md.inline.rules.append("site_bili_bv_url")
    if md.renderer.NAME == "html":
        md.renderer.register("site_acfun_url", acfun_video)
        md.renderer.register("site_bili_av_url", bili_video)
        md.renderer.register("site_bili_bv_url", bili_video)

    # Source.
    md.inline.register_rule("url_link", URL_LINK_PATTERN, parse_url_link)
    md.inline.rules.append("url_link")
