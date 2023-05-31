---
title: 一次故障的处理
tags: []
id: '722'
categories:
  - - 日　　记
date: 2018-03-08 16:31:59
---

网站 502，看 log

发现 mysql storage engine error 28，不明白原因

google 被提醒磁盘满了

du -sm * 查看哪个目录占空间大，发现无法执行，因为 /tmp 目录计算不出来

ls /tmp wc -l 发现计算不了，主要 ls 执行不了

怀疑文件过多，google 找方法，因为 ls 默认排序导致

ls -f /tmp
ls -U /tmp
ls --sort=None /tmp

等方法，发现文件有 145万个

都是 sess_xxxx 为 PHP 的 session 文件

删空 sess 文件，处理 sess 文件的自动清理问题

全部做完发现，磁盘仍然是满的

du -sm *

发现是 log 过大

查看 log 是因为 WP 报错导致，原因是数据库 user 没有权限

授权后，问题解决，但是牵扯了更多的问题，有待解决

1. wordpress 主从同步方案的缺陷
2. 服务器监控报警