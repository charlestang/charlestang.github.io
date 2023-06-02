---
title: 【How To】使用vsftpd在Debian Linux上搭建FTP服务
tags:
  - configuration
  - ftp
  - how-to
  - Linux
id: '514'
categories:
  - [工作相关, Linux]
date: 2012-10-09 00:55:34
permalink: how-to-config-a-ftp-service-on-debian-with-vsftpd/
---

vsftpd 是Very Secure FTPd的缩写，是一款小巧简单的ftp服务器软件，一般如果不需要对ftp帐号的流量做限制，不需要根据不同目录配置不同的属性的情况下，使用此款小巧的ftp软件，就再好不过了。vsftpd支持anonymous帐号登录和本地实体帐号登录，通过简单的配置，即可以运行。
<!-- more -->
下面就给出一个配置文件的范例，一般在个人VPS上，如此配置就已经够用了，通过这个配置，我们要实现以下目标：

*   使用独立进程模式运行vsftpd
*   禁止匿名用户登录
*   允许本地实体用户登录
*   限制登录用户的访问目录
*   禁止黑名单用户登录

以下是配置文件，在/etc/vsftpd.conf：

```ini

listen=YES
#独立进程

anonymous_enable=NO
#禁止匿名用户

local_enable=YES
#允许linux的用户登录

write_enable=YES
local_umask=022
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
xferlog_file=/var/log/vsftpd.log
connect_from_port_20=YES
#以上一些基础配置man 5 vsftpd.conf

chroot_list_enable=YES
chroot_list_file=/etc/vsftpd.chroot_list
secure_chroot_dir=/var/run/vsftpd/empty
#chroot jail，登录用户被限制在自己的Home目录中，不得出去

pam_service_name=vsftpd
#pam模块

rsa_cert_file=/etc/ssl/private/vsftpd.pem

pasv_enable=YES
#被动模式，建议开启

userlist_deny=YES
userlist_file=/etc/vsftpd.user_list
#不允许文件中的用户登录ftp

local_max_rate=100000

```

有了以上配置基本就可以正常使用了。然后就是创建本地用户了。一般来说，给自己创建一个用户，就可以正常使用了，那么要是给别人创建用户，或者作为共享ftp服务器呢，我们可能希望创建一个不能login到Server的用户，就是我们常说的nologin用户。

`adduser --shell /usr/sbin/nologin ftpuser`

可以创建一个无法使用ssh登录系统的用户，但是可以用这个ftpuser登录ftp。我这样做了以后，发现服务器始终是530错误。这到底是什么原因呢，放狗一搜，发现很多人提到了pam模块的问题，甚至有人说，只要去除了pam模块，就可以了。我觉得不至于这么绝对，肯定还是配置没搞对的问题。

pam是Pluggable Authentication Modules for Linux的缩写，说白了，就是一个外挂身份校验工具。研究了位于/etc/pam.d/下的文件vsftpd，

```conf

authrequiredpam_listfile.so item=user sense=deny file=/etc/ftpusers onerr=succeed

# Note: vsftpd handles anonymous logins on its own. Do not enable pam_ftp.so.

# Standard pam includes
@include common-account
@include common-session
@include common-auth
authrequiredpam_shells.so

```

我对最底下一行产生了怀疑，使用man pam_shells查了后发现，这个东西是查看用户是不是有合法shell的一个校验，有两种做法，一，删除这行（没验证，理论推测），二，根据文档里写的，让它能够通过/etc/shells文件校验shell合法性就行了。刚说了我创建了nologin用户，一看，/usr/sbin/nologin果然不再/etc/shells文件中，加进去，一切太平了。