Date: 2013-06-21
Title: hadoop on archlinux
Category: linux
Tags: linux, hadoop
Slug: hadoop_on_archlinux

搬迁自[以前的新浪博客](http://blog.sina.com.cn/s/blog_76db5e270101nu7o.html)～


参考：

[Hadoop - ArchWiki](https://wiki.archlinux.org/index.php/Hadoop)

[Single Node Setup](http://hadoop.apache.org/docs/stable/single_node_setup.html)


* 安装：

```sh
yaourt hadoop
```

* 主要目录是这个：
```sh
/etc/hadoop/
```

* 当然配置文件还是在这里。
```sh
/etc/hadoop/
```

* 检查java环境配置。
```sh
echo $JAVA_HOME
```

* 安装时生成了rsa密钥一对，还需要将本地用户的公钥添加到`/etc/hadoop/.ssh/authorized_keys`,用于`ssh`验证。

* 格式化新的分布式文件系统
```sh
hadoop namenode -format
```

* 启动服务,需要防火墙打开`9000`和`9001`端口，即使单机hadoop也需要，不明
```sh
bin/start-all.sh
```
或者启动`systemd`的一排service

* 启动后运行example测试，首先把测试用的文件写到`hadoop fs`
```sh
hadoop fs -put /etc/hadoop input
```

* 运行测试
```sh
hadoop jar /usr/lib/hadoop/hadoop-examples-*.jar grep input output 'dfs[a-z.]+'
```

* 查看结果
```sh
hadoop fs -get output output
cat output/*
```