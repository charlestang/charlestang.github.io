---
title: 使用 certbot 申请 Let's Encrypt 的免费 SSL 证书
tags:
  - HTTPS
  - SSL
  - TLS
id: '763'
categories:
  - - 技术
    - 运维
permalink: use-certbot-apply-letsencrypt-certificate/
date: 2017-02-01 00:25:55
---

2016 年 4 月 12 日，Let's Encrypt 宣布，免费为广大网站提供 SSL 证书，从此，再也没有必要使用自签名证书了。本站也很早就用上了 Let's Encrypt 提供的免费证书，那时候，还是使用的网友实现的 Python 脚本来进行的申请，后来，官方推出了官方客户端，也是 Python 实现的，我也懒得更换了。

这次，我突然遭遇了一次证书失效，（当然事后证明不是那么回事），怀疑到了非官方的证书申请客户端，并更换了官方推荐的形式，才发现，原来官方提供了这么好用的一个工具——certbot。所以，特此介绍给大家。
<!-- more -->
[certbot](https://certbot.eff.org/) 就是上篇文章说的 EFF 推出的一个客户端软件，使用 Ptyhon 写成的，在特定的软件环境下，基本可以做到全自动申请和部署 SSL 证书。首先是安装，如果有包管理器，可以尝试搜索 certbot，认准 EFF 出品，如果没有的话，可以用 wget 下载安装：

```shell
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto

```

建议安装到 /usr/local/bin 或者 ~/bin 目录下，这样以后执行的时候可以不用打完整路径。如果 Web Server 用的是 Apache 的话，基本上不用任何参数，可以完成全部的申请、配置、重启了，但是我没试过，因为我用的是 Nginx，不过也一样很好用了。使用的 Nginx 的时候，要加一个指令，叫 certonly，就是只申请证书，不进行自动部署。

```shell
./path/to/certbot-auto certonly --webroot -w /var/www/example -d example.com -d www.example.com -w /var/www/thing -d thing.is -d m.thing.is

```

上面的例子来自官方文档，意思是，只申请证书，使用一个叫 webroot 的插件，-w 的意思是你的网站的根目录是什么，-d 的意思是你申请的证书的域名，这两个参数都可以多次出现，也就是你可以一次性为多个网站域名申请证书。执行上面的指令，基本上，证书就会申请完毕。

证书申请完毕后，会在你的 /etc/letsencrypt 目录下，建立起一个目录结构，里面有几个文件夹，最重要的是 live 文件夹，里面有以你的域名命名的文件夹，里面放的就是证书和 key。你观察一下会发现，这些文件都已经是软链了，其实 certbot 脚本自动把证书和 key 都放在一个叫 archive 的归档文件夹里，我想，这是因为证书只有三个月有效，所以续期的时候会再次申请，干脆把所有证书都归档了，这样可以随意回溯历史的证书版本。想得还是比较周到的。

光是申请证书方便的话，我觉得也没什么了不起了，证书只有三个月有效期，使用 certbot 进行证书续期也超级方便的。竟然提供了一个测试续期的执行方式，和真正续期的执行方式。

```shell
# 测试续期功能是否正常
./path/to/certbot-auto renew --dry-run

# 真的续期
./path/to/certbot-auto renew --quiet --no-self-upgrade

```

可以无害地执行上面的脚本，测试是否可以正确续期，有比较友好的 log 能够调试所有的错误。如果都没问题了，把下面的真正执行，配置到 cron 里面，一个月执行一次就可以了。

可以创建一个这样的脚本，并且把脚本放到 /etc/cron.monthly 文件夹下，就可以实现每月一次续期证书：

```shell
#!/bin/bash
/root/bin/certbot-auto renew --quiet --no-self-upgrade

```