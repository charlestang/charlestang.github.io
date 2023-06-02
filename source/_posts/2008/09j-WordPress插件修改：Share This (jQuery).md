---
title: WordPress插件修改：Share This (jQuery)
tags:
  - jQuery
  - my works
  - plugins
  - WordPress
id: '230'
categories:
  - [WordPress, Plugins]
date: 2008-09-02 20:15:49
permalink: share-this-jquery/
---

[Share This 中文](http://www.happinesz.cn/archives/328/)，我很喜欢，看起来效果很好，但是……
<!-- more -->
> 建议牛人出来重写[sofish](http://happinesz.cn)改过的那个Share This。
> 
> [Alex King](http://alexking.org)大大写的[Share this](http://alexking.org/projects/wordpress)基本上没有照顾到中文用户。
> 
> 后来，经过sofish改写，我们有了非常适合中文博客使用的Share this 中文。
> 
> 但是，这个插件有三大缺憾：
> 
> 1. 这么简单的功能，居然动用了prototype，此类库尺寸达128k。
> 
> 2. 在hook使用方面，没有进行优化，如果一般用户不知道，安装了这个插件会在每一个页面都引用一个prototype进来，汗 ，实际上只需要在single页面引入，更人性化的做法是根据用户的需求来引入js文件和css文件。
> 
> 3. 完全应该改个名字重新发布，这并不是说对原作者不尊重，而是现在这个插件的代码看起来和原来的已经差别较大了，而且此插件进入官方目录，使用的是GPL协议，我们可以另立门户，这样使用此插件的用户就不必要收到升级的困扰，上次我误点了升级，直接跳到Alex King的版本上了。
> 
> 希望能有人接手这个工作！
> 
> 最后还是要谢谢写出这个插件的Alex King和修改它的sofish。

上面是我在论坛发的帖子，没有人响应我，囧……

其实，说的就是一直以来我想做的事情。

实在不能忍了，于是自己动手了，囧！

那个插件的sofish版本还有一个问题的，当时[stephen](http://www.caxblog.com "stephen")跟我提出过的，就是点击一个搜藏链接的时候，应该采用打开新页面更加符合中国人的习惯。这次我也一并给改了。

好，我就不多说了，把我改的版本放出来给大家分享下吧。

http://www.box.net/shared/naa6u9oi2j

建议：模板里已经使用了jQuery的人推荐用这个版本。

另外：jQuery也不是必须的，因为基本上没有用到相关度的什么特性，所以，建议使用纯js重写，囧！

有学习js的，jQuery的同学愿意尝试下么？

Updated:2008年9月2日21:28:37

调用方法没有变化，大家去sofish的那个页面看看调用方法吧，我懒得写了 :mrgreen: