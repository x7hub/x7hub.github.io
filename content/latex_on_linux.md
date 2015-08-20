Date: 2014-3-17
Title: Linux系统中LaTeX的安装与使用
Category: LaTeX
Tags: LaTeX, Linux
Slug: latex_on_linux


###安装

针对Archlinux，需要[TeX Live](https://wiki.archlinux.org/index.php/TeX_Live)，首先要编译LaTeX文件需要这个包`texlive-bin`，有一些图片字体之类的依赖，在这一组包里`texlive-most`。

如果想用vim或者emacs编辑LaTeX文件的话，就不需要专门的编辑器了。

Linux下的LaTeX编辑器[有很多](https://wiki.archlinux.org/index.php/Latex)，我使用的是`Kile`，KDE的组件，在Gnome和xfce下也可以正常使用，虽然不能像retext编辑Markdown那样实时预览，不过比起vim需要配置一堆插件来说还是很方便的。


###使用

LaTeX文件后缀通常为`.tex`。可以在命令行直接编译，
```sh
latex source.tex
```

用`Kile`编辑文件，可以直接通过''QuickBuild''编译生成pdf并直接打开预览。


####Helloworld

简单测试代码，很容易理解，

```latex
\documentclass[11pt]{article}
\usepackage{cite}

\begin{document}

\title{My Article}
\author{Nobody Jr.}
\date{Today}
\maketitle

Blablabla said Nobody ~\cite{Nobody06}.

\bibliographystyle{IEEEtran}
\bibliography{mybib}{}
\end{document}
```

生成的pdf是这样的，

![Hello world 的编译结果](http://7xl7ca.com1.z0.glb.clouddn.com/latex_on_linux-00.png/500px)


####使用模板

虽然语法不是太难理解，但是要自己编辑一篇文章符合投稿的各种格式需求还是相当困难的，所以要套用模板，比如[这里](http://www.ieee.org/conferences_events/conferences/publishing/templates.html)可以下载IEEE的模板，包括四个tex文件，bare_conf是会议，bare_jrnl和bare_jrnl_compsoc一个是for Computer Society Journals一个是for journals，bare_adv是Bare Advanced Demo of IEEEtran.cls for Computer Society Journals。


####插入图片

首先发表的论文中需要使用eps格式的图片的文件。matlab可以直接保存为eps格式。如果是visio图，需要先保存为pdf，再在acrobat中选择tools->print production->set page boxes->勾选remove white margins->OK，然后再保存为eps格式。

根据IEEE提供的模板，插入图片很简单，
```latex
\usepackage{graphicx}
```

```latex
\begin{figure}[!t]
\centering
\includegraphics[width=2.5in]{myfigure}
% where an .eps filename suffix will be assumed under latex, 
% and a .pdf suffix will be assumed for pdflatex; or what has been declared
% via \DeclareGraphicsExtensions.
\caption{Simulation Results}
\label{fig_sim}
\end{figure}
```

其中，`\begin{figure}[!t]`，`figure`后可以加`*`表示图片跨栏，`t`参数表示图片的位置，

* h: 直接放在目前所处位置
* t:  top，置顶
* b: bottom，置底
* p: 插入空白页之后h
* !: 让latex决定

如果要插入多张并列的一组图片，模板中提供了`subfloat`的方法，不过似乎给出的语法有误。可以用下边的方法实现，

```latex
\begin{figure*}[!t]
\centering
\subfigure[]{\includegraphics[width=1.5in]{fig2a.eps}\label{fig_moreuser_a}}
\hfil
\subfigure[]{\includegraphics[width=1.5in]{fig2b.eps}\label{fig_moreuser_b}}
\hfil
\subfigure[]{\includegraphics[width=1.5in]{fig2c.eps}\label{fig_moreuser_c}}
\caption{More users can achieve more effective network utilization in 3G/4G network}
\label{fig_moreuser}
\end{figure*}
```

####插入表格

```latex
\begin{table}[!t]
% increase table row spacing, adjust to taste
\renewcommand{\arraystretch}{1.3}
% if using array.sty, it might be a good idea to tweak the value of
% \extrarowheight as needed to properly center the text within the cells
\caption{An Example of a Table}
\label{table_example}
\centering
% Some packages, such as MDW tools, offer better commands for making tables
% than the plain LaTeX2e tabular which is used here.
\begin{tabular}{|c|c|}
\hline
One & Two\\
\hline
Three & Four\\
\hline
\end{tabular}
\end{table}
```

![插入表格](http://7xl7ca.com1.z0.glb.clouddn.com/latex_on_linux-01.png/500px)

####插入算法

算法不是用表格填写的，而是有专门的语法，很方便，
```latex
\usepackage{algorithmic}
\usepackage{algorithm}
```

```latex
\begin{algorithm}[!t]
\caption{Hello}
\label{alg_hello}
\begin{algorithmic}[1]
\WHILE {while}
    \STATE state;\
    \IF {if}
        \STATE state;\
    \ENDIF
\ENDWHILE
\end{algorithmic}
\end{algorithm}
```

![插入算法](http://7xl7ca.com1.z0.glb.clouddn.com/latex_on_linux-02.png/500px)

####插入参考文献

有两种方式。

#####thebibliography

参考模板中给出的格式，

```latex
\begin{thebibliography}{1}

\bibitem{IEEEhowto:kopka}
H.~Kopka and P.~W. Daly, \emph{A Guide to \LaTeX}, 3rd~ed.\hskip 1em plus
  0.5em minus 0.4em\relax Harlow, England: Addison-Wesley, 1999.

\end{thebibliography}
```

#####bibtex

正文中这样声明文件名，

```latex
\bibliographystyle{IEEEtran}
\bibliography{IEEEabrv,mybib}
```

创建`mybib.bib`文件，格式是这个样子的，

```bib
@misc{ Nobody06,
    author = "Nobody Jr",
    title = "My Article",
    year = "2006" }

```

可以在google scholar中生成bibtex的文件格式，cite->import into bibtex


####IEEE模板的段间距问题

在[上述地址](http://www.ieee.org/conferences_events/conferences/publishing/templates.html)下载到的模板显示是

>%% IEEEtran.cls 2011/11/03 version V1.8 based on
>
>%% IEEEtran.cls 2007/03/05 version V1.7a

这个版本的conf模板生成的pdf文件会有较大的段落间距，但是注意到现在可以检索到的IEEE的文章多数都是没有段间距的。[有人](http://blog.sciencenet.cn/blog-264887-725786.html)提到可以用另一个版本的模板代替官网上下载的版本，但是尝试后可以发现这个版本与官方版本的页边距等参数是不同的，为了避免其他问题，下面给出了避免段间距的办法。

避免分段，当需要分段时，用`\\`换行，再在下一行行首缩进固定的长度即可。

本来的分段的写法，

```latex
This demo file is intended to serve as a ``starter file''
for IEEE conference papers produced under \LaTeX\ using
IEEEtran.cls version 1.7 and later.

I wish you the best of success.
```

![有段间距](http://7xl7ca.com1.z0.glb.clouddn.com/latex_on_linux-03.png/500px)

用换行和缩进避免段间距，

```latex
This demo file is intended to serve as a ``starter file''
for IEEE conference papers produced under \LaTeX\ using
IEEEtran.cls version 1.7 and later.\\
\hspace*{0.5cm}I wish you the best of success.
```

![避免段间距](http://7xl7ca.com1.z0.glb.clouddn.com/latex_on_linux-04.png/500px)

