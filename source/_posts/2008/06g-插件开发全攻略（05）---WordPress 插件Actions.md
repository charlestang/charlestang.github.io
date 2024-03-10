---
title: 插件开发全攻略（05）---WordPress 插件Actions
tags:
  - develop
  - plugins
  - translate
  - WordPress
id: '85'
categories:
  - [WordPress, Plugins Develop]
date: 2008-06-03 14:47:35
permalink: how-to-write-a-wp-plugin-05/
---

[WordPress actions](http://codex.wordpress.org/Plugin_API#Actions)允许作为插件作者的你插入到WordPress应用中并且执行一段代码。一个Action的例子就是，你想要在一个用户发布完一篇文章或者留下一篇留言的时候执行一个动作。

一些我使用极其频繁的Action有：

*   admin_menu：允许你给你的插件设置一个管理面板。
*   wp_head：允许你将代码插入到博客的<head>标签内。
<!-- more -->
### Action在行动

当定义一个[WordPress插件的结构](http://blog.charlestang.org/how-to-write-a-wp-plugin-04.htm)的时，我为某些Action留下了一块地方。在这个例子中，我们将使得一段代码可以在WordPress博客中的<head>标签内运行。

首先，我们需要在**DevloungePluginSeries**类中添加一个函数：

```php

function addHeaderCode(){

}

```

 

上面一段代码的作用是输出HTML注释。相当简单，但是你实际上可以输出任何东西。为了调用这个函数，我们要添加一个Action。

```php

//Actions and Filters
if (isset($dl_pluginSeries)){
//Actions
add_action('wp_head',array(&$dl_pluginSeries,'addHeaderCode'),1);
//Filters
}

```

从[WordPress插件API](http://codex.wordpress.org/Plugin_API)中我们可以知道，add_action的结构如下：`add_action('hook_name','your_function_name',[priority],[accepted_args]);`

由于我们是在一个类的内部调用一个函数，我们传递给Action一个数组，里面包含我们的类对象的引用（dl_pluginSeries）和我们想要调用的函数名（addHeaderCode）。我们已经给我们的插件设定了一个优先级为1，数字越小，执行时间越靠前。

### 运行代码

如果Devlounge Plugin Series插件被启用了，使用【查看->源文件】应该可以在你的博客的源码中看到注释“Devlounge was here”。

### 移除Action

如果你的插件动态地添加Action，你也可以使用remove_action来动态地移除action。用法如下：

`remove_action('action_hook','action_function')。`