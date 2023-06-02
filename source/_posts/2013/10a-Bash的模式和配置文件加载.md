---
title: Bash的模式和配置文件加载
tags: []
id: '593'
categories:
  - [工作相关, Linux]
date: 2013-10-29 01:23:54
permalink: bash-running-mode-and-config-files/
---

有些很基础的东西，一直以来也就没有搞懂，其实，究其原因，还是不求甚解。关于Bash的种种，便是如是。接下来，我来过一点man里面有的东西，经常看man的人，就请自动飘过吧。

Bash是shell的一种，运行中的Bash有两种属性（状态/模式），一种，是否interactive shell（交互式Shell），另一种，是否login shell（登录Shell），然后，运行中的Shell排列组合有这么几种：

1.  登录交互式Shell
2.  非登录交互式Shell
3.  登录非交互式Shell
4.  非登录非交互式Shell

关于这两种东西的定义也是非常简单明了，但是非常不容易记忆：

**交互式Shell**：没有非选项参数，没有-c，标准输入和标准输出与终端相连的，或者用-i参数启动的Bash实例。可以通过探测PS1变量是否设置或者$-返回值中是否包含字幕i来判定。

什么是没有非选项参数？比如bash ~/myscript/clear_temp_files.sh这样执行的Shell脚本的Bash实例，就不是交互式Shell，因为脚本的路径，就是非选项参数。

-c又是干什么的？就是使用一个字符串作为Bash的传入参数，比如bash -c 'ls -ahl'，这种Shell进程也不算是交互式Shell。

**登录Shell**：第0个参数以-号开头的Bash实例，或者用--login参数启动的Bash Shell。

更加诡异了，什么叫第0个参数以-号开头？你只要随便登录一个*nix系统，Mac也行，Linux也行，然后echo $0，你就明白了，惊讶吧，出来的值竟然是-bash。真的是以-号开头的！！

搞不清楚这两个东西，到底有没有什么决定性的关系呢？事实上是没有太大关系的，又一个事实是我工作四年了，还没搞清楚这点东西。I survived. No big deal. 什么时候出问题了呢？比如当你配置了一个crontab，然后你发现，我擦，为毛总是不执行呢？又然后，为啥环境变量没有呢？一般，crontab里的东西都属于运维脚本，用不着一个小开发去写，所以，你survive的机会师很大的。

好吧，我漏了很重要的一块内容没说。

就是Bash启动的时候，要加载哪些配置文件的问题。搞清楚上面两点，就可以搞清楚Bash的配置文件到底是怎么加载的。对于一个登录Shell（不管是不是交互式的）来说，一般会按照顺序加载如下四个配置文件，如果存在的话。

1.  /etc/profile
2.  ~/.bash_profile
3.  ~/.bash_login
4.  ~/.profile

对于一个交互式非登录Shell来说呢？加载的文件又不一样了：

1.  /etc/bash.bashrc
2.  ~/.bashrc

所以，我们就会搞清楚一些事情的原因。比如一个crontab的bash脚本，到底会不会执行如上的配置文件，答案是否定的。一个crontab脚本，没经过处理的话，既不是交互式Shell，也不是登录Shell，所以上面的都不会执行。

怎么处理？比如可以把shabang改一下#!/bin/bash -l让脚本用登录Shell来解释执行，就可以加载/etc/profile或者，调用Bash解释器，加-l参数也可以。看似很简单对吧。

另一个遇到的问题，为什么在Linux，我们总是配置~/.bashrc但是在Mac下，我们配置就没有用呢，要去配置~/.bash_profile才行？哈！什么情况加载~/.bashrc，上面说得很清楚了，交互式**非登录**Shell，那在Mac下，你打开Term，echo一下$0，看看，前面是不是有个-号？说明这是交互式的登录Shell，当然不会加载~/.bashrc了。实属正常。你肯定要问了，为啥Linux下没问题呢？你打开~/.profile看看就知道了，这货竟然在~/.profile文件里面source了~/.bashrc！啊！谜题都解开了～