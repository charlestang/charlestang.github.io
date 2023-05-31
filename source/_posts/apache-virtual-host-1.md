---
title: Apache虚拟主机
tags:
  - apache
  - configuration
id: '380'
categories:
  - - 工作相关
date: 2010-08-01 20:55:51
---

Apache的虚拟主机是一种允许在同一台机器上，运行超过一个网站的解决方案。虚拟主机有两种，一种叫基于IP的（IP-based），另一种叫基于名字的（name-based）。虚拟主机的存在，对用户来说是透明的。
<!-- more -->
### 基于IP的虚拟主机：

对于基于IP的虚拟主机来说，必须为每个虚拟主机配备一个单独的IP。也就是说你的服务器必须有多个IP地址。对于这种方式，我们在本地就可以做一个实验来进行配置。

配置基于IP的虚拟主机，有两种方法：一是启动多个apache伺服程序，每个实例使用单独的配置文件，一般来说，在同一台机器上，架设两个网站，这两个网站互相之间不希望对方访问自己的文件，就使用这种方式，每个apache实例都是用单独的用户名，组来启动，并且放到不同的目录下，这种方式只要在apche的配置文件中，为Listen命令配置不同的ip即可；

第二种方法是只启动一个单一的apache进程，使用VirtualHost指令来为不同的站点，配置不同的值，这种配置方式，我们可以在本地做个试验的，由于127.0.0.*的所有ip都是指向本机的，所以，我们可以随便拿两个出来做实验，按照如下方式配置apache，之后，在hosts文件中，将域名绑定到配置的ip上，就可以实现在本地运行多个wp系统的一个配置：

> <VirtualHost 127.0.0.1:80>  
>     ServerAdmin yourname@domain.com  
>     DocumentRoot "E:/sexywp.com/wordpress-latest"  
>     ServerName wplatest.com  
>     ServerAlias www.wplatest.com  
>     ErrorLog "logs/wplatest.com-error.log"  
>     CustomLog "logs/wplatest.com-access.log" combined  
> </VirtualHost>
> 
> <VirtualHost 127.0.0.2:80>  
>     ServerAdmin yourname@domain.com  
>     DocumentRoot "E:/sexywp.com/wordpress-2.9.2"  
>     ServerName wpstable.com  
>     ServerAlias www.wpstable.com  
>     ErrorLog "logs/wpstable.com-error.log"  
>     CustomLog "logs/wpstable.com-access.log" combined  
> </VirtualHost>

### 基于名字的虚拟主机：

基于名字的虚拟主机比起基于IP的来说，配置要更加简单，它只要依靠客户端发送的HTTP头信息中的HOST字段来判断，服务器到底要服务哪个虚拟主机。一般情况下，还是比价推荐使用这种方式。因为IP资源日渐稀缺，对于一般用户来说，为一台服务器购买多个IP也是成本较高的。

使用这种方式配置时，首先是用NameVirtualHost指令，配置次apache实例监听的IP地址和端口号，然后使用VirtualHost指令来配置不同的虚拟主机，上述的例子，用这种方式配置的话，配置方法如下（注意，在这种方式中，ServerName是必填字段）：

> NameVirtualHost 127.0.0.1:80
> 
> <VirtualHost *:80>  
>     ServerAdmin yourname@domain.com  
>     DocumentRoot "E:/sexywp.com/wordpress-latest"  
>     ServerName wplatest.com  
>     ServerAlias www.wplatest.com  
>     ErrorLog "logs/wplatest.com-error.log"  
>     CustomLog "logs/wplatest.com-access.log" combined  
> </VirtualHost>
> 
> <VirtualHost *:80>  
>     ServerAdmin yourname@domain.com  
>     DocumentRoot "E:/sexywp.com/wordpress-2.9.2"  
>     ServerName wpstable.com  
>     ServerAlias www.wpstable.com  
>     ErrorLog "logs/wpstable.com-error.log"  
>     CustomLog "logs/wpstable.com-access.log" combined  
> </VirtualHost>

此种配置方法，也可以在本地简单地进行实验。