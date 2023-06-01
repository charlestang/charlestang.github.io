---
title: WordPress:插件开发API（Plugin API）
tags:
  - docs
  - WordPress
id: '57'
categories:
  - - wp
    - Plugins Develop
  - - WordPress
date: 2008-05-10 17:05:28
---

## Plugin API

### 介绍

本文当主要介绍[WordPress](http://wordpress.org/ "WP")插件开发者可以使用的API Hook，以及如何使用它们。

本文假设您已经阅读了《[Writing a Plugin](http://codex.wordpress.org/Writing_a_Plugin "Writing a Plugin")》（这篇文章概览了如何写一个插件）。本文主要介绍API Hook，也称作Filter和Action，[WordPress](http://wordpress.org/ "WP")使用这些函数来使您的插件起作用。

注意：本文的内容适用于WordPress1.2+。

### Hook，Action和Filter

Hook是[WordPress](http://sexywp.com/cata/wp "Becoming Charles-WP")提供的一种机制，帮助您将您的插件加入到[WordPress](http://wordpress.org/ "WP")中；也即，在您的插件中，通过调用一些系统函数，使得您的插件可以运作起来。一共有两种Hook：

1.  Action：Action是[WordPress](http://wordpress.org/ "WP")内核在运行到某个特定的点的，或者某个特定的事件发生的时候执行的。您可以通过使用Action API让您的插件中的一个或者多个函数在这些特定的点执行。
2.  Filter：Filter是[WordPress](http://sexywp.com/cata/wp "Becoming Charles-WP")在将一段文本加入到数据库，或者发送给浏览器之前处理不同种类的文本用的。您的插件可以通过使用Filter API，让一个或者多个函数在这些时刻运行，以处理特定类型的文本。

有的时候，您可以使用Action和Filter达到相同的目的。比如说，您希望你的插件可以更改一段日志的文本，您可能会往`publish_post`中添加一个Action函数（这段文字在被加入到数据库之前被修改了），或者往 `the_content`中添加一个Filter函数（这段文字在被发送给浏览器显示之前，被更改了）。

### Action

Action由[WordPress](http://sexywp.com/tags/wordpress "Becoming Charles-WP")中发生的一些特定的事件所触发，比如发布一篇日志，更改主题，或者在管理面板显示一个页面。您的插件可以通过执行一个PHP函数来响应事件，实现以下几个目的：

*   修改数据库数据
*   发送Email信息
*   修改将要在浏览器上呈现的内容（管理员看到的或者访客看到的）

要达到上述的目的，需要遵循的步骤为（下文有详细的描述）：

1.  在您的插件文件中，创建一个在某个事件发生时，需要运行的PHP函数。
2.  通过调用`add_action`函数，将您的函数插入到[WordPress](http://wordpress.org/ "WP")中。
3.  将您的插件文件放到插件目录下，然后激活它。

#### 创建一个Action 函数

在您的插件中创建一个Action的第一个步骤是创建一个能响应Action的函数，并且将它写入到您的插件文件里（您的插件文件最后会被放到_content/plugins_目录）。举个例子，如果您想要您的朋友在您发表了新文章的时候收到一封邮件，您可以创建下述函数：

`function email_friends($post_ID) {   $friends = ‘bob@example.org,susie@example.org’;   mail($friends, "sally’s blog updated",   ‘I just put something on my blog: http://blog.example.com’);   return $post_ID;   }`

对于大多数的Action来说，您的函数要接受一个单一参数（通常是日志或这评论的ID，这要视情况而定）。有些Action接受多于一个的参数，您可以查看WordPress的Action文档，或者直接查看WordPress源代码来取得第一手资料。除了一个参数外，您还可以访问WordPress的全局变量，并且调用其他WordPress函数或者您插件中的其他函数（或者其他插件中的函数）。

**注意**：您要始终留意，是否WordPress本身或者其他的插件已经使用了您想用的那个函数的名字。关于这点，您可以查看[避免函数名冲突](http://codex.wordpress.org/Writing_a_Plugin#Avoiding_Function_Name_Collisions "Avoiding Function Name Collisions")这篇文章来获取更详细的信息。

#### Hook到WordPress

当您定义好您的函数后，下一步就是将您的函数Hook或者注册到WordPress中。在您的插件文件中的全局空间中调用函数 add_action()就可以了：

```php
add_action(’hook_name’, ‘your_filter’, [priority], [accepted_args]);

```

该函数中：

*   `hook_name`是WordPress提供的供hook用的函数名，也即您的函数将关联到的事件的名称。
*   `your_function_name` 是您希望在`hook_name`指定的事件发生时执行的函数的名称。这可以是一个在WordPress中定义好的标准的函数，也可以是一个您自己定义的函数（比如上面提到的`email_friends`）
*   `priority`是一个可选的整型参数，可以指定可以指定关联到某个特定的函数的执行顺序。默认值是10。数字较小的执行较早，如果优先级相同，则按照他们hook进来的顺序先后来执行。
*   `accepted_args`是一个可选的整型参数，它定义了您的函数可以接受多少个参数，默认是1。这个参数很有用，因为有些事件发生的时候，可能会向您的函数传递多于一个的参数。这个参数是从WordPress 1.5.1后的版本才开始有的。

继续前文的例子，我们可以将下面一行代码加入到插件的文件中：

```php
add_filter(’comment_text’,'filter_profanity’);
```

相似的，您也可以将一个函数从Action中移除。你可以参考移除Action来获得详细的信息。

#### 安装和激活

让您的插件奏效的最后一个步骤就是安装和激活和插件了。您写好的函数和对add_action的调用，必须放到同一个文件中，插件文件必须被装到wp-content/plugins目录中。一旦插件安装好，您需要访问管理面板来激活您的插件。

#### 目前已有的Action Hook

参见[Plugin API/Action Reference](http://codex.wordpress.org/Plugin_API/Action_Reference "Plugin API Action Reference")来查看WordPress中的当前的Action列表。

### Filter

Filter是在WordPress执行过程中，传递数据时，在对数据采取某种行动（将数据写入到数据库或者发送给访客的浏览器）之前执行的。（当WordPress生成页面时）Filter就位于数据库和浏览器之间，（当WordPress向数据库添加日志和评论时）Filter就位于浏览器和数据库之间。WordPress中的绝大多数的输入和输出过程都要通过至少一个Filter。WordPress自己有一些默认的Filter，您可以在插件中使用自己的Filter。

将您自己的Filter添加到WordPress中，遵循以下几个步骤：

*   创建一个PHP函数来过滤数据。
*   通过调用add_filter将这个Filter添加到WordPress中。
*   将您的PHP函数写入到一个插件文件中，激活它。

#### 创建一个Filter函数

一个Filter函数把未经修改的数据作为输入，返回修改过的数据（或者有的时候返回的空值，表明这些数据应该被删除）。如果您的Filter没有修改数据，那么原始的数据必须被返回回去，以便于后续的插件可以继续它们的修改工作。

所以，在您的插件中创建一个Filter的第一步，就是创建一个PHP函数来执行过滤动作，并且，将这个函数写入到您的插件文件中去。再举个例子，如果您需要确定您的日志或者评论中没有出现违禁词汇，您可以定义一个全局变量，里面包含了全部的违禁词汇的列表，然后创建下面的PHP函数：

`function filter_profanity($content) {   global $profanities;   foreach($profanities as $profanity) {   $content=str_ireplace($profanity,’{censored}’,$content);   }   return $content;   }`

注意：同样要小心您的函数的命名，不要和其他的WordPress函数和其他插件的函数冲突。

#### 将您的Filter Hook到WordPress

在您的函数定义完毕后，下一步就是将您的函数"hook"或者说注册到WordPress中。在您的插件文件中，调用add_filter函数：

`add_filter(’hook_name’, ‘your_filter’, [priority], [accepted_args]);`

其中：

*   `hook_name` 是WordPress提供的供hook的函数的名称，定义了您可以加入您自己的Filter的插入点。
*   `your_filter`是您的filter函数的名称。这个函数可以是一个WordPress标准PHP函数，也即在WordPress内核中定义的函数，也可以使一个您自己定义的函数。
*   `priority`是一个可选的整型参数，标明了注册到某个特定的filter中的函数的执行顺序。默认是10。较小的数字执行时较靠前。如果priority值相同，那么按照注册的先后顺序来执行。
*   `accepted_args`是一个可选参数，用来标明您的函数能够接受的参数的个数，默认是1，某些hook可以像您的函数传递超过一个的参数。

继续上面的例子，您可以使用下面的代码，让WordPress过滤您评论中的违禁词汇：

`add_filter(’comment_text’,'filter_profanity’);`

您也可以使用`remove_filter()`函数来将一个Filter移除。

#### 安装和激活

最后一个步骤就是使您的filter运作起来。你需要做的就是将您的插件文件放到_wordpress/plugins_目录，然后到后台管理界面激活。

#### 目前WordPress中可以注册的Filter

参见Plugin API/Filter Reference。

#### 例子

下面是一个例子，是Ozh曾经在邮件列表中描述过的，该插件修改（或者说覆盖）了默认的`bloginfo()`函数。这需要修改内核函数的行为。

`add_filter(’bloginfo’, ‘mybloginfo’, 1, 2);   add_filter(’bloginfo_url’, ‘mybloginfo’, 1, 2);`

`function mybloginfo($result=”, $show=”) {   switch ($show) {   case ‘wpurl’:   $result = SITE_URL;   break;   case ‘template_directory’:   $result = TEMPL_DIR;   break;   default:   }   return $result;   }`

### 移除Action和Filter

在某些情况下，您可能会发现，您的插件需要禁用WordPress中的内建Action或者Filter之一，或者某个其它插件添加的函数。您可以通过调用`remove_filter(’filter_hook’,'filter_function’)`或者 `remove_action(’action_hook’,'action_function’)`来达到目的。

比如，`remove_action(’publish_post’,'generic_ping’);`可以在您发表日志的时候，阻止您的博客向外发送ping。

注意，如果一个hook不是使用默认的优先级（priority）注册到系统中，那么您必须在`remove_action()`中指定那个hook使用的优先级。一般来说还要注意，除非您很清楚那个函数在干什么并且为什么要那么做，请不要移除任何函数。

### 缺省加载的Filter和Action

最可靠的获知WordPress缺省加载了哪些Filter和Action的方法就是在其源代码中搜索`add_filter`和`add_action`函数的调用。

#### WordPress 2.1

在WordPress2.1中，绝大多数的Filter和Action的加载是在_wp-include/default-filters.php_文件中进行的。其他的在下列的文件中加载：

*   wp-admin/admin-ajax.php
*   wp-admin/admin-functions.php
*   wp-admin/custom-header.php
*   wp-admin/edit.php
*   wp-admin/index.php
*   wp-admin/options-permalink.php
*   wp-admin/upload-functions.php
*   wp-admin/upload.php
*   wp-includes/bookmark.php
*   wp-includes/general-template.php
*   wp-includes/kses.php
*   wp-includes/plugin.php
*   wp-includes/rewrite.php
*   wp-includes/template-loader.php
*   wp-includes/theme.php

#### WordPress 2.5

(以后我会完善这个部分)

### 您可以覆盖的函数

除了使用hook（action和filter），另一个插件修改Wordpress行为方式是覆盖WordPress的函数。实际上，有一小组函数，是WordPess希望被插件覆盖的。在所有的插件都已经启动后，如果他们还没有被覆盖的话，WordPress才启动这些函数。

这些函数在_wp-include/pluggable.php_文件中定义。这里有一个列表（WP2.1）。

*   set_current_user
*   wp_set_current_user
*   wp_get_current_user
*   get_currentuserinfo
*   get_userdata
*   update_user_cache
*   get_userdatabylogin
*   wp_mail
*   wp_login
*   is_user_logged_in
*   auth_redirect
*   check_admin_referer
*   wp_redirect
*   wp_get_cookie_login
*   wp_setcookie
*   wp_clearcookie
*   wp_notify_postauthor
*   wp_notify_moderator
*   wp_new_user_notification
*   wp_verify_nonce
*   wp_create_nonce
*   wp_salt
*   wp_hash