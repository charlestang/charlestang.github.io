---
title: 用云主机安全共享开发环境数据库
tags:
  - MySQL
  - 开发环境
  - 数据库
  - 网络
id: '892'
categories:
  - - something-about-daily-work
    - PHP
  - - 小窍门
  - - 工作相关
date: 2020-03-06 03:11:09
---

![](https://sexywp.com/wp-content/uploads/2020/03/KCP-隧道搭建开发环境数据库-1-1024x707.png)

使用隧道搭建开发环境数据库

最近，我在写一个小的项目，用到了 MySQL 数据库，然后我发现一个非常烦恼的问题，我在家里电脑的本地环境改了数据库，到了办公室，代码里的变更通过 GitHub 同步过来了，但是数据库里的变更则完全没有。虽然，也有类似 Migration 之类的解决方案，但是，毕竟是密集开发的阶段，都使用 Migration 太过麻烦了。每次记住自己的操作，重放一遍，或者导出整个数据库，也一并提交到 GitHub 未尝不可，可比起一个真正的两边都能连接的开发环境数据库服务器来说，体验还是差多了。

我自己有腾讯云和阿里云的 VPS，于是就想到了何不搭一个开发环境的数据库来用呢？因为腾讯云服务器上部署了本博客，本来就有数据库，于是我就直接选择了使用腾讯云。别的云原理也是一样的。

安全起见，数据库一般都是侦听本地端口，如果在公网开放端口，则非常不安全。但是，想要从家里和办公室都能连到云端的数据库，则必须解决网络联通性的问题。

于是我想到了隧道。

通过构建隧道，可以将服务器的端口映射到本地，用起来就像在本地开了侦听端口一样。能做到这个效果的非常多，比如 SSH 就是最常见的一种隧道软件。Google 搜索能找到很多的 SSH 建立隧道的范例，本文就不赘述了。

这次我使用的是 KCP 协议隧道。我使用了 [kcptun 这个软件](https://github.com/xtaci/kcptun.git)。首先在服务器下载软件最新版本，然后，使用如下命令，开启 KCP 服务器侦听：

```shell
screen -dmS KCPSERVER ./server -l :60331 -t 127.0.0.1:3306 -key "pwd@123456" -mtu 1400 -sndwnd 2048 -rcvwnd 2048 -mode fast2
```

然后，在客户端本地，同样下载好，使用如下命令开启客户端连接：

```shell
screen -dmS KCPCLIENT ./client -l :3306 -r 128.142.11.11:60331 -key "pwd@123456" -mtu 1400 -sndwnd 2048 -rcvwnd 2048 -mode fast2
```

如此，就建立了一个从本地到服务器的连接，并将服务器的 3306 端口，映射到本地的 3306 端口，中间使用的隧道协议还是加密的，这样就不用担心被黑客扫到 MySQL 服务器的端口了。

本地数据库的配置时候，Host 填写 127.0.0.1，端口 3306，这里比较需要注意的是服务器的用户授权：

```sql
GRANT ALL ON db_dev.* TO dev@localhost IDENTIFIED BY "Dev@demo1";
```

这样写就不对了，因为一般来说，我们都在本地连接，使用 localhost 作为连接来源的 host 是没问题的，现在通过隧道转发到 server 来的连接，来源 host 到底是哪里呢？

在腾讯云的 CVM 上，我实测下来，应该使用 CVM 服务器的内网 IP 地址，怎么确认这一点呢？其实用客户端尝试连接时候，看报错就知道了。如果我们选的 host 不对，那么连接时候鉴权无法通过，从报错信息里，可以看到应该授权的 host IP 地址。

这样我就相对安全地搭建了为两个本地环境共享的云端开发环境数据库。

这里有个小的技巧，就是善用同步网盘的功能。刚才说到了 KCP 隧道需要在本地安装客户端，启动命令里是有 key 的，密钥不能提交到 GitHub 去的，这是基本常识，包括服务器的 IP 地址也不能暴露到 GitHub，那样就被黑客看到了。

所以，我用的是平时同步文件用的网盘。因为我是 Mac 系统，实际上我用的就是 iCloud，把启动客户端的命令，写在一个 shell 文件里，然后放在 iCloud 网盘上，去了办公室，直接执行就行了，可以直接连接到服务器，在本地映射出服务器上的 MySQL 端口。

另外，在服务器上，可以把启动 Server 的命令也写入一个 shell 脚本，然后配置到 crontab，每 10 分钟重复执行一次，如果 KCP 的服务器端意外退出，就会被 crontab 拉起。非常简单粗暴地实现了可靠安全的 C/S 架构隧道。