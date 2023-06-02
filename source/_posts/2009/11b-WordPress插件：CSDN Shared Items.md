---
title: WordPress插件：CSDN Shared Items
tags:
  - DIY
  - plugins
  - WordPress
id: '357'
categories:
  - [WordPress, Plugins]
date: 2009-11-24 22:27:40
permalink: plugin-csdn-shared-items/
---

我在CSDN上分享了很多东西，一直想把那个列表也在博客上罗列一个，一直就没有付诸于行动，昨天一发狠，终于弄了。

等于昨天几个小时，今天几个小时，搞出了一个小插件。就是右侧的一个小挂件。点上去就会链到CSDN的下载页面。

算是我把一年前的债还了。真开心。

插件里面没什么技术含量，就是小小调用了一下Google Feed API。

做这个插件，也引发了我一个思考。

能否在页面的head部分，就知道这个页面会装载哪些Widget呢？昨天折腾了半天，也没有解决这个问题。

解决的好处是显而易见的，现在的Widget，大多数都需要js来辅助了。但是很多高端的主题有数个sidebar，每页不同，如果Widget开发者，为了符合Web标准，把js放在head部分，就不得不无差别地在所有页面插入代码了。那样的话，添加一个Widget就会带来浪费的流量，页面速度也会被不断拖慢。

当然有个替代方案是把代码放到页面的footer部分，不过，个人以为，只要脚本出现在了Html body里面，那么直接嵌入到Widget中和hook到footer上，其实没什么本质区别，都破坏了行为和数据分离的原则。

这也是无奈之举了。谁叫WP设计成了sidebar.php执行前，无法知道页面会载入哪个sidebar这种结构呢？

当然，不排除还有更好方法的可能，如果知道的网友还望不吝告知。