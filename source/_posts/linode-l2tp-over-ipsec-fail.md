---
title: 【Linode】 L2TP over IPSec 无法工作
tags:
  - linode
  - vpn
id: '639'
categories:
  - - something-about-daily-work
    - Linux
date: 2014-08-03 01:21:01
---

购买了Linode的同学，一般都会在Linode上安装部署各类技术解决方案，解决程序员的信息查找和咨询访问问题。这类方案里，本人首推使用shadowsocks，简单、轻量、稳定易用。但是在某些特殊的场合，非VPN不能解决问题。在各式各类的VPN方案里，我首推L2TP over IPSec，协议加密，内容加密，给未来还是要留个出路的，不然都被扫出来封掉，那太悲催了，我不忍细想。

如果安装的的Debian系统，那么整个部署流程会很方便愉快，但是最近这个问题，困扰我将近半年之久了，就是这个突然不工作了，多方查找才知道，是openswan版本存在bug，导致不兼容，致使L2TP over IPSec的方案无法尽功。有问题的版本如下：

```shell

# aptitude show openswan
Package: openswan
State: installed
Automatically installed: no
Version: 1:2.6.37-3+deb7u1
Priority: optional
Section: net
Maintainer: Rene Mayrhofer

```

想要恢复正常也比较简单，降级即可：

```shell

# apt-get install openswan=1:2.6.37-3

```

将openswan的版本降级后，重启IPSec，一切恢复了正常，世界清净了！

如果购买Linode，可以考虑使用我的referral code，算是对我的支持，谢谢：[f268347f24b5221e45c9a1048cb8b8db0f0c241a](https://www.linode.com/?r=f268347f24b5221e45c9a1048cb8b8db0f0c241a "f268347f24b5221e45c9a1048cb8b8db0f0c241a")