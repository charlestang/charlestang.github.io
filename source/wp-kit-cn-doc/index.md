---
title: WP Kit CN 文档
id: '176'
tags: []
categories:
  - - uncategorized
date: 2008-08-01 00:37:39
---

[**English Version**](http://sexywp.com/wp-kit-cn-doc-en)

## 目录

1.  [Widget使用说明及设定参考](#widgets-refer)
    
    *   [热评文章Widget](#widget-most-commented)
    *   [最近评论Widget](#widget-recent-comments)
    
2.  [模板标签参考](#tags-refer)
    
    *   [wkc_recent_comments](#wkc_recent_comments)
    *   [wkc_recent_pings](#wkc_recent_pings)
    *   [wkc_recent_posts](#wkc_recent_posts)
    *   [wkc_most_commented_posts](#wkc_most_commented_posts)
    *   [wkc_random_posts](#wkc_random_posts)
    *   [wkc_most_active_commentors](#wkc_most_active_commentors)
    *   [wkc_recent_commentors](#wkc_recent_commentors)
    
3.  [联系作者](#contact_the_author)

## Widget设定参考

### 热评文章Widget

 [
 ![](http://lh3.ggpht.com/_QYicOeu89Bk/STo-lZAPdQI/AAAAAAAAA5k/G8b50alxiZI/s400/wkc_most_commented.png)](http://picasaweb.google.com/lh/photo/d60wugVoaIIyRc67y-9e1w)

热评文章Widget设定界面截图

标题

此Widget在页面侧栏显示的标题

文章数量

热评文章列表中包含的文章数量

几天之内

这是一个为了防止热评文章聚焦效应（人们倾向于查看热评文章，使得热评文章越来越热，永远占据着列表首位）的设计，通过这个参数，可以给进入列表的文章加上时间限制，如15天内发表的热评文章列表，**可以通过指定-1来禁用此项功能**

条目之前标记

一般来说，标题列表使用的HTML标记为<li>，你可以自己给li标签添加id或者class属性，或者干脆不用li标签，默认情况下，会使用li标签，此外，还有一个小小的加号，这个加号继承自中文工具箱的原版，算是原版本的一个小小印记：）

条目之后标记

如果使用li标签，则必须封口

显示的文章类型

此项可以设定页面是否也进入热评文章列表

是否显示评论数量

设定是否显示评论数量，目前其样式无法自定义，显示格式如：（15）

[回到目录](#doc_content)

### 最近评论Widget

[![](http://lh4.ggpht.com/_QYicOeu89Bk/STqEPBQpHbI/AAAAAAAAA50/ATDKHExUBzk/s800/wkc_recent_comments.png)](http://picasaweb.google.com/lh/photo/1eNqORo2U0D1Q6bvgAX8Uw)

From [illustration](http://picasaweb.google.com/TangChao.ZJU/Illustration)

标题

此Widget在页面侧栏显示的标题

评论数量

显示的评论的条数

条目之前标记

一般来说，标题列表使用的HTML标记为<li>，你可以自己给li标签添加id或者class属性，或者干脆不用li标签，默认情况下，会使用li标签，此外，还有一个小小的加号，这个加号继承自中文工具箱的原版，算是原版本的一个小小印记：）

条目之后标记

如果使用li标签，则必须封口

评论内容长度

截断评论显示的字数

排除用户

不希望某位用户的评论显示在最近评论列表里，**可以指定多位，使用半角逗号分隔**

Gravatar头像尺寸

如果要在最近评论列表里显示头像，在这里设定尺寸

评论自定义格式

设置评论列表显示的格式，这里可以使用xformat格式，支持的变量如下：

*   %post_title%—文章的标题
*   %comment_count%—该篇文章的评论数量
*   %comment_auhtor%—评论作者
*   %comment_auhtor_url%—评论作者的网站
*   %permalink%—该条评论的永久链接
*   %comment_excerpt%—评论摘要
*   %gravatar%—头像

 上面的图是对最新评论Widget的设定说明，最底下的那个参数，在我的文章[《WP Kit CN再次更新》](http://sexywp.com/wp-kit-cn-update-again.htm)里还有个例子。
 

```html

            %gravatar%%comment_author%: %comment_excerpt%
 
```


 
       

[回到目录](#doc_content)

## 模板标签参考

此节，将提供一个模板标签的调用参考手册。WP Kit CN的模板标签采用了统一的风格，都是wkc开头的函数，参数采用字符串给出。

1.  [wkc_recent_comments](#wkc_recent_comments)
2.  [wkc_recent_pings](#wkc_recent_pings)
3.  [wkc_recent_posts](#wkc_recent_posts)
4.  [wkc_most_commented_posts](#wkc_most_commented_posts)
5.  [wkc_random_posts](#wkc_random_posts)
6.  [wkc_most_active_commentors](#wkc_most_active_commentors)
7.  [wkc_recent_commentors](#wkc_recent_commentors)

[回到目录](#doc_content)

* * *

### wkc_recent_comments

此函数显示最新评论的列表。接受参数为：

*   `number`——显示最新评论的条数，默认5条。
*   `before`——列表表项前使用的代码，默认<li>。
*   `after`——列表表项后面使用的代码，默认</li>。
*   `showpass`——是否显示密码保护文章的评论，默认0（不显示）。1为显示
*   `length`——评论截断的字数，默认50。
*   `skipuser`——不显示某个用户的评论，默认为admin。留空显示所有评论。
*   `echo`——是否直接打印，默认为1（打印）。选0，则直接返回数据库查询结果，是一个数组。

  

使用范例：

    
 

[回到目录](#doc_content)

* * *

### wkc_recent_pings

此函数显示最新回响的列表。接受参数为：

*   `number`——显示最新评论的条数，默认5条。
*   `before`——列表表项前使用的代码，默认<li>。
*   `after`——列表表项后面使用的代码，默认</li>。
*   `showpass`——是否显示密码保护文章的评论，默认0（不显示）。1为显示
*   `length`——评论截断的字数，默认50。
*   `type`——回响的类型，默认为both，可选pingback或trackback。
*   `nopings`——如果回响不存在显示的文字，默认为No Pings。
*   `echo`——是否直接打印，默认为1（打印）。选0，则直接返回数据库查询结果，是一个数组。

  

使用范例：

    
 

[回到目录](#doc_content)

* * *

### wkc_recent_posts

此函数显示最新文章的列表。接受参数为：

*   `number`——显示最新文章的条数，默认5条。
*   `before`——列表表项前使用的代码，默认<li>。
*   `after`——列表表项后面使用的代码，默认</li>。
*   `showpass`——是否显示密码保护文章的评论，默认0（不显示）。1为显示
*   `skip`——跳过前面多少篇，默认0
*   `echo`——是否直接打印，默认为1（打印）。选0，则直接返回数据库查询结果，是一个数组。

  

使用范例：

    
 

[回到目录](#doc_content)

* * *

### wkc_most_commented_posts

此函数显示评论最多文章的列表。接受参数为：

*   `number`——显示最新文章的条数，默认5条。
*   `days`——几天之内的热评文章，默认7天
*   `before`——列表表项前使用的代码，默认+。
*   `after`——列表表项后面使用的代码，默认<br />。
*   `posttype`——显示的文章的类型post（日志）还是page（页面）还是both，默认post。
*   `showcount`——是否在文章标题后面显示评论数量。默认值1，表示显示，可选值0，表示不显示。
*   `echo`——是否直接打印，默认为1（打印）。选0，则直接返回数据库查询结果，是一个数组。

  

使用范例：

    
 

[回到目录](#doc_content)

* * *

### wkc_random_posts

此函数显示随机文章的列表。接受参数为：

*   `number`——显示最新文章的条数，默认5条。
*   `length`——自动文章摘要的长度，默认400字
*   `before`——列表表项前使用的代码，默认<li>。
*   `after`——列表表项后面使用的代码，默认</li>。
*   `showpass`——是否显示密码保护的文章名称，默认0，不显示，1表示显示。
*   `showexcerpt`——是否在链接title属性中显示摘要，默认1，0表示直接显示文章摘要，不在链接title中显示。
*   `echo`——是否直接打印，默认为1（打印）。选0，则直接返回数据库查询结果，是一个数组。

  

使用范例：

    
 

[回到目录](#doc_content)

* * *

### wkc_most_active_commentors

此函数显示活跃用户的列表。接受参数为：

*   `threshhold`——上榜用户最少评论数，默认5。
*   `days`——时间期限，默认7天内。
*   `skipuser`——被排除的用户名，默认admin。改参数用于屏蔽作者自己的显示。
*   `before`——列表项之前显示的html标签，默认值为<li class="wkc_most_active">
*   `after`——列表项之后显示的html标签，默认值为</li>
*   `echo`——是否直接打印，默认为1（打印）。选0，则直接返回数据库查询结果，是一个数组。

  

使用范例：

    
 

[回到目录](#doc_content)

* * *

### wkc_recent_commentors

此函数显示最近留言用户的列表。接受参数为：

*   `threshhold`——上榜用户最少评论数，默认-1，表示没有限制。
*   `type`——本周内或者本月内，默认week，可选值为month。
*   `skipuser`——被排除的用户名，默认admin。改参数用于屏蔽作者自己的显示。
*   `before`——列表项之前显示的html标签，默认值为<li class="wkc_recent_commentors">
*   `after`——列表项之后显示的html标签，默认值为</li>
*   `echo`——是否直接打印，默认为1（打印）。选0，则直接返回数据库查询结果，是一个数组。

  

使用范例：

    
 

[回到目录](#doc_content)

## 与作者取得联系

如果上面的帮助有不详细的，或者插件有bug，请联系我：

[回到目录](#doc_content)