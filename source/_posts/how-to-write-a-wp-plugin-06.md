---
title: 插件开发全攻略（06）---WordPress插件Filter
tags:
  - develop
  - plugins
  - translate
  - WordPress
id: '86'
categories:
  - - wp
    - Plugins Develop
  - - WordPress
date: 2008-06-04 18:48:18
---

[Filter](http://codex.wordpress.org/Plugin_API/Filter_Reference)是一组使得你的插件可以插入来修改文字的函数。被修改的文字通常是要插入到数据库或者显示给终端用户看的。

WordPress Filter允许你修改几乎任何类型的显示文字，而且其功能十分强劲。通过Filter你可以修改文章，feed，怎么样在评论中的作者，还有很多，很多。

为了说明WordPress Filter的用处，我们会继续在已经存在的Devlounge Plugin Series代码上工作。
<!-- more -->
### 添加一个内容Filter

有一个你可以使用的很Cool的Filter是'the_content'。这个filter在文章内容被显示在浏览器之前执行。我们将要添加一行文字到文章内容的末尾。

根据[WordPress插件API](http://codex.wordpress.org/Plugin_API)，添加一个filter的格式为：`add_filter('hook_name','your_filter',[priority],[accepted_args]);`

我们只需要往**DevloungePluginSeries**类中添加一个函数。让我叫它**addContent**。

```php

function addContent($content=''){
$content.="Devlounge Was Here";
return $content;
}

```

  

在上面的代码中，发生了以下的事件：

*   上述函数会接受一个参数叫做**content**
*   如果调用时不传递参数，那么content会设定为默认值（空串）
*   参数**content**被附加了一行我们自定义的文本
*   然后重新返回了content

在向类添加了上述函数后，下一步要做的就是将它插入到'**the_content**'中，使得这个函数被调用。

```php

//Actions and Filters
if(isset($dl_pluginSeries)){
//Actions
add_action('wp_head',array(&$dl_pluginSeries,'addHeaderCode'),1);
//Filters
add_filter('the_content',array(&$dl_pluginSeries,'addContent'));
}

```

 

在这段代码的第6行你可以看到，添加了一个叫做'**the_content**'的filter，通过这个filter，我们的函数'**addContent**'会被调用。

如果插件启用，当一篇文章被显示的时候，文本“Devlounge Was Here”将会被显示到文章的末尾。

### 添加一个作者Filter

我在这里要展示另一个使用Filter的例子，我要展示一下怎么操纵显示一个评论的作者。我这里只是简单地让所有的作者名字都用大写显示。

我们只需要往**DevloungePluginSeries**类中添加一个函数。我们叫它**authorUpperCase**。

```php

function authorUpperCase($author=''){
return strtoupper($author);
}

```

在上述代码中，做了这些事情：

上述函数会接受一个参数，叫做**author**

如果没有参数，会被设定成默认值

**author**字符串会以大写的形式返回

在函数被添加到类后，下一步是将它插入到'**get_comment_author**'中使它被调用。

```php

//Actions and Filters
if(isset($dl_pluginSeries)){
//Actions
add_action('wp_head',array(&$dl_pluginSeries,'addHeaderCode'),1);
//Filters
add_filter('the_content',array(&$dl_pluginSeries,'addContent'));
add_filter('get_comment_author',array(&$dl_pluginSeries,'authorUpperCase'));
}

```

像你在第7行看到的，我们添加了一个'**get_comment-author**' filter，然后，我们的函数'**authorUpperCase**'会被调用。

如果插件已经启用，并且一篇日志的评论是可见的，那么评论的作者名字会以大写显示。

### 应用Filter

使用Filter可以做的更强大的是，你可以动态地调用他们。没有必要每次运行都添加一次filter。你可以在任何时候在你的代码里面调用filter。

**apply_filters**的格式是：apply_filter('filter name','you text');

你会在这个系列的后续文章中看到**apply_filters**的例子。