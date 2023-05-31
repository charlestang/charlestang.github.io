---
title: 【What】Ubuntu中apt-get列出的软件包前面的字母标识含义
tags:
  - apt-get
  - debian
  - Linux
  - ubuntu
id: '546'
categories:
  - - something-about-daily-work
    - Linux
  - - 工作相关
date: 2013-04-02 00:33:01
---

在Ubuntu服务器上，执行apt-get或者aptitude，可以列出软件包的名字，每行一个，最前面有个表明状态的字母标识：

*   **p** 在系统里没有关于该软件包的相关操作记录
*   **c** 软件包已经删除，但是配置文件仍旧保留在系统中
*   **i** 软件包已经安装过了
*   **v** 软件包是虚拟的（由若干其他软件包组合而成）

第二个位置上的字母，表明即将执行的动作

*   **i** 即将被安装
*   **d** 即将被删除
*   **p** 软件包和配置文件将被删除
*   **A** 表示软件包已经自动安装了