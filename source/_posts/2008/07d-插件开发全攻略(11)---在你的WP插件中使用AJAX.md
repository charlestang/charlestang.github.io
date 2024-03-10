---
title: 插件开发全攻略(11)---在你的WP插件中使用AJAX
tags:
  - develop
  - plugins
  - translate
  - WordPress
id: '106'
categories:
  - [WordPress, Plugins Develop]
date: 2008-07-01 13:41:23
permalink: how-to-write-a-wp-plugin-11/
---

越来越多的插件开始使用AJAX技术。我个人并没有在大多数的插件中看到过AJAX，但是使用AJAX来完成某个任务对你的插件来说可能是必要的。这篇文章将像你展示怎样在你的插件中使用AJAX。

这篇文章将在上一篇文章[《在插件中添加js和css》](http://blog.charlestang.org/how-to-write-a-wp-plugin-09.htm)的基础上继续。
<!-- more -->
### 建立一个新的PHP文件

Devlounge Plugin Series插件已经有了如下的目录结构了：

*   devloung-plugin-series
    
    *   devlounge-plugin-series.php(main plugin file)
    *   js
        
        *   devlounge-plugin-series.js.php
        
    *   css
        
        *   devlounge-plugin-series.css
        
    *   php
        
        *   dl-plugin-ajax.php(新php文件)
        
    

注意，我的javascript文件的扩展名是**php**。我会在这篇文章后面解释这个变化的来历。

我已经建立了一个新的文件，并且把它放到了**php**文件夹中，并且命名为**dl-plugin-ajax.php**。我已经在这个文件中放了如下的代码：

```php

showComments();
}
?>

```

这个段代码非常简单，并且仅为做AJAX调用而写。它确保了配置结构存在，从而我们可以调用类对象**dl_pluginSeries**，引用其他WordPress函数和变量。然而，**showComments**函数还没有创建，我们下一个议程就是来做这件事。

### 定义showComments函数

**showComments**函数将放在我们的**DevloungPluginSeries**类中：

```php

function showComments() {
    global $wpdb;
    $devloungecomments = $wpdb->get_row("SELECT count(comment_approved) comments_count FROM $wpdb->comments where comment_approved = '1' group by comment_approved", ARRAY_A);
    echo "You have " . $devloungecomments['comments_count'] . " comments on your blog";
}

```

可能已经认出来了，这段代码在数据库交互这篇文章中出现过。此函数输出你博客上留言的数量。

### 让JavaScript知道你的博客在哪里

使用AJAX时，一个烦人的事情就是外部JavaScript文件不知道你博客安装路径是什么。我是通过在js后面添加php扩展名来处理这个问题的，因为这样，我就可以调用WordPress函数了。在**addHeaderCode**函数中，我把代码从：

```php

if (function_exists('wp_enqueue_script')) {
    wp_enqueue_script('devlounge_plugin_series', get_bloginfo('wpurl') . '/wp-content/plugins/devlounge-plugin-series/js/devlounge-plugin-series.js', array('prototype'), '0.1');
}

```

换成：

```php

if (function_exists('wp_enqueue_script')) {
    wp_enqueue_script('devlounge_plugin_seriess', get_bloginfo('wpurl') . '/wp-content/plugins/devlounge-plugin-series/js/devlounge-plugin-series.js.php', array('prototype'), '0.3');
}

```

我唯一改变的是一个版本号码，还有就是给JavaScript文件添加了一个php扩展名。

### 编写JavaScript

这段脚本的目的是找到博客的URL，调用PHP文件，然后返回结果给用户。

```javascript


Event.observe(window, 'load', devloungePluginSeriesInit, false);
function devloungePluginSeriesInit() {
    $('devlounge-link').onclick = devloungePluginSeriesClick;
}
function devloungePluginSeriesClick(evt) {
    var url =  "/wp-content/plugins/devlounge-plugin-series/php/dl-plugin-ajax.php";
    var success = function(t){devloungePluginSeriesClickComplete(t);}
    var myAjax = new Ajax.Request(url, {method:'post', onSuccess:success});
    return false;
}
function devloungePluginSeriesClickComplete(t) {
    alert(t.responseText); 
}

```

上述代码做了下面这些事情（记住，我们在使用Prototype）：

*   确定配置结构是存在的，这样我们才能访问WordPress函数
*   在文档已经装载后，**devloungePluginSeriesInit**函数被调用了
*   给你添加到文章末尾的链接上绑定了一个事件。如果你忘了，现在可以加进去。简单地找到文章，然后添加这段代码：<a href="#" id="devlounge-link">Get the Number of Blog Comments</a>
*   找到PHP文件的绝对路径
*   调用PHP文件
*   将反馈输出给用户

### 结果

下一步，我们假设你已经把那个链接添加好了。我们点击链接“**Get the Number of Blog Comments**”，脚本使用AJAX调用了**DevlongePluginSeries**类中的函数，并且以对话框的形式返回了结果。

就如你看到的那样，我的本地安装版本，并没有多少评论。