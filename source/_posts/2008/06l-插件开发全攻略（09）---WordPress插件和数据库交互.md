---
title: 插件开发全攻略（09）---WordPress插件和数据库交互
tags:
  - develop
  - plugins
  - translate
  - WordPress
id: '99'
categories:
  - [WordPress, Plugins Develop]
date: 2008-06-23 15:58:48
permalink: how-to-write-a-wp-plugin-09/
---

当你编写一个插件的时候，你将不可避免地要将一些变量存储到数据库，或者将它们从数据库中取出。幸运的是，WordPress通过options和一个数据库对象，使得存取数据变得很简单。本文将会谈及如何在一个WordPress数据库中存储或者取回数据。
<!-- more -->
### 在数据库中存储数据

将数据存储到WordPress数据库，主要有两种方法：

1.  创建你自己的表。
2.  使用Options

由于绝大多数插件不需要它们自己的表，所以，我将只讨论使用options的方法。然而，WordPress Codex上面详细讨论了怎样设定你自己的表的方法。

### WordPress Options

使用WordPress Options，在数据库存储和取回数据就跟函数调用一样简单。WordPress为options提供了四个函数：

*   add_option
*   get_option
*   update_option
*   delete_option

#### add_option

 **add_option** 函数接受四个参数，option的名字是必须的。四个参数是： `add_option($name,$value,$description,$autoload);` 

使用这个函数来添加将来要从数据库中取出的数据是很有好处的。

参数 **$name** 必须是独一无二的，否则你就会覆盖别人的option，或者别人会覆盖你的option。

我通常不用这个函数，因为 **update_function** 完全可以做相同的事情。

#### get_option

 **get_option** 函数允许你取回事先存储在数据库里的option。它只接受一个参数，就是option的名字。函数的格式是： `get_option($option_name);` 

#### update_option

 **update_option** 函数工作方式和 **add_option** 是一样的，除此之外，如果option已经存在，该函数会更新option的值。当往数据库中存储数据的时候，我个人喜欢使用这个双重功能的函数，尤甚于 **add_option** 。

#### delete_option

 **delete_option** 函数从数据库中删除options。函数的格式是： `delete_option($option_name);` 

### 一个代码范例

你可能会回忆起这个系列以前的文章中，我把options以array的形式存入数据库。这里是一个例子，并且还有一些说明分析：

```php

//Returns an array of admin options
function getAdminOptions() {
$devloungeAdminOptions = array('show_header' => 'true',
'add_content' => 'true',
'comment_author' => 'true',
'content' => '');
$devOptions = get_option($this->adminOptionsName);
if (!empty($devOptions)) {
foreach ($devOptions as $key => $option)
$devloungeAdminOptions[$key] = $option;
}
update_option($this->adminOptionsName, $devloungeAdminOptions);
return $devloungeAdminOptions;
}

```

在第 3-6 行，我创建了一个最终要作为option存入WordPress数据库（ 12 行）的数组。我这么做是因为我不需要存储多个选项（每个选项都要查询一次数据库）。这个技术对代码臃肿，数据库查询和名字冲突都有所助益。

### WordPress 数据库类

另一个在WordPress数据库存储和取回数据的强大的方法是使用WordPress数据库类对象。在一个函数中，这个类对象的引用方式如下：

```php

function sample_function() {
global $wpdb;
}

```

在这个变量被引用了以后，你可以访问《[wpdb类中许多有用的函数](http://codex.wordpress.org/Function_Reference/wpdb_Class)》。

举例来说，假如我们想要取回WordPress博客的评论的总数。这是一个函数，通过使用WPDB类来实现这个目的：

```php

function sample_function() {
global $wpdb;
$comments = $wpdb->get_row("SELECT count(comment_approved) comments_count FROM $wpdb->comments where comment_approved = '1' group by comment_approved", ARRAY_A);
echo $comments['comments_count'];
}

```

上述函数完成了如下工作：

*   第2行，我们添加了一个 `$wpdb` 的引用。
*   第3行，我们调用了一个wpdb类内部的函数 `**get_row**`
*   第3行，我们从评论表（ `$wpdb->comments` ）中取回数据。这里我们指定返回的数据为一个联合数组（ARRAY_A）。
*   第4行，我们打印出结果。因为我希望数据的放回形式是联合数组，我只要调用我在SQL语句中赋值的变量就可以了，也就是 `**comments_count**`

**wpdb** 类是一个有着许多功能的非常大的类。我建议查看一下 [WPDB类页面](http://codex.wordpress.org/Function_Reference/wpdb_Class) ，看看**wpdb类**到底可以干些什么。