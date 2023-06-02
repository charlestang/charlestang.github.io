---
title: 【vim】 Debian(Jessie) 源里带的vim，不支持Python
tags:
  - usage
  - vim
id: '683'
categories:
  - [小窍门]
  - [工作相关]
date: 2015-06-16 23:19:31
permalink: debian-jessie-does-not-support-python/
---

在安装有些vim插件的时候，需要Vim支持Python，比如YouCompleteMe，但是，最近升级到Jessie后，发现，默认的vim，是不支持Python的，于是在网上搜索了一下，如果需要vim的二进制版本带有Python支持的话，应该安装一个叫 vim-nox 的包，其介绍为：

 Vi IMproved - enhanced vi editor - with scripting languages support

就这样。