Date: 2013-07-29
Title: 从源码编译Android系统
Category: android
Tags: android, linux
Slug: build_android_from_source

搬迁自[以前的新浪博客](http://blog.sina.com.cn/s/blog_76db5e270101oqvu.html)～

参考：

[Android - ArchWiki](https://wiki.archlinux.org/index.php/Android)

[Initializing a Build Environment | Android Developers](http://source.android.com/source/initializing.html)

[[TUT] Configuring Arch Linux to build Android - xda-developers](http://forum.xda-developers.com/showthread.php?t=2259929)


首先在32位archlinux上尝试，最后发现必须要64位的才行。。。最后转战到ubuntu 10.04 server

### arch上的尝试：

* 系统需求，32位系统需要这么一堆东西：
```sh
gcc git gnupg flex bison gperf sdl wxgtk squashfs-tools curl ncurses zlib schedtool perl-switch zip unzip libxslt
```

64位系统还需要：
```sh
lib32-zlib lib32-ncurses lib32-readline gcc-libs-multilib gcc-multilib lib32-gcc-libs
```

* 需要`jdk6`，古董级别的，源里和AUR里都没有了，去王八壳网站[下载](http://www.oracle.com/technetwork/java/javasebusiness/downloads/java-archive-downloads-javase6-419409.html)。

* 下好了放到`/opt`下，给`x`权限，执行,安装到`/opt/jdk1.6.0_45`。
```sh
sudo chmod +x jdk-6u45-linux-i586.bin
sudo ./jdk-6u45-linux-i586.bin
```

* 然后搞`python2`，为了让系统默认`python`为`python2`，需要修改`PATH`，顺道把`java`也改了。
```sh
mkdir android-build
cd android-build
ln -s $(which python2) python
export PATH="/opt/android-build:/opt/jdk1.6.0_45/bin:$PATH"
```

* 进到源码目录，执行Google提供的设定环境变量的脚本,非让我用`bash`，`zsh`不给用。
```sh
bash
source build/envsetup.sh
```

* `lunch`，然后就杯具了。。。
```sh
/bin/bash: prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.6/bin/arm-linux-androideabi-gcc: cannot execute binary file
```
谷了一歌，说需要x64系统。。。。闹哪样 要x64你就别提供x86的包啊，唬我呢。。。

### 于是吧源码搞到服务器上去

* 装这么一堆依赖：
```sh
apt-get install git-core gnupg flex bison gperf build-essential zip curl zlib1g-dev libc6-dev lib32ncurses5-dev ia32-libs x11proto-core-dev libx11-dev lib32readline5-dev lib32z-dev libgl1-mesa-dev g++-multilib mingw32 tofrodos python-markdown libxml2-utils xsltproc
```

* 重新下载64位的王八壳的java（openjdk不让，必须oracel的），和前边一样，然后改`PATH`
```sh
export PATH="/opt/jdk1.6.0_45/bin:$PATH"
```

* 配置`ccache`
```sh
export USE_CCACHE=1
export CCACHE_DIR=/root/android-build/ccache
prebuilts/misc/linux-x86/ccache/ccache -M 50G
```

* 编译,就可以了
```sh
make -j4
```
