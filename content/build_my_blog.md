Date: 2013-08-27
Title: 在Github Pages上搭建个人博客
Category: blog
Tags: blog, github, pelican
Slug: build_my_blog

参考:

[一步一步打造Geek风格的技术博客 by lizherui](http://www.lizherui.com/pages/2013/08/17/build_blog.html)

[用pelican在github上创建自己的博客! by mx](http://x-wei.github.io/pelican_github_blog.html)

[使用Pelican打造静态博客 by cold](http://www.linuxzen.com/shi-yong-pelicanda-zao-jing-tai-bo-ke.html)

### 搭建环境

在Linux环境下搭建，我使用的是Archlinux i686，使用其它发行版过程基本相同。

### Github Pages

* 注册Github,注册和配置SSH密钥过程[help page](http://help.github.com/articles/set-up-git)写得很清楚。
* 在Github创建一个名为username.github.io的版本库（将username替换成自己的Github账户名）。
* Setting -> Automatic page generator -> Continue to layout，选择一个模板，并发布。

这时在username.github.io页面就已经生成了一个页面。

### 本地搭建

* 安装pelican和markdown：
```sh
yaourt pelican
yaourt markdown
```
* 搭建目录：
```sh
mkdir blog
cd blog
pelican-quickstart
```
生成的目录结构:
```sh
blog/
├── content
│   └── *.md             # markdown文件
├── output               # 默认的输出目录
├── develop_server.sh
├── Makefile
├── pelicanconf.py       # 主配置文件
└── publishconf.py
```
* clone之前生成的username.github.io版本库：
```sh
git clone git@github.com:username/username.github.io.git
```
为了直接向Github的username.github.io库中提交本地生成的文件：
```sh
mv username.github.io/.git .
rm -rf username.github.io
```
这样就可以将整个blog目录托管在github上。

### 修改配置文件

#### 配置Makefile

修改默认的`$OUTPUTDIR`值，使之指向博客根目录而不是output目录，这是因为生成的index.html必须位于github托管目录的根目录，才能访问到网页。

```makefile
OUTPUTDIR=$(BASEDIR)
```

修改`publish`项的值，不必需要提供默认输出目录，另外指定pelidanconf.py为配置文件：

```makefile
publish:
    $(PELICAN) $(INPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
```

添加`github`项，方便直接向github提交修改：

```makefile
github: publish
    cd $(OUTPUTDIR); git add .; git commit -am 'zzz'; git push
```

另外可以删除掉不必要的项。

#### 配置pelicanconf.py

修改`AUTHOR`，`SITENAME`，`TIMEZONE`，`DEFAULT_LANG`，`GITHUB_URL`，`LINKS`，`SOCIAL`等选项：
```python
AUTHOR = 'x7'
SITENAME = 'x7\'s 
TIMEZONE = 'Asia/Beijing'
DEFAULT_LANG = 'zhs'
GITHUB_URL = '<https://github.com/x7hub>'

LINKS =  (('Pelican', 'http://getpelican.com/'),
        ('ArchWiki', 'https://wiki.archlinux.org/'),
        )

SOCIAL = (('新浪微博', 'http://weibo.com/ulzzz'),
          )
```

指定默认输出目录：

```python
OUTPUT_PATH = '.'
```

### 写博文

需要编辑的md文件应该位于content目录下，我暂时使用的编辑器是ReText，另外有一个在线的编辑器[MaHua](http://mahua.jser.me)，还没尝试其他。

pelican要求文章的开头必须有一些字段，如`Title`等，比如本文的开头是这样的：
```
Date: 2013-08-27
Title: 在Github Pages上搭建个人博客
Category: blog
Tags: blog
Slug: build_my_blog
```

编辑完成后，利用`make pulish`生成博文，还可以通过`make serve`在localhost:8000可以生成预览，如果完成了之前对Makefile的修改，就可以用`make github`直接提交到Github。

### 主题

生成的博文好丑！

安装主题：
```sh
yaourt pelican-themes
```
不是archlinux系统的话就这样：
```sh
git clone https://github.com/getpelican/pelican-themes.git
cd pelican-themes
pelican-themes -i tuxlite_tbs
```
其中tuxlite_tbs是选择使用的主题，[pelican主题的Github目录](http://github.com/getpelican/pelican-themes)下几乎每个都提供了预览.

然后，在配置文件`pelicanconf.py`中添加：
```python
THEME = 'tuxlite_tbs'
```

重新make，就生成了带有选定主题的页面。

### 评论系统

使用[Disqus](http://disqus.com/)作为评论系统，注册帐号后直接在pelicanconf.conf中添加:
```python
DISQUS_SITENAME = your_shortname
```

### 站长工具
使用[google webmaster tools](http://www.google.com/webmasters/‎)，申请之后会提示需要`sitemap`，于是需要用`pelican`的`sitemap`插件：
```sh
git clone https://github.com/getpelican/pelican-plugins
```
再在`pelicanconf.py`中加入：
```python
PLUGIN_PATH = u"pelican-plugins"

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
        "articles": "daily",
        "indexes": "monthly",
        "pages": "monthly",
    }
}
```


### To be continued
暂时就这样～ 当然还有好多东西要做，Analytics、Webmaster等等。。。
