---
title: 在Linode上安装Debian 7+Nginx+MySQL+PHP FastCGI
tags: []
id: '572'
categories:
  - - 技术
    - 运维
permalink: linode-initialize/
date: 2013-07-11 01:39:53
---

在我印象里，我大概做了许多次这个事情了，拿到一台新的Linode，或者将某个Linode实例彻底清空而变成新的Linode，然后从0开始装成一个Web Server。本文，我就记录一下这个过程吧，省得以后用到了，又去各个服务器上拷贝。
<!-- more -->
## Linode

Linode是我到目前为止用过的最好的VPS服务，没有之一。

1.  服务稳定，间断少，一年也就一两次，时间很短；
2.  服务器在国外，可以当梯子用；
3.  流量够大2T；
4.  除了价格贵，基本没缺点，$20一个月，年付9折；

Linode有很方便的管理后台，拿到一台最弱的Linode实例，上去首先装系统，Deploy a Linuy Distribution，然后，选择64位系统里的Debian 7，纯粹个人喜好，CentOS也是很好的发行版，只是我比较喜欢Debian，熟悉、容易、稳定。一开始，虚拟的磁盘应该有20多G，让你填写两个东西，一个是SWAP分区的大小，另一个是root密码。SWAP的大小，是三个选项，1G内存，建议选择512M的SWAP。root密码，你就网死里复杂吧，然后一定找个小本记下来，因为用得不多，肯定会忘记。

## SSH登录

首先要搞定ssh登录，因为我用Mac，我就只描述Mac的做法了。第一次没法子的，必须手动输入密码的，

```bash
ssh root@123.123.123.123
```

然后，键入你那个超级复杂的密码。

然后，你需要做的是，做好今后的免密码登录，省得背密码。前提是必须在自己常用的机器上，比如笔记本，比如公司的办公机。以Mac为例，在命令行执行：

```bash
ssh-keygen -t rsa -b 2048
```

生成一个2048位长的公私钥对，生成过程中，问你paraphrase，你就填空，否则还是要输入密码的。

生成完毕后，你在.ssh目录里，会看到两个文件，一个是id_rsa.pub，另一个是id_rsa。然后你打开id_rsa.pub，会看到这么一段东西：

```shell
ssh-rsa bbbbB3NzaC1yc2EAAAADAQABAAABAQDGEyRW/mF1dVPFLGRV6nBBIKGBznyRgM2A/fWtjumY/rkdG1WxVhrIklXm1YsUPd1kRc+dWF2mxVom/81+QJc8947595rneriueiritkRTxIKDB4VOERGidi+WNbwoqVs7hRQ06wK9Sn4UPS9nwbm08mZQxtPUxUtNHK2395908437eCZuRPZyTuKto5o4MVEFZkLeuZOwKILH0Eet2F72Vnr4wQ9YRrDrJGAuaQ7q4LpiI6vpgYpvBODVXictTkeHaoO5FYuh4ndfgyRd2gPqmEpBb6n6OznM1laDZY/2kCNrkZbyxF2nmbeSIhdBIMb charles@TCRMBP.local

```

在你服务器上，~/.ssh目录里面（不存在就创建），的authorized_keys文件（不存在就创建）里，加上1行，就是上面的东西。然后，你以后再ssh你的服务器的时候，就会直接登录进去。

## source.list

不得不说，当你的服务器在美国的时候，你会发现，原来服务器的使用是这么方便的一件事情，原来那么多软件包，都触手可得，原来网络速度是如此之快，原来官方网站是如此值得信赖，恶劣的，紧紧只我朝的网络环境而已。

如果你在服务器上安装Debian的话，你会发觉，完全没有必要去特意配置什么source.list，用操作系统自带的足以，连接官方源足够。不过，在Debian源中，一般的软件，为了追求稳定，版本更新速度都很慢，近些年已经有所转变了，跟我初次使用时候不同了。但是在Web服务这个领域，Debian的软件包仍显保守，如果只是自己玩玩，追求新版本，学习新特性的话，我建议，使用dotdeb.net这个网站提供的源，致力于Web开发，始终维护着Nginx，Apache，PHP，MySQL最新的版本，并将互相之间的配合做好测试。

使用root打开/etc/apt/source.list文件，然后加入：

```bash

deb http://packages.dotdeb.org wheezy all
deb-src http://packages.dotdeb.org wheezy all

```

然后，执行

```bash

wget http://www.dotdeb.org/dotdeb.gpg
cat dotdeb.gpg  sudo apt-key add -

```

如此，就算添加好了dotdeb的源，执行apt-get update && apt-get safe-upgrade，就可以将系统的软件包更新了。

## shell设置

在Debian系统中，不知道什么，明明有很好用的功能，但是默认都是不支持的。比如Bash Completion，找到bash的总配置文件/etc/bash.bashrc

```shell

# 下面这段取消注释
# enable bash completion in interactive shells
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# 增加下面这段，看文档的时候，增加红色和绿色
# man color
export LESS_TERMCAP_mb=$'\E[01;31m'
export LESS_TERMCAP_md=$'\E[01;31m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;44;33m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[01;32m'

```

## vim

如果你在虚拟机上安装Debian，那默认带的是vim-tiny这个非常不好用，马上执行：

```shell

aptitude purge vim-tiny
aptitude install vim

```

如此装上vim的完整版，这至关重要。

然后是vim的语法高亮默认不开的，去/usr/share/vim/vimrc中，设置syntax on，这样，以后就都有语法高亮了。不过，默认颜色不好看的话，你可以安装solarized。我就不讨论那个了。

## Nginx+PHP+MySQL

安装Nginx和PHP，因为我们要使用Nginx ＋ FastCGI的形式来架设web服务，所以，我们不能安装php5这个软件包，会把整个apache都给装上的。

```shell

aptituge install nginx php5-cli php5-fpm php5-apc php5-curl php5-gd php5-imagick php5-mysqlnd

```

有以上这些包，已经差不多了。



写得我累死了，未完待续……