---
title: Nexus S上网、彩信设置方法
tags: []
id: '416'
categories:
  - - 历史归档
permalink: how-to-set-nexus-s-net/
date: 2011-03-19 02:28:17
updated: 2025-05-08 02:18:29
---

入手Nexus S一周了，主要感觉还是信号较弱，WiFi比较弱，通信信号也很弱。在室外空旷地稍微好一点，在办公室基本比较悲剧。按照我同事的说法，国外生产的手机，辐射量必须符合他们自己的标准，是考虑了辐射量不会影响身体健康的前提下制定的，所以在中国信号相比国产山寨机要弱。OK，听起来像是个不错的理由。那就这样吧。
<!-- more -->
拿到Nexus S，如果是新机器，一开机的话，可能网络是没有设置好的。这个时候，既不能发彩信，也不能上网，但是可以发送普通短信和打电话。

根据我实际使用的经验来看，我用的中国移动，移动的网络是自动向外广播它的网络配置方法的，也就是说，如果刚拿到手机的童鞋，不做任何设置，一段时间后，就会被自动设置好。我是怎么发现的呢，我一拿到，看到有两个配置，但是不怎么对，就按照网上说的改了，勉强改到能上网了，今天本来想彻底重新研究一下这块的配置，重新设置的，就执行了一下“重置为默认设置”，结果一看，已经正确配置好了彩信和网络。

这里还是列举一下配置方法，以供没有自动配成功的童鞋参考：

进入“设置-无线和网络-移动网络-接入点名称”，点击菜单按钮，选择“新建APN”，按照如下填写：

1.名称: 中国移动彩信
2.APN: cmwap
3.代理: 10.0.0.172
4.端口: 80
5.用户名:（空着）
6.密码:（空着）
7.服务器:（空着）
8.MMSC: http://mmsc.monternet.com (记住一定要加上“http://”不然的话只能收不能发)
9.彩信代理: 10.0.0.172
10.彩信端口: 80
12.MCC: 460
13.MNC: 00 (有的机器需要设置00，原生中文版才可以设置02)
14.身份验证类型: CHAP
15.APN类型: mms

保存，以上是发送彩信使用的。然后再创建一个新的APN，按如下配置：

1.名称: 中国移动 GPRS
2.APN: cmnet
3.代理: （空着）
4.端口: （空着）
5.用户名:（空着）
6.密码:（空着）
7.服务器:（空着）
8.MMSC: （空着）
9.彩信代理: （空着）
10.彩信端口: （空着）
12.MCC: 460
13.MNC: 00 (有的机器需要设置00，原生中文版才可以设置02)
14.身份验证类型: CHAP
15.APN类型: default,supl （网上也有人说这里填internet的，如果上不了可以试试）

保存，以上配置是用来上网的，连接的是cmnet。

这里，我报下我手机的系统版本：
Android 版本：2.3.1
基带版本：I9020XXJK8
内核版本：2.6.35.7-g7f1638a

配置保存好网络接入点设置后，单选勾取cmwap，平时发彩信，如果用到网络的话，会自动选择cmnet作为接入点的。我已经实验过了。在外层菜单一定勾选“已启用数据”，否则还是不能上网的。