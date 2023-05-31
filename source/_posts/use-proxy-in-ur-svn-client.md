---
title: 给SVN客户端配置代理服务器
tags:
  - proxy
  - subversion
  - svn
id: '439'
categories:
  - - 小窍门
  - - 工作相关
  - - something-about-daily-work
    - 心得体会
date: 2011-06-13 21:39:47
---

最常见的SVN客户端其实是TortoiseSVN，我一直叫它作乌龟SVN。上班以后，我在办公室使用SVN连接非办公网络的服务器，发现无法连接，原来，是因为大多数办公网络都设置了防火墙，要连接外网的服务器，必须配置代理。如果使用的是TortoiseSVN，那么“右键”-》“Settings”-》“Networking”，就可以找到设置代理的地方：

![set proxy in tortoise svn](http://niff.home.xs4all.nl/stuff/tortoiseproxy.png)

我自己经常使用的是另一款SVN客户端，不知道国内有多少用户，总之我也提一下吧，下载的网站是这里：http://www.collab.net/，这家公司是SVN的幕后支持公司，他们开发基于命令行的各种操作系统的客户端，基于命令行，所以就非常的轻巧，最关键是装好以后，可以和NetBeans无缝集成，也不会弄一堆花花绿绿的图标在资源管理器里面，让你看了红色惊叹号凭空焦虑。

给这个命令行客户端设置代理有点纠结，看不明白的童鞋，自动忽略好了。首先打开CMD，然后键入命令echo %APPDATA%，得到的结果，就是你的配置所在的根目录，进入那个目录，然后进入Subversion子目录，你会看到两个配置文件，一个叫config，一个叫servers，用写字板编辑那个servers的配置文件：

```shell

[global]
# http-proxy-exceptions = *.exception.com, www.internal-site.org
http-proxy-host = defaultproxy.whatever.com
http-proxy-port = 7000
http-proxy-username = defaultusername
http-proxy-password = defaultpassword

```

配置好后，就可以实现给SVN客户端挂上了代理，如果只想给特定的域挂代理，就使用另一个section来配置代理：

```shell

[groups]
group1 = *.googlecode.com
# othergroup = repository.blarggitywhoomph.com
# thirdgroup = *.example.com

### Information for the first group:
[group1]
http-proxy-host = proxy.myoffice.com
http-proxy-port = 8080
# http-proxy-username = blah
# http-proxy-password = doubleblah
# http-timeout = 60

```

如上只是我的配置的一个节选，是我给googlecode这个域配置了一个代理。