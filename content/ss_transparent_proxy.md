Date: 2017-12-12
Title: 利用shadowsocks在树莓派上搭建科学上网透明代理
Category: Linux
Tags: Linux
Slug: ss_transparent_proxy


效果是手机连接树莓派的wifi热点时，不需要任何设置，可以直接访问墙外网站，而且不影响对国内直连网站的访问速度。

用到的工具：shadowsocks-libev，simple-obfs，ipset，iptables，chinadns，bind9，create_ap



参考:

[Advanced usage by shadowsocks](https://github.com/shadowsocks/shadowsocks-libev#advanced-usage)

[绕开网络封锁访问敏感域名 by whiler](https://github.com/whiler/whiler.github.io/blob/master/articles/bypass.md)


### 原理

简单的iptables配置就可以满足全部流量直接走shadowsocks，但是这样对国内网站（包括cdn等）也会绕道国外，造成访问速度会大大下降。

* 首先是dns问题，如果完全使用谷歌的dns解析，一些国内网站的地址会解析到其国外的备份。chinadns是一个dns工具，用他来实现国内外dns同时查询，对于需要科学上网的网站，才使用谷歌的解析。

* 另外是根据ip分流的问题，国内外不同的目的地址，分别走默认的路由和shadowsocks提供的代理。[APNIC](http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest)提供了一个ip地址段和其对应的国家地区的列表，通过ipset配合iptables来实现分流。

### 服务器搭建

服务器就是普通的ss-server，此处使用了`shadowsocks-libev`+`simple-obfs`的方案。

对于Debian 9 的服务器，直接按照官方文档安装`shadowsocks-libev`。

> For Debian 9 (Stretch) users, please install it from stretch-backports: We strongly encourage you to install shadowsocks-libev from stretch-backports. For more info about backports, you can refer Debian Backports.
> 
>     sudo sh -c 'printf "deb http://deb.debian.org/debian stretch-backports main" /etc/apt/sources.list.d/stretch-backports.list'
>     sudo apt update
>     sudo apt -t stretch-backports install shadowsocks-libev

同时安装插件`simple-obfs`用于混淆流量，躲避探测。

```shell
sudo apt -t stretch-backports install simple-obfs
```

修改配置文件`/etc/shadowsocks-libev/config.json`，配置如下，这里使用8080端口是为了配合`simple-obfs`用。

```json
{
    "server":"<YOUR_IP_OR_HOST_HERE>",
    "server_port":8080,
    "local_port":1080,
    "password":"<YOUR_PASSWORD_HERE>",
    "timeout":60,
    "method":"aes-256-cfb",
    "plugin":"obfs-server",
    "plugin_opts":"obfs=http;failover=127.0.0.1:8081;fast-open"
}
```

obfs配置的failover是一个用于混淆流量的http服务器，如果是个能通的地址会伪装得更好。

对于Debian服务器，使用systemd来控制后台开启。

```shell
sudo systemctl start shadowsocks-libev.service
```

至此服务器配置完成。已经可以支持客户端来连接，包括Windows、Android、MacOS等平台的工具。


### wifi热点

使用树莓派3作为网关。树莓派3有一个以太网接口，和一个内置的wifi芯片，可以使用以太网连接外网，用wifi开启热点供手机上网。

简单的脚本工具[create_ap](https://github.com/oblique/create_ap)提供了方便的热点配置方案。默认会安装到`/usr`目录。

```
git clone https://github.com/oblique/create_ap
cd create_ap
sudo make install
```

配置文件

```
CHANNEL=1
GATEWAY=192.168.12.1
WPA_VERSION=2
ETC_HOSTS=0
DHCP_DNS=192.168.12.1
NO_DNS=1
NO_DNSMASQ=0
HIDDEN=0
MAC_FILTER=0
MAC_FILTER_ACCEPT=/etc/hostapd/hostapd.accept
ISOLATE_CLIENTS=0
SHARE_METHOD=nat
IEEE80211N=0
IEEE80211AC=0
HT_CAPAB=[HT40+]
VHT_CAPAB=
DRIVER=nl80211
NO_VIRT=1
COUNTRY=
FREQ_BAND=2.4
NEW_MACADDR=
DAEMONIZE=0
NO_HAVEGED=0
WIFI_IFACE=wlan0
INTERNET_IFACE=eth0
SSID=MyAccessPoint
PASSPHRASE=12345678
USE_PSK=0
```

其中关键是`DHCP_DNS`，这里把手机上网时分配的
地址是网关的地址，为了下一步科学上网时使用chinadns来区分国内外服务器。

启动

```shell
sudo systemctl start create_ap.service
```

### 科学上网

#### shadowsocks

树莓派作为客户端，同样先安装`shadowsocks-libev`和`simple-obfs`，安装方法和服务器相同，或参考官方文档。

客户端的配置文件位于`/etc/shadowsocks-libev/tiny.json`，文件名是自定义的，在systemd启动时可以指定。

```json
{
    "server":"<YOUR_IP_OR_HOST_HERE>",
    "server_port":8080,
    "local_address":"0.0.0.0",
    "local_port":1080,
    "password":"<YOUR_PASSWORD_HERE>",
    "timeout":60,
    "method":"aes-256-cfb",
    "plugin":"obfs-local",
    "plugin_opts":"obfs=http;obfs-host=www.bing.com"
}
```

用systemd启动`ss-redir`，`@`后的参数为对应的配置文件名.

```shell
sudo systemctl start shadowsocks-libev-redir@tiny.service
```

#### ipset

下载并分析得到国内ip的范围，对于这些ip需要跳过shadowsocks的转发。

```shell
curl 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' | grep ipv4 | grep CN | awk -F\| '{ printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > chnroute.txt
```

修改得到的`chnroute.txt`文件，第一行加入

```shell
ipset -N chnroute hash:net maxelem 65536
```

后续每行都修改为ipset命令，修改完成后的文件如

```shell
ipset -N chnroute hash:net maxelem 65536
ipset add chnroute 1.0.1.0/24
ipset add chnroute 1.0.2.0/23
ipset add chnroute 1.0.8.0/21
ipset add chnroute 1.0.32.0/19
ipset add chnroute 1.1.0.0/24
```

保存为`chnroute.sh`并执行。

这一步的作用，是将向国内的ip的流量，加上了`chnroute`的标签，以供下一步iptables的配置来识别。

如果需要实现开机启动，可以导出和导入ipset的指令

```shell
sudo ipset save > /etc/iptables/ipset.conf
sudo ipset restore < /etc/iptables/ipset.conf
```

#### iptables

添加iptables在`nat`链的规则，将部分流量直接输出，剩余的全部接入到shadowsocks的代理中。需要直接输出的ip规则包括：

- shadowsocks服务器
- 内网
- 国内

```shell
sudo iptables -t nat -N SHADOWSOCKS
sudo iptables -t nat -A SHADOWSOCKS -d 45.76.241.35 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 97.64.104.145 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 0.0.0.0/8 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 10.0.0.0/8 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 127.0.0.0/8 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 169.254.0.0/16 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 172.16.0.0/12 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 192.168.0.0/16 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 224.0.0.0/4 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -d 240.0.0.0/4 -j RETURN
sudo iptables -t nat -A SHADOWSOCKS -p tcp -m set --match-set chnroute dst -j RETURN
sudo iptables -t nat -A PREROUTING -p tcp -j SHADOWSOCKS
sudo iptables -t nat -A OUTPUT -p tcp -j SHADOWSOCKS
```

#### chinadns

安装参考[官方文档](https://github.com/shadowsocks/ChinaDNS)

```shell
wget https://github.com/shadowsocks/ChinaDNS/releases/download/1.3.2/chinadns-1.3.2.tar.gz
tar xvf chinadns-1.3.2.tar.gz
cd chinadns-1.3.2
./configure
make
sudo cp src/chinadns /usr/local/bin
```

另外还要用到刚才下载的chnroute.txt文件，用来区分国内外地址。

```shell
sudo cp ~/Download/chnroute.txt /usr/local/etc
```

创建一个systemd服务，配置文件位于`/usr/lib/systemd/system/chinadns.service`

```shell
[Unit]
Description=ChinaDNS Service
After=network.target

[Service]
Type=simple
User=nobody
ExecStart=/usr/local/bin/chinadns -m -c /usr/local/etc/chnroute.txt -b 127.0.0.1 -p 5353 -s 219.141.140.10,219.141.136.10,8.8.8.8

[Install]
WantedBy=multi-user.target
```

其中参数`-s`指定多个dns服务器，前几个为运营商提供的默认dns，最后一个填写国外可靠的谷歌dns用于查询国外网站。

```shell
sudo systemctl restart chinadns.service
```

启动服务，这里将chinadns的端口放在5353，是为了再用bind9或dnsmasq等工具做一层dns缓存。

以bind9为例。

修改配置文件`/etc/bind/named.conf.options`，将上游地址制定到chinadns配置的5353。

```
options {
    directory "/var/cache/bind";
    forwarders {
        127.0.0.1 port 5353;
    };
    forward only;

    dnssec-enable no;
    dnssec-validation no;

    auth-nxdomain no;    # conform to RFC1035
    listen-on-v6 { any; };

    recursion yes;                 # enables resursive queries

};
```

启动bind9服务

```shell
sudo systemctl start bind9
```


### 完成

自此，手机只需要连接热点即可实现科学上网。

由于使用了混淆机制，如果手机再独立使用shadowsocks连接另外的服务器，会造成多次混淆，可能会使网速大减。
