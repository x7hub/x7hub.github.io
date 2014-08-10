Date: 2013-09-29
Title: 在本地建立DNS缓存
Category: linux
Tags: linux, dns
Slug: local_dns

参考：

[dnsmasq - ArchWiki](https://wiki.archlinux.org/index.php/Dnsmasq)

[用dnsmasq加速你的网络!!!](http://tieba.baidu.com/p/1034963853)

### dnsmasq
Dnsmasq 提供 DNS 缓存和 DHCP 服务功能。作为域名解析服务器(DNS)，dnsmasq可以通过缓存 DNS 请求来提高对访问过的网址的连接速度。作为DHCP 服务器，dnsmasq 可以为局域网电脑提供内网ip地址和路由。DNS和DHCP两个功能可以同时或分别单独实现。dnsmasq轻量且易配置，适用于个人用户或少于50台主机的网络。此外它还自带了一个 PXE 服务器。

### 配置
* 首先安装：

```sh
pacman -S dnsmasq
```
* 修改配置文件`/etc/dnsmasq.conf`。指定用于域名查询的配置文件，反注释并修改这一行：

```
resolv-file=/etc/resolv_dnsmasq.conf
```

* 这个文件不存在啊？当然是需要自己创建的，复制前要保证`/etc/resolv.conf`是原本配置好的或者被`networkmanager`等应用自动生成的，没被修改过。
```sh
sudo cp /etc/resolv.conf /etc/resolv_dnsmasq.conf
```

### 启用

* 修改系统dns服务器地址设置。如果使用了`networkmanager`等管理网络的应用，在其中修改使用的网络连接，取消自动获取dns服务器的选框，设定`127.0.0.1`为默认dns。

* 如果没有使用，那么系统是通过直接读取用户设置的`/etc/resolv.conf`来获取dns服务器，那么直接修改这个文件即可：
```
nameserver 127.0.0.1
```

* 然后启动dnsmasq服务：
```sh
sudo systemctl start dnsmasq.service
```

### 测试

开启后测试一下：
```sh
dig g.cn
```
可以看到这么一行：
```
;; SERVER: 127.0.0.1#53(127.0.0.1)
```

这就成功了。由于使用本地的缓存，就不必担心学校的dns服务器再瘫掉导致没法上网了。或者还可以使用8.8.8.8作为dnsmasq的上游，更稳定，不过会导致解析学校的登陆网关出问题。

另外，[archwiki](https://wiki.archlinux.org/index.php/Dnsmasq#DNS_Caching)上有这么一段：
>To do a lookup speed test choose a website that has not been visited since dnsmasq has been started (dig is part of the dnsutils package):

>```
>$ dig archlinux.org | grep "Query time"
>```

>Running the command again will use the cached DNS IP and result in a faster lookup time if dnsmasq is setup correctly.

于是就试了一下：
```sh
~ % dig archlinux.org | grep "Query time"              commander@myhost pts/2 19:11 
;; Query time: 315 msec
~ % dig archlinux.org | grep "Query time"              commander@myhost pts/2 19:12 
;; Query time: 0 msec
```
确实效果明显。但是，关掉了dnsmasq并设置使用自动获取的dns服务，一样也是这样的效果，看来学校给的dns服务器也是大概使用了这种缓存机制吧。
