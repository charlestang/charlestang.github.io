---
title: 使用 APT 源将 MySQL 升级到 5.7
tags:
  - debian
  - Linux
  - MySQL
id: '764'
categories:
  - 工作相关
date: 2017-02-04 12:24:30
permalink: update-mysql-server-5-7-with-apt/
---

我的博客是使用 [Linode](https://www.linode.com/?r=f268347f24b5221e45c9a1048cb8b8db0f0c241a) 搭建的，算算已经快有八年多历史了。从一开始，我就使用 Debian 发行版作为我的服务器版本。当时，最流行的服务器是 RedHat 和 Ubuntu，那时候我还没听说过 CentOS，哈哈，不想用盗版，又觉得 Debian 比较稳定，而且有无敌的 apt-get，就一直用 Debian 了。
<!-- more -->
因为我用 WordPress 搭建博客，一直以来，用的就是 MySQL 数据库，从 2015 年开始，MySQL 就推出了 5.7 版，增加了一些激动人心的特性，比如更好的 InnoDB，JSON，地理位置等等东西，一直以来还没机会探索。其实，我感觉，在做 PHP 的人群里，使用 MySQL 的新特性，一直以来都是比较偏保守的，也可能我个人处理更大规模的应用的机会比较多，平时更偏重于利用架构解决问题，反倒是对数据库本身的能力不甚了解。

自己拥有一台 Server，不就是为了实验各种新奇的技术嘛，但是又不想博客的稳定性（lan3）受到影响，所以，一直拖着没有安装 MySQL 5.7，今天又萌生了看看的想法，去官网一看，原来人家早就提供了使用 APT 源更新 MySQL 版本的方式，安全可靠，这下再没什么借口了。

打开官网的下载页面，再平台选择框里，选择 Debian 或者 Ubuntu，你就会看到一个 APT 安装源的广告 banner，[点击链接过去](https://dev.mysql.com/downloads/repo/apt/)，就会看到一个 deb 包的下载，下载好这个包到你的服务器，执行：

```shell
sudo dpkg -i mysql-apt-config_0.8.1-1_all.deb

```

其实是使用手动方式部署安装了一个 deb 包到你的服务器，作用是配置好 MySQL 的安装源，按下回车，会出现一个字符图形界面，在里面选择 MySQL 5.7 版的 Server，然后 OK，就算配置完毕了 MySQL 安装源。

```shell
sudo aptitude update
sudo aptitude safe-upgrade

```

再执行这两个指令，你的 MySQL，就会安全平滑的升级到 5.7 版本了。aptitude 可以用 apt-get 代替，我个人习惯使用 aptitude。本来以为执行到这里就应该结束了，但是想得太简单了。其实，到了这里已经不影响一般的使用了，但是，当我执行 mysqldump 的时候，错误发生了：

> mysqldump -hlocalhost -umydb -pmypass --single-transaction mydb > /tmp/sexywp_com_20170205-19-39-05.sql
> mysqldump: [Warning] Using a password on the command line interface can be insecure.
> mysqldump: Couldn't execute 'SHOW VARIABLES LIKE 'gtid\_mode'': Native table 'performance_schema'.'session_variables' has the wrong structure (1682)

原来，在 MySQL 数据库升级以后 performance_schema 表会出问题，接下来要执行：

```shell
mysql_upgrade -uroot -p --force
sudo service mysql restart

```

首先完成升级操作，然后再重启数据库，这样才算全部执行完毕，现在再进行 mysqldump 也不会出问题了。