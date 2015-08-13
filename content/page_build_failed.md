Date: 2013-12-4
Title: 用Pelican构建博客上传到Github Pages出错
Category: blog
Tags: GitHub, Pelican
Slug: page_build_failed

参考：

[Using submodules with Pages](https://help.github.com/articles/using-submodules-with-pages)

### 出错情况

上次写完博客，上传Github的时候突然出问题了，现在当然已经修复。

用`pelican`和`markdown`本地编译成功，但是用`git`提交到`Github`时，收到了这么一封邮件，

>From:	GitHub (noreply@github.com) This sender is in your safe list.
>
>Sent:	Saturday, November 30, 2013 1:06:57 PM
>
>To:	x7hub (x7.0@outlook.com)
>
>The page build failed with the following error:
>
>page build failed
>
>For information on troubleshooting Jekyll see:
>
>https://help.github.com/articles/using-jekyll-with-pages#troubleshooting
>
>If you have any questions please contact us at https://github.com/contact.

错误信息就只有`page build failed`，给出的帮助链接指向的是`Jekyll`，我用的是`Pelican`啊，很苦恼啊。于是尝试了删除新添加的博文，尝试了回退到之前的版本，尝试更新系统软件，都不起作用，每次提交都会收到上面那封邮件。无奈之下求助邮件中的第二个链接，就是[Github的帮助](https://github.com/contact)。

### 求助Github

帮助页面写着，

>We’re here to help with any questions or comments. If you just want to say hi, that's cool too.

简单说明了问题以后，几分钟内就收到了答复邮件，

>Sorry about this. We are currently working on improving these error messages.
>
>The actual error found in the page build logs is as follows:
>
>No submodule mapping found in .gitmodules for path 'pelican-plugins'
>
>Please take a look at our Help article on using Git submodules with GitHub Pages:
>
>https://help.github.com/articles/using-submodules-with-pages
>
>That should help you sort out the issue.

`No submodule mapping found in .gitmodules for path 'pelican-plugins'`这个就是问题所在了。因为我的博客目录下有`pelican-plugins`和`pelican-themes`两个submodule，之前也没有在`.gitmodules`中声明，现在他们不认了。

自己也不会写`.gitmodules`，所以还是交给`git`自动添加吧，

```sh
rm -rf pelican-plugins
rm -rf pelican-themes
ga . -A
gc -m "remove 2 submodule dirs "
git submodule add  https://github.com/getpelican/pelican-plugins pelican-plugins
git submodule add  https://github.com/getpelican/pelican-themes pelican-themes
```

现在`.gitmodules`是这样的了，

```
[submodule "pelican-plugins"]
	path = pelican-plugins
	url = https://github.com/getpelican/pelican-plugins
[submodule "pelican-themes"]
	path = pelican-themes
	url = https://github.com/getpelican/pelican-themes
```

再次提交，没有收到报错的邮件，很快就在页面上看到更新了。












