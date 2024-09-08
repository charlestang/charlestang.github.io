---
title: Aria2 在 Mac 上的使用教程
tags:
  - aria2
  - usage
categories:
  - - Mac
permalink: 2023/aria2-missing-manual/
date: 2023-09-17 23:50:00
updated: 2024-09-08 17:41:16
---
已经彻底想不起来这款软件是怎么进入我的视野的，但是，对于我这种迟钝的用户来说，仍能让我注意到，说明它至少在某个狭小的领域已经火到出圈了。

我决心认真学习一下如何使用此款软件，并把我的所得写成教程分享出来。

<!-- more -->

## Aria2 是什么？

根据[官网](https://aria2.github.io/)的介绍：

> aria2是一个轻量级的多协议和多源命令行下载工具，支持HTTP/HTTPS、FTP、SFTP、BitTorrent 和 Metalink。aria2可以通过内置的JSON-RPC和XML-RPC接口进行操作。
> 
> 核心特性：
> 
> * **多连接下载。** aria2可以从多个源/协议下载文件，并尝试利用最大的下载带宽。真正加速您的下载体验。
> 
> * **轻量级。** aria2不需要太多的内存和CPU时间。当磁盘缓存关闭时，正常的HTTP/FTP下载时的物理内存使用量通常为4MiB，BitTorrent下载时为9MiB。使用下载速度为2.8MiB/sec的BitTorrent时，CPU使用率约为6%。
> 
> * **功能齐全的BitTorrent客户端。** 所有你想要的BitTorrent客户端功能都可用：DHT、PEX、加密、磁力链接、Web-Seeding、可选择下载、本地对等发现和UDP追踪器。
> 
> * **支持Metalink。** aria2支持Metalink下载描述格式（也称为Metalink v4）、Metalink v3和Metalink/HTTP。Metalink提供了文件验证、HTTP/FTP/SFTP/BitTorrent集成和各种配置（如语言、位置、操作系统等）。
> 
> * **远程控制。** aria2支持RPC接口来控制aria2进程。支持的接口有JSON-RPC（通过HTTP和WebSocket）和XML-RPC。

上面没有说明的是，此款软件是完全免费的，使用 GPL 协议族发布。另外，该软件还是跨平台的，在 Win/Linux/Mac 上都可以运行。

当然，这款软件有一个最大的缺点，就是它是一款命令行工具，没有可视化界面，一切操作都通过终端命令和 API 执行。这个时代就是这样，没有优美的界面，你再强大，往往也会被人看成是垃圾。好在，还是有爱好者通过 RPC 接口，为其实现了简陋的 Web 版界面，不过足堪使用了。

## 如何安装

在 Mac 系统，安装是非常简单的：
```shell
brew install aria2
```
## 使用指南

### 命令行用法

对于程序员来说，这种用法并不陌生，就当成是另一个 wget，即可以正常使用。各种命令参数非常多，下载不同协议的文档时，参数也各不相同，可以使用 man 来查询手册。在 Linux 和 Win 上也是有对应的手册的。

### 服务用法

网上大量的教程，还是关于 aria2 如何作为一个守护进程来使用的说明。这等于就是大家都更愿意使用 RPC 接口提供的功能，把 aria2 当成一个下载服务器来用，并且通过“简陋”的 Web UI 来对其进行操作，当然，我们都爱图形界面。

这个软件非常小巧，只有 6M，如果没有下载任务，在内存中占用空间也非常小。再加上又可以远程操作，在本地当成一个总是启动在那里的“迅雷”，或者在远程当作一个“离线下载”，都是尚佳选择。
```shell
aria2c –enable-rpc –rpc-listen-all=true –rpc-allow-origin-all -c -D
```
上面是一个启动 aria2 服务的命令的例子，看看就可以了，实际上，没有人会这么用。因为这个就是一个普通的后台进程的启动命令，如果这个进程被杀死，或者意外退出，不会自动恢复，这条命令本身也成为一条 history，你必须找出来再敲一遍，才能恢复服务。

实际上，大家更喜欢使用配置文件来保存启动参数，也是一般的 server 启动的时候，喜欢选择的方式，这样每次启动的配置可以被妥善保存。另外，配置文件一般也会积累尽可能多的启动设定和参数。

### 配置文件

网上可以搜到很多关于 aria2 的服务如何配置的文章，这里我给出一个，是一个 Web UI 自带的说明，在[这里](http://aria2c.com/usage.html)可以查看。

### 守护服务

一般这种运行在后台的进程，叫做 daemon 进程，也叫守护进程。不过我们这里说的守护服务，是守护 daemon 的意思，aria2 这个服务启动后，我希望它永久运行，如果意外退出，也应该被拉起。

在 Linux 上，我们可以用 supervisord 来实现这个功能。现在也可以把它包装成镜像，用 Docker 的能力来实现这个功能。那么在 Mac 个人电脑上，怎么实现呢？使用 `launchd` 来拉起和守护，将 Aria2 注册成一个系统服务。

在 `~/Library/LaunchAgents` 目录里，创建一个配置文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sexywp.Aria2</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/aria2c</string>
        <string>--conf-path=/Users/charles/.aria2/aria2.conf</string>
        <string>-D</string>
    </array>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```
如上所示，然后执行命令：

```shell
launchctl load com.sexywp.Aria2.plist
```

就实现了在 Mac 上后台启动 Aria2 服务，后续配合 Web 界面或者客户端，就可以正常使用了。该服务在不工作的时候，占用资源极低，不用担心。

### Web 界面

Web 界面主要使用 JSON-RPC 和 XML-RPC 一类的协议来实现对服务的远程控制，现在甚至都不用下载和自己部署 Web 服务器，就可以通过云端的网站界面，直接连接本机的 aria2 服务，这样就变得无比方便了。

我尝试了一款[https://aria2c.com](https://aria2c.com)，打开网站后，点击扳手图标，就可以实现连接本机启动的 aria2 服务，就可以开始下载了。

如果出现了 RPC 报错的话，大家要注意一下，本地启动的 aria2 服务，默认不是 https 服务，应该使用 http，如果需要使用 https 的话，还需要专门配置。

### 客户端界面

在 Mac 上我找到了一个很[简陋的免费 UI](https://github.com/xjbeta/Aria2D)，虽然很简陋，但是基本功能也都有了。而且提供了启动客户端，就自动拉起 aria2 进程的功能，如果当作本机的下载工具用的话，再合适不过，省去了守护后台进程的麻烦，对服务器技术不过硬的小伙伴还是非常友好的。

## 使用体验

今天我体验了一下，下载了三个文件，其中一个是磁力链接。另外两个是 BT，速度都非常快，而且也比较节省资源，只不过，界面过于简陋，在 Mac 上如果当作本地的下载工具软件的话，还是远远不如 Folx 5 精美的。

但是，其可以运行在服务器上，我看不少人也是运行在路由器上，或者 NAS 服务器上，当作远程一个下载服务器来使用，在公司上班，登录自己的服务器，上传个种子就能下片了，这多爽啊。
## 总结

Aria2 是一款功能强大，全面的下载工具软件，但是其没有 UI 界面一切都通过命令行参数或者配置文件来执行，三方免费的 UI 界面也都比较薄弱，虽然使用体验不佳，但是胜在可以远程登录和操作。是路由器上和NAS上部署下载工具的一个选择。

