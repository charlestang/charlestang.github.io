---
title: Linux 运维：使用 ss 命令代替 netstat
tags:
  - DevOps
  - Linux
  - maintain
id: '842'
categories:
  - - 技术
    - 运维
permalink: linux-use-ss-replace-netstat/
date: 2019-07-11 17:49:42
---

在运维和管理 Linux 服务器的时候，我们最常用的一个命令就是 netstat，我常用这个命令来查看当前服务器上有哪些进程正在侦听端口，主要用来诊断网络服务的工作状态。

不过，最近有一次安装好一个 Ubuntu 发型版，发现默认没有安装 netstat，觉得非常奇怪，自己手动安装后，发现 man pages 提示，netstat 命令已经是 deprecated 了，建议使用 ss 命令代替。

> This program is mostly obsolete. Replacement for netstat is ss. Replacement for netstat -r is ip route. Replacement for netstat -i is ip -s link. Replacement for netstat -g is ip maddr.
> 
> netstat man pages

## netstat 的用法

netstat 有许多许多参数，我一般就用一种组合，以至于后来已经想不起来为什么是这几个参数了：

```shell
netstat -npl
```

得到的结果是这样的：

```generic
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      655/systemd-resolve
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      890/sshd
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      30790/cupsd
tcp        0      0 0.0.0.0:18025           0.0.0.0:*               LISTEN      890/sshd
tcp6       0      0 :::22                   :::*                    LISTEN      890/sshd
tcp6       0      0 ::1:631                 :::*                    LISTEN      30790/cupsd
tcp6       0      0 :::9090                 :::*                    LISTEN      15415/./prometheus
tcp6       0      0 :::18025                :::*                    LISTEN      890/sshd
udp        0      0 127.0.0.53:53           0.0.0.0:*                           655/systemd-resolve
udp        0      0 0.0.0.0:631             0.0.0.0:*                           30792/cups-browsed
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           757/avahi-daemon: r
udp        0      0 0.0.0.0:42360           0.0.0.0:*                           757/avahi-daemon: r
udp6       0      0 :::58232                :::*                                757/avahi-daemon: r
udp6       0      0 :::5353                 :::*                                757/avahi-daemon: r
Active UNIX domain sockets (only servers)
Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path
unix  2      [ ACC ]     STREAM     LISTENING     35116    1304/gnome-session-  @/tmp/.ICE-unix/1304
unix  2      [ ACC ]     SEQPACKET  LISTENING     1448     1/init               /run/udev/control
unix  2      [ ACC ]     STREAM     LISTENING     34277    1270/systemd         /run/user/1000/systemd/private
unix  2      [ ACC ]     STREAM     LISTENING     34282    1270/systemd         /run/user/1000/gnupg/S.gpg-agent.ssh
unix  2      [ ACC ]     STREAM     LISTENING     33510    1270/systemd         /run/user/1000/gnupg/S.gpg-agent
unix  2      [ ACC ]     STREAM     LISTENING     33511    1270/systemd         /run/user/1000/pulse/native
unix  2      [ ACC ]     STREAM     LISTENING     33512    1270/systemd         /run/user/1000/gnupg/S.gpg-agent.extra
```

最常用的就是这个命令组合，展示的结果有两个段落，第一个段落展示的是 TCP/UDP 协议的侦听情况，第二个段落展示的是 socks 文件的侦听情况。参数 n 的意思是展示数字格式的 IP 地址，不然会展示主机名称或者是域名，参数 p 的意思显示进程的名字（有时候显示不出来），l 的意思，是关注处于 LISTENING 状态的 socket。

通过如上命令，我们看到了系统所有打开的 socket，如果你启动一种网络服务也好，自己开发一个网络服务打开端口也好，通过这个命令都应该能看到自己打开的端口，如果看不到，应该就是没有能够正确打开端口，要好好查询是什么原因。所以这是一个很好用的调试命令。

## ss 的用法

上面介绍了 netstat 的最最基本的一种用法，其他用法当然还有很多，但是先略过不表，如果想使用 ss 命令来代替 netstat 的话，我们怎样达到类似的效果呢？

```shell
ss -atlp
```

这是我自己摸索的一个参数组合，目前我背诵得还不是很流利，每次还需要看一下文档：

```generic
State          Recv-Q           Send-Q                      Local Address:Port                       Peer Address:Port
LISTEN         0                128                         127.0.0.53%lo:domain                          0.0.0.0:*              users:(("systemd-resolve",pid=655,fd=13))
LISTEN         0                128                               0.0.0.0:ssh                             0.0.0.0:*              users:(("sshd",pid=890,fd=5))
LISTEN         0                5                               127.0.0.1:ipp                             0.0.0.0:*              users:(("cupsd",pid=30790,fd=7))
LISTEN         0                128                               0.0.0.0:18025                           0.0.0.0:*              users:(("sshd",pid=890,fd=3))
LISTEN         0                128                                  [::]:ssh                                [::]:*              users:(("sshd",pid=890,fd=6))
LISTEN         0                5                                   [::1]:ipp                                [::]:*              users:(("cupsd",pid=30790,fd=6))
LISTEN         0                128                                     *:9090                                  *:*              users:(("prometheus",pid=15415,fd=3))
LISTEN         0                128                                  [::]:18025                              [::]:*              users:(("sshd",pid=890,fd=4))
```

这是 ss 命令呈现出来的结果，可以看到，格式和 netstat 很不一样，不像 netstat 命令那么紧凑和直观。这是很多人诟病这个命令的原因之一。当然，批判这种批判的声音认为，人们只是死守了一种习惯，不愿前行。当然了，这么说也未尝不对，就拿 Charles 个人来说，就算我 2010 年参加工作，才学会 netstat 命令，那我到现在也使用了将近十年，从来没有变过，当然看得无比顺眼啦。

当然，也有一种理由是老外提出来的，说 ss 这个命令的名字不好，其实 ss 可能是 socket statistics 的意思，缩写以后，竟然只有两个字母，不太好联想，不像 netstat 那么直观。当然这是我的解释，不是老外抱怨的理由，他们抱怨的是，每每提及 ss，他们会联想起希特勒！是不是匪夷所思，我是 80 后，我这个年代的人，对这个都没有什么印象，关键我们用中文为主，估计大家看到 ss 最多联想到梯子，怎么都不会想到希特勒。这个大纳粹有一个武装部队，以前叫党卫队特别机动部队，后来改名叫武装党卫队。它的德语简称正是SS。

不说闲话了，说说几个参数，a 参数是显示所有的意思，t 参数意思是显示 TCP 协议的，l 代表正在 LISTENING 状态的，p 代表进程信息。从上面的表里，我们看到 p 参数打印的信息，组织得不如 netstat 精炼。但是更为完善一点，显示了进程名字和 PID 以及 FD。但是因为用了两重小括号，key/value 的格式，再加引号，看起来脏乱差。当然，我们可以用一些命令去格式化它，不过还是太麻烦了。

## 更换的原因是什么？

这可能是我最为好奇的事情。不过网上我搜索了不少的资料，基本都语焉不详。这也有点让我有点无奈。

大体上，我们能看出来，主要是 net-tools 这个包，将要被 iproute 这个包给替换。理由大概是，1，这个包太老了，2，这个包不支持很多内核新的特性（但是没有说是哪些特性），界面不够优化使用困难（对命令行不友好），3，net-tools 里面的 ifconfig 确实缺点多多，4，未来不再想维护 net-tools 了。

> Luk Claes and me, as the current maintainers of net-tools, we've been thinking about it's future. Net-tools has been a core part of Debian and any other linux based distro for many years, but it's showing its age.  
> It doesnt support many of the modern features of the linux kernel, the interface is far from optimal and difficult to use in automatisation, and also, it hasn't got much love in the last years.  
> On the other side, the iproute suite, introduced around the 2.2 kernel line, has both a much better and consistent interface, is more powerful, and is almost ten years old, so nobody would say it's untested.  
> Hence, our plans are to replace net-tools completely with iproute, maybe leading the route for other distributions to follow. Of course, most people and tools use and remember the venerable old interface, so the first step would be to write wrappers, trying to be compatible with net-tools.  
> At the same time, we believe that most packages using net-tools should be patched to use iproute instead, while others can continue using the wrappers for some time. The ifupdown package is obviously the first candidate, but it seems that a version using iproute has been available in experimental since 2007.
> 
> [https://serverfault.com/questions/633087/where-is-the-statement-of-deprecation-of-ifconfig-on-linux](https://serverfault.com/questions/633087/where-is-the-statement-of-deprecation-of-ifconfig-on-linux)

也有从[原理层面](https://utcc.utoronto.ca/~cks/space/blog/linux/ReplacingNetstatNotBad)分析的：现在的 netstat 和 ifconfig 命令，都是通过读写 /proc 目录下的虚拟文件来完成任务的，这个东西在小型业务系统上，是没问题的，但是在大规模系统里，可能会伤害系统的性能之类的。相比之下，ss 和 ip 两个命令，使用的是 Linux 内核的 netlink sockets 特性。有着根本上的不同。虽然，老命令也可以用新原理重写，但是其实并没有人那么做，主要因为不同程序员团体的一些 political issues ，大家意见不合……

当然，深层次的还有，我们使用这样的调试命令，本质上还是希望获知内核的状态的，其实，内核已经改变了 networking 模块的整个原理，另一方面我还要求命令像从前那样去展示信息，展示层面的格式和真实原理已经背离，所以，从长远看，替代这两个命令才是必然。

## 结论

咱们这些做技术的，也还是要与时俱进比较好，虽然，以前的那些命令熟悉，好用，手到擒来，甚至无法忘记，但是新的还是要保持学习。很多发型版已经默认不带有 net-tools 包了，虽然仍然可以手动安装回来，但是，这背后的态度已经很明确了。另一方面，我们做技术，也要谨防自己的大脑僵化，还是要保持对新事物的好奇心和热情。