---
title: 在 CentOS 6.8 上安装 Python 2.7
tags:
  - Linux
  - python
  - usage
id: '755'
categories:
  - - something-about-daily-work
    - Python
  - - 小窍门
  - - 工作相关
date: 2016-12-24 20:25:13
---

CentOS 是使用最普遍的服务器端 Linux 发行版，其主要原因还是因为 RedHat 公司出品的 RHEL 享誉盛名。很多公司目前使用的主要就是 CentOS 6.x 版本的操作系统。其实我个人不是很喜欢这个发行版，当然用了这么多年也不讨厌就是了。所以，一般朋友问我服务器装什么系统，如果对方完全不懂行的话，我会建议安装 Debian，因为既然来问我了，多数也会有跟进的问题。如果以前有一定使用经验的化，我推荐 CentOS 准没错，一般人的使用经验一般来自公司的服务器，多数就是 RedHat/CentOS/Suse 等等，用 CentOS 都是熟悉的味道。
<!-- more -->
今天帮一个朋友安装服务器，发现 CentOS 6.x 上面，竟然用的是 python 2.6，而使用 pip 的时候，提示 python 2.6 已经停止维护了，建议升级 python 2.7，搬出 yum 大法，发现，竟然提示 python27 包已经装了，可是我去 /usr/bin 和 /usr/local/bin 都找了，竟然没有 python27 的二进制，实在诡异。

于是我 yum remove python27 甚至我把 python 2.6 的包也 remove，然后执行了一下 python 命令，竟然还有，我就知道，遇到硬点子了。放狗一搜，感情在 CentOS 里，python 是深度耦合的系统组件，难怪卸载不了，而且，也不能用普通的方法升级。

```shell
sudo yum update # update yum
sudo yum install centos-release-scl # install SCL 
sudo yum install python27 # install Python 2.7

scl enable python27 bash

```

原来系统提供了工具来帮助用户能在 shell 下自然地使用 python 2.7，如上方法，对于 /usr/bin/python 这个二进制不会有任何影响的，因为是和系统深度耦合的二进制文件，当然不能动了，不过，只要用上了 python2.7，满足了应用层的需求就可以了。

总体来说，这是一个蛋疼的体验，我在知乎上发帖说 python 不会像 PHP 那么流行，部署困难就是一个主要原因，竟然被人喷成筛子，多数人一开口就是“这就是一个傻逼”的语气，有功夫先去改善改善在一个版本快速分裂向下不兼容的解释器吧。

上述的方法，只能 fork 一个新的 shell，让你用上 python 27，如果用 cron 等环境启动 python 应用，大家可以看看 virtualenv 怎么搞的。

参考：
[https://gist.github.com/dalegaspi/dec44117fa5e7597a559](https://gist.github.com/dalegaspi/dec44117fa5e7597a559)
[http://stackoverflow.com/questions/16631461/scl-enable-python27-bash](http://stackoverflow.com/questions/16631461/scl-enable-python27-bash)