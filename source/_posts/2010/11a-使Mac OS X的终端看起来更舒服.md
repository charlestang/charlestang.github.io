---
title: 使Mac OS X的终端看起来更舒服
tags:
  - DIY
  - guide
  - mac
  - tips
id: '405'
categories:
  - - 技术
    - 工具
permalink: custom-mac-os-x-terminal/
date: 2010-11-14 12:55:49
---

初次打开Mac OS X的终端，我非常不习惯。以界面优美著称的苹果操作系统，终端竟然如此丑陋，实在是大出我的意料之外。别的我也就不说了，最不能容忍的是两个，一个是没有颜色的ls，还有一个就是那个命令提示符。

实际上，Mac OS X作为一个类Unix系统，或者说根本就是一个Unix系统，而且默认shell已经变更成了bash，那么它理应该可以配置到跟Linux下的表现一样才对。在Linux系统中，ls能呈现多彩的颜色，还需要终端的支持，而Mac OS里的终端显然是支持颜色的，那为什么ls就显示不出来颜色呢？网上有老外说，ls用的不是gnu的core-utils，给了一套更换core-utils的方案，太麻烦我没采纳。今天，静心看了下man，才发现，感情人家根本就是支持彩色的。只是参数变成了-G，而不是我们熟悉的--colors，唉，竟然这么简单。

另外提一点，如果大家想要自定义Mac下的bash的表现的话，那么不要像在Linux中一样使用.bashrc，因为在Mac下起作用的其实是.bash_profile文件。好了，这里把我配置上面说的两个特性的.bash_profile分享一下。

`export PS1="\u@mac:\w > " export CLICOLOR="xterm-color" export LSCOLORS="gxfxcxdxbxegedabagacad"  # aliases alias cd..="cd .." alias l="ls" alias ll="ls -l" alias la="ls -al" alias mysql='/usr/local/mysql/bin/mysql' alias mysqladmin='/usr/local/mysql/bin/mysqladmin'`