---
title: 在Mac上使用Homebrew的时候调整PATH顺序
tags: []
id: '635'
categories:
  - - 技术
    - 工具
permalink: change-the-path-order-on-mac-to-use-brew/
date: 2014-06-27 10:36:34
---

在Mac上，管理命令行软件包，使用Homebrew，它的原理主要就是将软件安装在一个固定的目录，然后将二进制文件的路径，加入到系统的PATH中，
这样，系统就可以正确识别到命令。PATH的顺序会影响到系统搜索命令的顺序。

brew使用的/usr/local/bin默认已经在Mac系统的PATH里了，但是在最后面。通过 echo $PATH命令可以查看。

但是对于想要使用新版本的人来说，这就不方便了。所以，就要想办法调整PATH的顺序。

sudo vi /etc/paths

就可以在里面调整PATH的搜索顺序了，这个我特意去Linux系统里看了一下，不是这样的，看来是Mac系统特有的。
一般在Linux系统里调整PATH顺序都是在 .bash_profile或者 .bashrc里面，执行

export PATH=/usr/local/bin:$PATH