#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'x7'
AUTHOR_EMAIL = 'x7.0@outlook.com'
SITENAME = 'x7\'s blog'
SITEURL = 'http://x7res.info'
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'zhs'
THEME = 'pelican-themes/gum'

DISQUS_SITENAME = 'x7qus'
GOOGLE_ANALYTICS_ID = 'UA-44068198-1'
GOOGLE_ANALYTICS_SITENAME = 'x7res.info'

OUTPUT_PATH = '.'
ARCHIVES_URL = 'archives.html'
ARTICLE_URL = 'archives/{slug}.html'
ARTICLE_SAVE_AS = 'archives/{slug}.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
FEED_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#        ('ArchWiki', 'https://wiki.archlinux.org/'),)

# Social widget
SOCIAL = (('新浪微博', 'http://weibo.com/ulzzz'),
          ('GitHub', 'https://github.com/x7hub'),
          ('Twitter', 'https://twitter.com/x7tter'),
          ('Facebook', 'https://www.facebook.com/profile.php?id=100009856203706'),
          ('Google+', 'https://plus.google.com/u/0/103542609671038993194'),
          )

GITHUB_URL = 'https://github.com/x7hub'
TWITTER_URL = 'https://twitter.com/x7tter'
FACEBOOK_URL = 'https://www.facebook.com/profile.php?id=100009856203706'
GOOGLEPLUS_URL = 'https://plus.google.com/u/0/103542609671038993194'

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
