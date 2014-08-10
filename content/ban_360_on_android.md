Date: 2013-08-07
Title: Android禁止安装360手机助手
Category: android
Tags: android
Slug: ban_360_on_android

搬迁自[以前的新浪博客](http://blog.sina.com.cn/s/blog_76db5e270101ozui.html)～


360太讨厌了，还老有人用我手机调试，一插他们电脑，马上就要给我装上360,于是就有了下边的招：

android程序在手机上在`/data/app/`目录下，考虑在此位置放一个360相同包名的文件，想让它安装的时候不能覆盖
```sh
adb shell
su
touch /data/app/com.qihoo.appstore-1.apk
chattr +i /data/app/com.qihoo.appstore-1.apk
```

尝试安装，软件装到手机时成功的禁止掉，但是还是能被安装到sd卡，于是采取占用`data`文件夹的方式：
```sh
adb shell
su
touch /data/data/com.qihoo.appstore
chattr +i /data/data/com.qihoo.appstore
```

再尝试安装，无论是安装到手机还是sd卡都被禁止了：
```sh
~ % adb install -s com.qihoo.appstore-1.apk
4058 KB/s (3737068 bytes in 0.899s)
        pkg: /sdcard/tmp/com.qihoo.appstore-1.apk
Failure [INSTALL_FAILED_UID_CHANGED]
~ % adb install com.qihoo.appstore-1.apk
3713 KB/s (3737068 bytes in 0.982s)
        pkg: /data/local/tmp/com.qihoo.appstore-1.apk
Failure [INSTALL_FAILED_UID_CHANGED]
```