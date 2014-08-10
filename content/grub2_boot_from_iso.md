Date: 2012-11-25
Title: grub2直接引导iso镜像
Category: linux
Tags: linux, grub2
Slug: grub2_boot_from_iso

搬迁自[以前的新浪博客](http://blog.sina.com.cn/s/blog_76db5e270101f2an.html)～

参考：

[GRUB - ArchWiki](https://wiki.archlinux.org/index.php/Grub)

[grub2 - How to boot live iso images? - Ask Ubuntu](http://askubuntu.com/questions/141940/how-to-boot-live-iso-images)

[打造自己的多功能USB启动盘——grub2引导WinPE、Archlinux安装镜像和Ubuntu liveCD](http://forum.ubuntu.org.cn/viewtopic.php?f=139&t=393256)


### U盘准备

格式fat32，卷标 zzz。
```sh
sudo grub-install --boot-directory= --no-floppy --target=i386-pc --recheck /dev/sd
```

### 目录放置

* 考虑到方便win下使用没有分两个区。

* `/livecd`需要引导的iso镜像 不必解压  暂时只用到arch ubuntu

* `/livecd/grub`在arch中用grub-install安装的grub2文件

* `/livecd/grub4dos`用于引导windows镜像

### 配置文件

* `grub.cfg`:

```
# grub.cfg
# for livecd
# by zzz

set menu_color_normal=light-blue/black
set menu_color_highlight=light-cyan/blue

set default=0
insmod part_msdos
insmod ext2
insmod ntfs

# archlinux i686
menuentry 'Arch GNU/Linux i686' {
    set isofile='/livecd/archlinux-2012.10.06-dual.iso'
    set isolabel='ARCH_201210'
    set disklabel='zzz'
    loopback loop (hd0,1)$isofile
    linux (loop)/arch/boot/i686/vmlinuz archisolabel=$isolabel img_dev=/dev/disk/by-label/$disklabel img_loop=$isofile
    initrd (loop)/arch/boot/i686/archiso.img
}

# archlinux x86_64
menuentry 'Arch GNU/Linux x86_64' {
    set isofile='/livecd/archlinux-2012.10.06-dual.iso'
    set isolabel='ARCH_201210'
    set disklabel='zzz'
    loopback loop (hd0,1)$isofile
    linux (loop)/arch/boot/x86_64/vmlinuz archisolabel=$isolabel img_dev=/dev/disk/by-label/$disklabel img_loop=$isofile
    initrd (loop)/arch/boot/x86_64/archiso.img
}

# ubuntu 12.04
menuentry 'Ubuntu 12.04.1 LTS' {
    set isofile='/livecd/ubuntu-12.04-desktop-i386.iso'
    loopback loop $isofile
    linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=$isofile ro
    initrd (loop)/casper/initrd.lz
}

# grub4dos
menuentry 'Grub4dos' {
    linux /livecd/grub4dos/grub.exe --config-file=/livecd/grub4dos/menu.lst
}
```

* `grub4dos`配置

```
# menu.lst

color light-blue/black light-cyan/blue

title en Windows 7 x86 ultimate sp1
map (hd0,0)/livecd/en_windows_7_ultimate_with_sp1_x86_dvd_u_677460.iso (0xff)
map --hook
chainloader (0xff)
```