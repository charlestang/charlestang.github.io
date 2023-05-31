---
title: 折磨一下浏览器们，哈哈
tags:
  - test
  - Web Browsers
  - web design
id: '355'
categories:
  - - 工作相关
date: 2009-09-04 16:30:20
---

The Web Standards Project **Acid Tests**

[http://www.acidtests.org/](http://www.acidtests.org/ "http://www.acidtests.org/")

“An acid test is a test used to confirm that a material such as jewellery is gold.”  ---  Wikipedia
<!-- more -->
Acid Test 恰如其字面意思，酸性实验，拿来测试一种珠宝首饰是否是黄金制成。这个词，现在已经作为词组进入了牛津词典，其引申意义为“决定性的试验；严峻考验”。

The [Web Standards Project](http://www.webstandards.org/) is a grassroots coalition fighting for standards which ensure simple, affordable access to web technologies for all.

这个Web Standards Project则是一个草根组织，致力于推广Web标准的。我现在这里说的这个Acid Test就是他们推出的，用于检测浏览器对Web标准支持情况进行检测的一组测试。

每一种测试，都有其偏重的方面，能否通过测试和得分高低，并不能说明什么绝对问题，只是可以作为一种参考标准。因为执行测试很简单，所以我把自己手头的所有浏览器都测试了一遍。

浏览器

Acid3结果

用时

IE8

Fail 得分20

 

Firefox 3.5.2

Pass 得分93

2.35s

Opera 9.27

Fail 得分47

 

Opera 9.64

Pass 得分85

2.88s

Chrome 3.0

Pass 得分100

2.22s

Safari 4

Pass 得分100

2.68s

Acid Test有3组，鉴于上述所有浏览器都完美地展现了1和2的结果，我也就没有列进去了。

上述结果，只是一个参考，我们可以看到一些事情，Webkit内核已经率先做好了对标准的支持，包括CSS3和HTML，其实Opera公司的Presto也同样做好了准备，我前些日子再Opera10 beta上跑过Acid3，发现也是100分，不过没有看执行时间。所以，基于Webkit内核的Chrome和Safari都得了满分，不过呢，貌似Chrome的脚本引擎确实要更先进一些，所以呢，Chrome更快。

上述列表中的大输家是IE8和Opera 9.27。Opera 9.2还情有可原，IE8实在是让人抱歉了，折腾了半天，对标准兼容还是这么差。不过，我还是想强调，这个测试不能说明大部分问题。因为这两个大输家，正是我日常使用最多的浏览器。（我平时使用的，就只有IE8，Firefox和Opera 9.27，其他都是调试用的。）事实上，我觉得IE8是微软历史上最好的浏览器了，甚至我觉得比Firefox 3.5.2要好用很多。其实，我很实在的，IE8真的要快上一个数量级了。至少在我的机子上是这样。对各类垃圾网页的兼容也很好。以前，我最常用的浏览器是Firefox，现在重心在向IE8转移。正所谓“一快遮三丑”，就是这个样子的。另外一个因素，就是Firefox绝对是内存杀手，只要开的程序稍多，我一定会先杀死这只狐狸。

我记忆如果没有偏差IE7是无法通过Acid2的，而IE8轻易过关，这表明了微软的一种姿态，还是支持Web标准的。其他可能是一些市场因素的考虑吧，所以才会变成现在这种结局。

写到这里，我也不知道要说些啥了，貌似胡乱扯了一堆东西。就这样吧。