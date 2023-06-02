---
title: 在WinXP上搭建自己的SVN服务器
tags:
  - server
  - subversion
  - usage
id: '353'
categories:
  -   - 工作相关
date: 2009-07-21 20:47:49
permalink: how-to-make-a-easy-svn-server/
---

本文将介绍一个最为简略的搭建SVN服务器的方法。
<!-- more -->
经常要开发一些小项目，实验室里没有统一的文件服务器和版本库，那么只好自己动手来搭建一个。

推荐使用[http://www.open.collab.net/](http://www.open.collab.net/ "http://www.open.collab.net/")提供的SVN，服务器和客户端软件包一共只有11M。是全命令行的界面。

在页面：[http://www.open.collab.net/downloads/subversion/](http://www.open.collab.net/downloads/subversion/ "http://www.open.collab.net/downloads/subversion/")

下载：CollabNet Subversion Server and Client v1.6.3 (for Windows) 下载的时候请选用最新版本，一般来说更新得非常勤快的。

下载后双击安装，安装过程中会提示，是否把svn安装成service，选是。

安装完成后，可以检查一下svnserver是否已经启动。

检查方法为进入控制台（开始-->运行-->cmd），输入命令

netstat –an

看看Listen列表里是否在监听3690端口，如果已经在监听了，说明svn服务器已经启动，如果没有启动的话，进入“控制面板”-->“管理工具”-->“服务”，找到CollabNet Subversion，然后点启动。（按照我的理解，这项服务应该在重启计算机后自动启动的，但是不知道为什么，我的没有自动启动，只好手动启动一下。）

到此，服务器已经安装完成了。

按照安装过程中的设置，会在你的磁盘上生成一个svn_repository的目录，从命令行进入该目录，输入命令

svnadmin create my_repository

就会建立一个版本库。

然后进入该版本库，进行配置。进入conf目录，有三个文件需要配置

svnserve.conf

> [general]  
> ### These options control access to the repository for unauthenticated  
> ### and authenticated users.  Valid values are "write", "read",  
> ### and "none".  The sample settings below are the defaults.
> 
> anon-access = read  
> auth-access = write
> 
> ### The password-db option controls the location of the password  
> ### database file.  Unless you specify a path starting with a /,  
> ### the file's location is relative to the directory containing  
> ### this configuration file.  
> ### If SASL is enabled (see below), this file will NOT be used.  
> ### Uncomment the line below to use the default password file.
> 
> password-db = passwd
> 
> ### The authz-db option controls the location of the authorization  
> ### rules for path-based access control.  Unless you specify a path  
> ### starting with a /, the file's location is relative to the the  
> ### directory containing this file.  If you don't specify an  
> ### authz-db, no path-based access control is done.  
> ### Uncomment the line below to use the default authorization file.
> 
> authz-db = authz

这个文件有若干的选项，上文中引用的部分为比较基本的几个选项，主要是控制访问权限的。

authz

[/]  
sexywp = rw  

password

[users]  
sexywp = 123456  

另外两个文件分别是authz和password，里面的内容如上述。主要的含义是创建了一个用户，名字为sexywp，其密码为123456，对整个版本库的根目录有读写权限。

至此，服务器端的版本库已经建立完毕了。下一个步骤就是把项目代码导入到版本库了。

导入版本库非常简单，可以从服务器端导入，使用import命令，也可以从客户端导入，我接下来介绍一下从客户端导入。

首先找到一个目标目录，你要在这里管理你的代码，比如E:/MyProject目录下，然后执行命令

svn checkout svn://localhost/my_repository --username sexywp --password 123456  

然后，你就会得到一个my_repository的空目录，进入后，里面有一个.svn的隐藏目录，除此之外，没有任何其他的东西了。

你可以在这个目录里建立好你版本库的结构，比如，我会建立三个目录trunk，branches，tags（使用svn mkdir命令），然后，将项目代码拷贝到trunk目录下，然后执行

svn commit –m “first version”

命令，将所有代码导入到服务器的版本库。