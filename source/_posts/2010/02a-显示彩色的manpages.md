---
title: 显示彩色的manpages
tags:
  - color
  - Linux
  - man
  - manpages
  - usage
id: '360'
categories:
  - [工作相关, Linux]
date: 2010-02-06 22:35:16
permalink: show-colorful-manpages/
---

man是Linux下最最常用的命令之一，用来显示某个命令的手册。

一般在命令行下，manpages通过粗体和下划线来标记关键信息，有多种方法来使man命令显示彩色的manpages。

man是调用less来显示manpages的，可以更换这个程序，使用most来显示，这是一个方法。但是长期以来使用less，已经习惯，most又有一套操作方法，后来我又发现了一种方案，非常简单，只要通过在bashrc中设定环境变量，就可以高亮彩显manpages，非常方便。

设定方法如下，在.bashrc末尾添加如下几行：
`export LESS_TERMCAP_mb=$'\E[01;31m' export LESS_TERMCAP_md=$'\E[01;31m' export LESS_TERMCAP_me=$'\E[0m' export LESS_TERMCAP_se=$'\E[0m' export LESS_TERMCAP_so=$'\E[01;44;33m' export LESS_TERMCAP_ue=$'\E[0m' export LESS_TERMCAP_us=$'\E[01;32m'`

如此，即可以为manpages添加红绿两色，虽然不多，但是远好过了单调的黑白页面。