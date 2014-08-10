#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'x7'
AUTHOR_EMAIL = 'x7.0@outlook.com'
SITENAME = 'x7\'s blog'
SITEURL = 'http://x7hub.github.io'
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'zhs'

#THEME = 'tuxlite_tbs'
THEME = 'gum'

GITHUB_URL = 'https://github.com/x7hub'
DISQUS_SITENAME = 'x7qus'
GOOGLE_ANALYTICS_ID = 'UA-44068198-1'
GOOGLE_ANALYTICS_SITENAME = 'x7hub.github.io'

OUTPUT_PATH = '.'
ARCHIVES_URL = 'archives.html'
ARTICLE_URL = 'pages/{slug}.html'
ARTICLE_SAVE_AS = 'pages/{slug}.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
TAG_FEED_ATOM = 'feeds/%s.atom.xml'
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
        ('ArchWiki', 'https://wiki.archlinux.org/'),)

# Social widget
SOCIAL = (('新浪微博', 'http://weibo.com/ulzzz'),
          ('GitHub', 'https://github.com/x7hub'),
          )
#SOCIAL = (('新浪微博', 'http://weibo.com/ulzzz'),
#          )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["sitemap"]

## 配置sitemap 插件
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.7,
        "indexes": 0.5,
        "pages": 0.3,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}
