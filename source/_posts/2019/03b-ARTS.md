---
title: ARTS
tags:
  - algorithm
id: '822'
categories:
  - - 生活
    - 日记
permalink: arts-no-3/
date: 2019-03-08 16:32:51
---

## Algorithm

## Review

## Tips

这次的 Tips 是关于 Linux 服务器管理的，Charles 前两周，颇费周章，把自己动的第一台 MacBook Pro，安装成了 Linux 服务器，装的发行版是 Ubuntu 19.04 Desktop 版。

一个朋友跟我说，这么激进啊，我嘿嘿一笑。谁知道，今天折腾的时候，才发现自食苦果。最近几年，明显感觉到 Linux 的系统管理发展迅猛，我们小时候玩 Linux 学会的那些知识，眨眼全部作废了，真让人不胜唏嘘啊。

这次碰到的问题是 DNS 服务地址的设定问题。在我的记忆里，就是 /etc/resolve.conf 里面写一行 nameserver 指令配置一下就可以了。现在实际试下来才知道，根本不对。我无论是把里面改写了还是新增记录，一重启解析服务，里面的东西就全部还原了。

后来，我又想起来可以在 /etc/network/interfaces 里面修改配置，写是写好了，但是完全不起作用，我用 ifdown enp3s0 && ifup enp3s0 命令重启网络，还是报错无法解析。

实在不行，去官方看文档，竟然发现 Ubuntu 19.04 的服务器管理文档根本没有发布！果然，在服务器选择方面，还是不应该太激进，还是要选可靠一点的版本。现在也不可能重装了，算了吧。再给我一次重来的机会，我一定会选择 LTS。

我只能照着 18.04 LTS 版本的文档去查找和阅读了，得知在 18.04 里面引入了 netplan （[https://netplan.io/](https://netplan.io/)）这个套件来管理网络，号称用更加人性化的配置方式来管理整套网络了。怎么个人性化呢，就是选择了人类更容易读写的 YAML，好吧。

但是，我一尝试，发现 Desktop 版，根本没有安装过 netplan，虽然说配置文件的目录布局都有了，但是竟然软件没装，apt 来安装，发现——不能解析！气死我了：

```shell
# 观看 resolv.conf 的文档，顺藤摸瓜找到用 resolvectl 命令可以动态设置 DNS
resolvectl dns enp3s0 192.168.1.1
```

总算是把 DNS 给设置出来了，然后使用 apt install netplan 安装好 netplan 网络管理包。然后，我们来看看现在的 Ubuntu 的网络管理。这里发生了很多的变化，我都没法理解的，先记录在这里把。比如第一点，关于以太网设备的名字，以前我们熟悉的那套 eth0，eth1 之类的，被称作 Linux kernel 风格。现在你用 ifconfig 命令看到的是：

```generic
enp3s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.9  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::cabc:c8ff:fe8d:9d3  prefixlen 64  scopeid 0x20<link>
        ether c8:bc:c8:8d:09:d3  txqueuelen 1000  (Ethernet)
        RX packets 29433  bytes 2466486 (2.4 MB)
        RX errors 0  dropped 17848  overruns 0  frame 0
        TX packets 7051  bytes 1450602 (1.4 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 16

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 15196  bytes 1083107 (1.0 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 15196  bytes 1083107 (1.0 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

以上，我的以太网卡的名字变成了 enp3s0 ，这个名字的来源还不太懂。然后我发现，现在官方文档推荐用 ip a 命令来查看网卡了了。

```generic
○ → ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether c8:bc:c8:8d:09:d3 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.9/24 brd 192.168.1.255 scope global enp3s0
       valid_lft forever preferred_lft forever
    inet6 fe80::cabc:c8ff:fe8d:9d3/64 scope link
       valid_lft forever preferred_lft forever
```

以上，命令的结果是这样的。[1]

在 netplan 里，配置文件要好写得多:

## Share

参考文献：

1.  [https://help.ubuntu.com/lts/serverguide/network-configuration.html](https://help.ubuntu.com/lts/serverguide/network-configuration.html)