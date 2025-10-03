---
title: MAMP Pro 里面自带的 PHP 命令行执行特别慢的问题
tags:
  - mac
  - PHP
id: '760'
categories:
  - - 技术
    - 后端
permalink: mamp-pro-php-cli-very-slow/
date: 2017-01-11 14:04:22
---

在 Mac 系统下开发 PHP 的话，使用 MAMP Pro 来搭建环境是一个不错的选择，主要还是因为方便，一口气就可以拥有 PHP + MySQL + Nginx + Apache + PostgreSQL + Memcached + Ruby + Python + Perl，可以说 Web 开发的全部组件基本都涉及到了。
<!-- more -->
所使用 MAMP Pro 已经有两年的历史了，最新升级的这个版本，配合最新的 Mac OS Sierra 版本，遇到了一个十分奇怪的问题，如果在命令行下使用 php 命令的话，每次执行命令都会特别缓慢。

其实我以前也遇到过这类的问题，知道大概的起因，这次很想自己证明一下子，结果，失败。哈哈哈，一般我会使用 strace 或者 ltrace 来看命令卡顿的点。

结果在 Mac 下是没有 strace 的，得用 dtruss 代替，也没有看出来什么端倪。索性就放弃了，网上搜了一下，根据经验，这个问题都是因为某些地方调用了无谓的 DNS 导致的，所以就在这么一个帖子里看到了[关于 DNS 的说法](https://github.com/liip/php-osx/issues/102)，于是在自己的 hosts 文件里添加了关于自己的主机的 entry，问题解决。

Mac 的主机名，在 Preference -> Sharing 面板上面的 Computer Name 格子里填着，设置 host 的时候，记得加 .local 后缀。

例如，你的主机名叫 MyComputer，那么你的 host 应该如下：

```txt
127.0.0.1 MyComputer.local
:::1      MyComputer.local

```

药到病除！