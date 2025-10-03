---
title: 如何配置RHEL的iptables开放端口
tags:
  - ftp
  - iptables
  - Linux
  - rhel
id: '460'
categories:
  - - 技术
    - 运维
permalink: how-to-config-iptables-on-rhel/
date: 2011-10-02 11:53:47
updated: 2025-10-03 01:19:09
---

要给一个朋友的服务器上架设ftp，一看，这哥们的服务器装的是RHEL AS4，看到这个发行版的名字，我就发怵了，果不其然，么有包管理器，我简直寸步难行，什么软件都没法装，各种依赖，太难解决了！！

看了一下已经安装的软件列表，发现已经装了vsftpd，就用这个吧，man了半天，最后配好了，但是一连，发现死活连不上，百思不得其解，各种google，各种百度，也不知道过了多少天，才发现问题的症结在iptables，原来，要使用passive mode登陆ftp，必须开一个范围的端口，而系统默认的iptables规则，不允许对这些端口的访问，导致ftp连不上。怎么开放iptables的端口呢？又是各种google，各种百度，搜到一个iptables的tutorial，竟然有290页之厚，太难用了。

几经周折又找到了一个图形化系统界面可以配置防火墙规则的，system-config-securitylevel-tui，通过这个东西，很容易就可以开放一个端口，但是这个东西也有问题，我要开10000号段的端口100个，就麻烦了，虽然网上说，用格式形如10000-10100:tcp这样的写法可以开放一个系列的端口，但是实际上，这么写是不管事的，也不知道是不是软件的版本的问题。

最后，知道这个ui界面生成的规则被写到了/etc/sysconfig/iptables文件里面，然后又看了一下man，研究了一下如果手动配置规则的话，端口范围的写法（--dport 10000:10100），先用ui工具生成一条一个端口的规则，然后手动改文件，将端口改成范围，一重启，发现终于一切都按照预期的搞定了，真是累死我了。

在RHEL下面，启动，重启，关闭，查询iptables状态的方法：

Usage: /etc/init.d/iptables {startstoprestartcondrestartstatuspanicsave}