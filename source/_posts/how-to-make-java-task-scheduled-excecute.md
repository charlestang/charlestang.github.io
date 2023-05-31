---
title: 如何让Java程序定时运行
tags:
  - excecute
  - java
  - schedule
  - thread
id: '302'
categories:
  - - 工作相关
date: 2009-02-23 23:13:59
---

![Timer and TimerTask class diagram](http://lh6.ggpht.com/_QYicOeu89Bk/SaK8o7J0S2I/AAAAAAAABHw/wvBb9HFkEcw/s400/Timer.png)

由于项目开发的需要，必须实现让一个Java程序定时运行。比如，我的项目中，有一个网络蜘蛛，需要从互联网上抓取数据，与其配合，有另一个程序来对新抓取的页面进行索引的创建，由于数据源更新频率不高，我们不可能让蜘蛛无休无止地工作，或者忙等待新数据的产生，那样只能造成浪费，而且非常地不礼貌，所以最理想的情况是，让它每隔一个小时运行一次，这样一天也就运行不了几次。
<!-- more -->
那么如何才能实现让一个Java程序定时运行呢？Java基本类库里面，提供了两个工具供我们使用，它们是java.util.Timer和java.util.TimerTask。

Timer是一个对象，这个对象在初始化之初，会创建一个后台进程（TimerThread），同时创建一个任务队列（TaskQueue），然后后台进程开始检测TaskQueue中是否存在等待调度的任务，如果存在，就运行之，如果不存在，就等待（Object.wait()）。

对于程序员可见的类是Timer和TimerTask，TimerTask是一个抽象类，是能够被Timer所调度的一种对象，所有希望定时执行的任务，只要实现TimerTask类即可，然后使用Timer的schedule方法，给定一定的参数，即可实现定时执行，或者周期执行。

schedule方法的本质，是将一个TimerTask对象添加到了TaskQueue中，这个TaskQueue是一个堆（可以动态增长），可以管理很多的Task。

Timer的本质，就是一个线程，按照指定的时间顺序，来顺次执行一个又一个的任务，根据这种性质，我们可以知道，Timer实现的定时不可能准确，而且，还会收到任务本身耗费时间的干扰。如果前一个任务执行时间过长，超过后一个任务的启动时间，则后一个任务的启动时间必然要顺延。所以，这种方法，只能用于，任务短小，且对时间精度要求不高的语境。

Timer是线程安全的，可以实现并发访问。