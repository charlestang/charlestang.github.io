---
title: Windows组件中的Timer计时精确度有限
tags:
  - computer
  - dotNet
  - programming
  - science
id: '45'
categories:
  - 工作相关
date: 2008-04-08 20:49:46
permalink: the-timer-is-not-accurate/
---

真是无比惭愧啊，过了这么久，连这么基础的知识都不知道，特意记录在此。

今天，实验室要求我编写一个小程序，操纵一个摄像头按照指定的时间间隔拍摄照片。真的是小Case啦。两个多小时，我做完了。晚上，我兴致勃勃的开始了测试。

按照需求，我测了一下1秒中内等时间间隔拍摄10张图片。在反复不断测试中，我突然惊讶的发现了一个问题——我拍摄下来的图片，不是间隔100毫秒的，而是间隔109毫秒。

开始，我以为这是因为我的中断处理程序的执行时间造成的，于是，我给时间间隔做了个修正，即如果设置时间间隔为100的话，在程序内部，就按照90毫秒来触发。发现这种情况下，时间间隔变成了93或94毫秒。

终于还是把这个问题问出了口，对面的小哥立刻告诉我，Timer使用的时间中断，Windows中每隔1/18秒触发一个时钟中断，所以，Timer的定时精度只能达到55毫秒。晕死，这么简单的事情，我竟然不知道，一看msdn，还真是这么回事。

按照msdn的指引，选用了所谓的更加精确的服务器计时器，System.Timers.Timer，重新测试，发现结果没有变。晕死，怎么会这样呢？仔细看文档，对比.net framework中拥有的三种定时器。Win32定时器，服务器定时器，线程定时器。Win32定时器是单线程定时器，精度55毫秒；服务器定时器是多线程定时器，其精度**可能**比Win32定时器精确得多（注意只是可能）；线程计时器专门用于那种消息不在线程上发送的解决方案，没有提到其精度。原来如此啊。

对于最终的结果，我有如下的结论：
1、我用任何定时方法，都无法达到指定的精度，其原因可能与码流本身有关，因为我调用的是第三方非开源的控件提供的ImageCaptur方法，该方法截取图片的时间间隔可能受到帧率的影响，而我除了使用这个非开源控件，不能用其他办法操纵摄像头。
2、虽然说Win32定时器(System.Windows.Forms.Timer)的精度只有55毫秒，但是实际使用中，发现产生的最终结果和System.Timers.Timer相同，即，不是93或94毫秒，就是109毫秒。由于我对msdn更加信任一点，所以这个结果就更加使我确信，实际拍摄的时间间隔受到视频流本身的帧率的影响。
3、实际上，可以更加进一步地调查定时不精确的原因，并且寻求解决办法（最终结论可能还是没有解决办法），但是由于这个选择的性价比实在太低，不值得尝试，所以，到此为止。