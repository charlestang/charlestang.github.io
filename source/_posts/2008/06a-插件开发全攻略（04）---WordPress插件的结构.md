---
title: 插件开发全攻略（04）---WordPress插件的结构
tags:
  - develop
  - plugins
  - translate
  - WordPress
id: '72'
categories:
  - [WordPress, Plugins Develop]
date: 2008-06-01 19:32:47
permalink: how-to-write-a-wp-plugin-04/
---

开发一个WordPress插件的一个更重要的方面，是你怎样设计它的结构。本文将研究几个关于设计插件结构的提示，以帮助你组织你的插件资源，避免名字冲突。每一个插件作者的插件的结构都不尽相同，所以这些提示只是我的个人偏好。我将首先简单地描述一下一个WordPress插件是怎样工作的，然后介绍一个插件的结构。

### WordPress插件怎样工作

在将一个插件放入到wp-content/plugins/目录后，插件[应该自动的处于可以安装的状态](http://codex.wordpress.org/Managing_Plugins)。

当一个插件被“启用”，等同于告知WordPress将你的代码装载到“每”个页面（包括管理页面）。这也就是为什么当你启用了很多的插件的时候，你的WordPress可能非常慢的原因，这是由它所引入的代码的量决定的。
<!-- more -->
从你的插件被启用，WordPress自动将你的代码装载后开始，你可以利用[WordPress插件API](http://codex.wordpress.org/Plugin_API)。你还可以使用[WordPress模板标签](http://codex.wordpress.org/Template_Tags)或者创建你自己的函数。

如果你计划开发一个改变文章内容或者评论的插件，我建议你读一下[WordPress loop](http://codex.wordpress.org/The_Loop)。WordPress loop是一个显示你的文章的循环。有些模板标签在这个循环外面无法工作，所以，你准确地知道你代码在哪里执行是非常必要的。你可通过使用[Actions](http://codex.wordpress.org/Plugin_API#Actions)和[Filters](http://codex.wordpress.org/Plugin_API#Filters)来控制这一点，这将会在将来的文章中解释。

### 文件夹结构

所有的WordPress插件都会被安装到wp-content/plugins目录中。有些插件作者的插件只包含一个文件，但是我推荐你总是创建一个文件夹来保存你的插件。

典型地，我会把我的插件放在如下的目录结构中：

*   插件文件夹名称（你插件的名字，没有空格或者特殊字符）
    *   插件PHP文件
    *   js文件夹（存放javascript文件）
    *   css文件夹（存放样式表文件）
    *   php文件夹（存放其他的PHP文件）

举例来说，这是一个我创建的样例结构：

*   devlounge-plugin-series
    *   devlounge-plugin-series.php
    *   js
    *   css
    *   php

在devlounge-plugin-series文件夹中，我将只包含主要的PHP文件，把其他的文件都放到他们各自属于的文件夹中。这个结构将帮助其他插件作者在查看你的代码的时候，能够分辨哪个是主要的插件文件，哪些是支持插件正常工作的附属文件。

WordPress还建议将图片放到一个文件夹中，并且包含一个readme文件在你的插件中。

### 主要插件文件

当你开始编写一个插件的时候，前面七行用来描述你的插件。

```php


第3行是让你命名你的插件的。第4行是向用户指出插件所在的网址的。第5行让你指定当前的版本。第6行让你设定插件的作者。第7行是对插件的描述。下面展示的是一个已经填写完毕的范例：

/*
Plugin Name: Devlounge Plugin Series
Plugin URI: http://www.devlounge.net/
Version: v1.00
Author: Ronald Huereca
Description: A sample plugin for a Devlounge series.
*/
  
下面展示的是插件在WordPress插件面板上出现的截图。

设定一个类结构开发一个插件，并不需要你对PHP类了若指掌，但是如果你真的很熟悉，那会很有帮助。为了避免与其他的WordPress插件发生名字冲突，一个类结构是必须的。如果别人在插件当中使用了和你一样的函数名，那么就会发生一个错误，WordPress可能会无法响应直到你删除那个插件。为了避免名字冲突，所有的插件都使用一个PHP类结构是急需的。这里有一些“骨架”代码，可以帮助你创建一个类结构。

if (!class_exists("DevloungePluginSeries")) {
class DevloungePluginSeries {
function DevloungePluginSeries() { //constructor
}
}
} //End Class DevloungePluginSeries

上述代码的含义是，首先检查是否有一个名叫DevloungePluginSeries的类存在。如果这个类不存在，那么创建这个类。初始化你的类下面的代码将会初始化你的类。

if (class_exists("DevloungePluginSeries")) {
$dl_pluginSeries = new DevloungePluginSeries();
}

 上面的代码检查是否类DevloungePluginSeries已经存在了。如果已经存在，那么一个变量$dl_pluginSeries将会被创建，并且会使用一个DevloungePluginSeries类的对象给它赋值。设置Actions和Filters下面的代码段是用来放置WordPress Actions和Filters的地方（我会在后续的文章中详细讲）。

//Actions and Filters
if (isset($dl_pluginSeries)) {
//Actions
//Filters
}

上述代码首先确认$dl_pluginSeries是否已经被设定。如果设定了（仅当类存在的时候），那么就会设定合适的actions和filters。
```