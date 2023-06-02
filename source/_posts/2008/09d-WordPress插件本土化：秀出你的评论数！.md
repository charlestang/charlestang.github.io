---
title: WordPress插件本土化：秀出你的评论数！
tags:
  - localization
  - plugins
  - WordPress
id: '233'
categories:
  - WordPress
date: 2008-09-04 11:27:02
permalink: show-your-comments-counter/
---

今天，要介绍给大家的这款插件叫做[Liz Comment Counter](http://planetozh.com/blog/my-projects/liz-strauss-comment-count-badge-widget-wordpress/)（点进去吧，去Ozh那里看看美丽的截图，和详尽的介绍，e文滴--b），这是由著名的插件达人Ozh编写的，由著名的篡改达人Charles篡改 -_-## 寒一下~~~（表拍砖）

说白了，效果很简单啦，就是像本站右边栏那样的，看起来有点像FeedSky的统计图标。当然，那个颜色是可以调整的，后面的字也是可以调整的，完全自定义！！这就是Ozh的强大。
<!-- more -->
我篡改了啥呢？

咦？……为啥你的“评论徽章”上面的字是中文的？（高手当然不会好奇任何东西，飘过飘过吧）

我就是简单本土化了一下。

好，下面放出下载链接：

[点击这里](http://www.mediafire.com/?cdgseh2onkn)

用法是超级简单的，Widget嘛，没什么花头的。里面选项，要注意，如果用了中文，字体选“Simfang”（没错，这个字体我加的，是仿宋，因为体积最小，只有3M，你可以放个好看的雅黑40M或者宋体10M到你的fonts文件夹，在插件目录里面，字体自己去找）。

如果不想使用Widget，想用手动调用（为啥总有小强那么爱找麻烦呢？），可以使用如下template tag：

<?php wp_ozh_lcc_badge();?>

不过呢，选项设定就烦一点了：

1. 进入Widgets管理页面，添加Liz Comment Counter Widget；

2. 设置选项，保存；

3. 移除Widget，保存；

通过这个动作，你设定好了选项，但是又没有添加Widget，烦吧，如果你的主题正好不支持Widget，那么，是否需要我教你怎么做？？汗……提示一下，先换上一个支持Widget的主题，比如default……………………好冷~

Updated：

发现Jinwen写过这个文章的，唉，慢了一步，还好我汉化了不算啥都没干，大家去看看他的文章吧，很详细。
[Smartr.cn：秀秀你的评论数](http://smartr.cn/wordpress/why-not-show-your-comment-numbers.html)