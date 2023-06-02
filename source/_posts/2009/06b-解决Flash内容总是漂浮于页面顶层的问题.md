---
title: 解决Flash内容总是漂浮于页面顶层的问题
tags:
  - development
  - web design
id: '348'
categories:
  -   - 工作相关
date: 2009-06-03 21:54:27
permalink: flash-float-on-topest-layer/
---

已经有两个网友向我反应了Flash MP3 Player无法和lightbox之类插件兼容的问题，其症状为，当打开lightbox效果的图片时，flash movie会漂浮在整个页面的最顶层，破坏了lightbox的效果。

今天做了一点小小的调查，原来浏览器渲染嵌入页面的内容如flash movie或Java applet时，默认将它们放置于页面的最上层，忽略其z-index属性。所以，像lightbox这类插件，靠设置覆盖层的z-index属性来营造高亮效果的js脚本，基本无法做到覆盖掉页面上的flash movie。
<!-- more -->
Adobe公司给出了对于类似问题的解决办法，就是设置flash movie的wmode属性。

这个属性用于控制Flash 的窗口模式，其有三个取值：

> **window 模式**
> 
> 默认情况下的显示模式，在这种模式下flash player有自己的窗口句柄，这就意味着flash影片是存在于Windows中的一个显示实例，并且是在浏览器核心显示窗口之上的，所以flash只是貌似显示在浏览器中，但这也是flash最快最有效率的渲染模式。由于他是独立于浏览器的HTML渲染表面，这就导致默认显示方式下flash总是会遮住位置与他重合的所有DHTML层。
> 
> 但是大多数苹果电脑浏览器会允许DHTML层显示在flash之上，但当flash影片播放时会出现比较诡异的现象，比如DHTML层像被flash刮掉一块一样显示异常。
> 
> **Opaque 模式**
> 
> 这是一种无窗口模式，在这种情况下flash player没有自己的窗口句柄，这就需要浏览器需要告诉flash player在浏览器的渲染表面绘制的时间和位置。这时flash影片就不会在高于浏览器HTML渲染表面而是与其他元素一样在同一个页面上,因此你就可以使用z-index值来控制DHTML元素是遮盖flash或者被遮盖。
> 
> **Transparent 模式**
> 
> 透明模式，在这种模式下flash player会将stage的背景色alpha值将为0并且只会绘制stage上真实可见的对象，同样你也可以使用z-index来控制flash影片的深度值，但是与Opaque模式不同的是这样做会降低flash影片的回放效果，而且在9.0.115之前的flash player版本设置wmode=”opaque”或”transparent”会导致全屏模式失效。
> 
> 了解了各种模式的实现方式和意义在以后的开发中就可以按照具体情况选择设置wmode属性的值了。

我的插件之所以出现问题，就是因为我把wmode的值设定为了window，当然，这也是默认的值。从三种属性值的具体含义中，我们可以知道，无论是将wmode设定为opaque或者transparent，都可以解决问题，不过网上搜出来的结果，普遍只说了设成transparent这种，并且普遍不讲理由为何。

参考资料：

[flash wmode 参数详解](http://www.blueidea.com/tech/web/2009/6469.asp)

[Flash content displays on top of all DHTML layers](http://kb2.adobe.com/cps/155/tn_15523.html)

[How to make a Flash movie with a transparent background](http://kb2.adobe.com/cps/142/tn_14201.html)