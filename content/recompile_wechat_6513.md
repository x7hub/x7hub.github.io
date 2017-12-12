Date: 2017-12-12
Title: 反编译微信Android客户端并重新打包
Category: Android
Tags: Android
Slug: recompile_wechat_6513

参考:

[微信安卓客户端逆向分析 by impakho](http://x-wei.github.io/pelican_github_blog.html)

[微信的二次打包 by manmade](http://www.jianshu.com/p/a0e6b3f15d78)


### 工具

* 微信版本`6.5.13`.[官方下载地址](http://dldir1.qq.com/weixin/android/weixin6514android1120.apk)，文件名叫6514，实际在应用内显示版本为6.5.13。其他相近的版本原理相似，但是由于代码混淆机制，可能对应的包名类名不同。
* Apktool `2.2.4`
* jadx `0.6.1`
* jdk `1.8.0_151`

### 反编译

如果直接默认选项反编译，那么在重新打包时会遇到资源文件错误的问题，所以尝试用`-r`参数保留资源文件。

```shell
java -jar .\apktool\apktool_2.2.4.jar  d -r .\weixin6514android1120.apk
```

反编译后的目录：

```shell
total 3057
drwxr-xr-x 1 Sec 197121   0 Dec 12 10:45 ./
drwxr-xr-x 1 Sec 197121   0 Dec 12 10:42 ../
-rw-r--r-- 1 Sec 197121  242032 Dec 12 10:42 AndroidManifest.xml
-rw-r--r-- 1 Sec 197121 379 Dec 12 10:45 apktool.yml
drwxr-xr-x 1 Sec 197121   0 Dec 12 10:45 assets/
drwxr-xr-x 1 Sec 197121   0 Dec 12 10:45 lib/
drwxr-xr-x 1 Sec 197121   0 Dec 12 10:45 original/
-rw-r--r-- 1 Sec 197121 2831616 Dec 12 10:42 resources.arsc
drwxr-xr-x 1 Sec 197121   0 Dec 12 10:44 smali/
drwxr-xr-x 1 Sec 197121   0 Dec 12 10:44 smali_classes2/
drwxr-xr-x 1 Sec 197121   0 Dec 12 10:45 smali_classes3/
```

微信相关的代码位于`smali/com/tencent/mm/`。


### 签名检查

位于`smali/com/tencent/mm/d/a.smali`中的第`793`行。

```smali
if-eqz v0, :cond_2
```

直接删掉就可以跳过检查。

### 简单修改

对代码做一些简单的修改，以打印内部日志为例。

对于日志输出的分析，参考[这篇文章](https://impakho.com/2017/02/22/wechat-android-client-hack/)。

日志类在`smali/com/tencent/mm/sdk/platformtools/v.smali`，其中的`d`、`i`等方法中，都会调用`Lcom/tencent/mm/sdk/platformtools/v$a;->getLogLevel()I`方法，猜测是在检查日志输出级别的设置，
如果我们想要输出全部级别的日志，则需要在每个日志方法中，去掉对日志级别的检查，并用`android.util.Log`打印日志到logcat。

例如在`v`方法中，第`532`行的以下代码

```smali
.line 265
sget-object v0, Lcom/tencent/mm/sdk/platformtools/v;->uqV:Lcom/tencent/mm/sdk/platformtools/v$a;

if-eqz v0, :cond_1

sget-object v0, Lcom/tencent/mm/sdk/platformtools/v;->uqV:Lcom/tencent/mm/sdk/platformtools/v$a;

invoke-interface {v0}, Lcom/tencent/mm/sdk/platformtools/v$a;->getLogLevel()I

move-result v0

const/4 v1, 0x1

if-gt v0, v1, :cond_1
```

检查loglevel如果不够`1`，则认为不该输出`v`级别的日志，就跳转到了`:cond_1`处，直接结束。

时直接将这一段判断代码删除，以跳过检查。并且，找到第597行出现了一段代码

```smali
invoke-interface/range {v0 .. v10}, Lcom/tencent/mm/sdk/platformtools/v$a;->logD(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;IIJJLjava/lang/String;)V
```

`logD`的调用明显是在输出日志内容，所以在此处插入一行

```smali
invoke-static {p0, v10}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
```

输出`v10`的内容到logcat。

对于此类中的其他日志相关的方法，同样跳过检查并插入logcat输出，就可以在打包运行时看到内部的全部日志，能直接看到聊天显示内容和网络交互等内容，信息量很大。


### 打包

直接打包可以打包成功，并且可以安装，但是运行时会秒退，根据报错信息发现是缺少了资源文件。

微信的资源文件位于`r`目录，而不是默认的`res`，在使用apktool反编译和打包的过程中出现了问题，没有将资源文件还原。一个简单的应对方案是直接将原来的`r`目录塞到打包好的apk中。

1. 使用默认选项重新打包

    ```
    java -jar .\apktool\apktool_2.2.4.jar b weixin6514android1120
    ```

    其中会遇到报错

    ```
    [Fatal Error] :1:1: Content is not allowed in prolog.
    ```

    是正常显现，并没有影响

1. 使用解压缩工具解压原本的apk文件，取出其中的`r`

1. 使用解压缩工具打开由apktool打包好的apk文件，将刚才的`r`目录直接塞到apk中并保存。

1. 签名，对齐，安装


这样修改后的微信就可以正常运行了。

### 下一步

微信的动态调试有问题，暂时只能使用插入日志的方式来调试。
