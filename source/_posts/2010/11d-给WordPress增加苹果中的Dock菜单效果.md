---
title: 给WordPress增加苹果中的Dock菜单效果
tags: []
id: '398'
categories:
  - [WordPress, Plugins]
date: 2010-11-09 14:19:21
permalink: add-dock-menu-to-ur-wordpress/
---

苹果操作系统的Dock菜单，可能是个人桌面操作系统中，最成功的一种UI设计了。这个交互设计效果优美，使用简便，一目了然。无数爱好者，将Dock菜单的交互设计和视觉效果移植到了各种各样的系统和平台上。

在Web上实现Dock菜单，也不是什么新鲜事了，包括我以前想要汉化过的一个favourate类插件，也都是Dock的理念。

jQuery有个插件，就是专门实现这个[Dock菜单的效果](http://interface.eyecon.ro/docs/fisheye)的。在[这里](http://interface.eyecon.ro/demos/fisheye.html)可以看到例子。文章标题里说的，是一个WordPress的插件，插件的名字翻译成中文的话，叫[动态WP鱼眼菜单](http://wordpress.org/extend/plugins/dynamicwp-fisheye-menu/)。我不知道为什么作者要取这么难听的名字，而且并不让人一目了然，既然Dock已经是几乎人尽皆知的效果了，何必再去自己发明名字。不过呢，这并不妨碍作者实现了这么一个使用简便的插件。到[这里](http://www.dynamicwp.net/fisheye-menu-demo/)可以看效果。

从一个插件开发者的角度来看，Charles觉得这个插件的结构是非常简单的，只是在WordPress的里面引入了一个jQuery的插件，顺便增加了后台管理界面。从一个用户的角度看，我觉得这个插件有一个值得赞扬的地方，它的后台非常之简单，简单到了一目了然的地步。应该成为所有插件作者设计插件后台时候参考的典范。不过呢，也有一个缺点，就是这个插件的安装却并不是那么简单。因为需要用户手动修改代码。我想，这会给这个插件的流行，带来巨大的阻力。我觉得这是每个插件开发作者应该竭力避免的事情。