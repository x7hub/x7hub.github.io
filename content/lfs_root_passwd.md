Date: 2013-01-22
Title: LFS编译shadow之后设置root密码出错解决
Category: linux
Tags: linux, lfs
Slug: lfs_root_passwd

搬迁自[以前的新浪博客](http://blog.sina.com.cn/s/blog_76db5e270101hvh1.html)～

按照[lfs book](http://www.linuxfromscratch.org/lfs/download.html)编译安装配置`shadow`之后没法修改root密码：

```
root:/sources/shadow-4.1.5.1# passwd root
Changing password for root
Enter the new password (minimum of 5 characters)
Please use a combination of upper and lower case letters and numbers.
Bad password: too short.  
Warning: weak password (enter it again to use it anyway).
passwd: password changed.
```

不给输密码的机会，直接跑过去了。经过反复重新解包编译安装… 最后才发现错误原因：

之前重启过host，重新进入chroot之前忘记挂载系统虚拟文件了。

```
root@ant-arch /media/lfs # mount -v --bind /dev dev                pts/0 19:28
mount: /dev binded on /media/lfs/dev
root@ant-arch /media/lfs # mount -vt devpts devpts dev/pts         pts/0 19:28
mount: devpts mounted on /media/lfs/dev/pts
root@ant-arch /media/lfs # mount -vt proc proc proc                pts/0 19:28
mount: proc mounted on /media/lfs/proc
root@ant-arch /media/lfs # mount -vt sysfs sysfs sys               pts/0 19:28
mount: sysfs mounted on /media/lfs/sys
root@ant-arch /media/lfs # mount -vt tmpfs shm dev/shm             pts/0 19:28
mount: shm mounted on /media/lfs/dev/shm
```

然后再chroot，修改密码，一切正常了：

```
root@ant-arch /media/lfs # chroot /media/lfs /tools/bin/env -i \   pts/0 19:29
HOME=/root \
TERM="$TERM" \
PS1='\u:\w\$ ' \
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin \
/tools/bin/bash --login +h
root:/# passwd root
Changing password for root
Enter the new password (minimum of 5 characters)
Please use a combination of upper and lower case letters and numbers.
New password:
Bad password: too simple. 
Warning: weak password (enter it again to use it anyway).
New password:
Re-enter new password:
passwd: password changed.
root:/#
```
