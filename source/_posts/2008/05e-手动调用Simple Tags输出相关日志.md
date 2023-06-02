---
title: 手动调用Simple Tags输出相关日志
tags:
  - DIY
  - plugins
  - usage
  - WordPress
id: '55'
categories:
  - WordPress
date: 2008-05-13 16:42:44
permalink: use-simple-tags-mannually-to-output-related-posts/
---

Simple Tags是一款非常优秀的插件，在WordPress原生支持tags后，Simple Tags因为其强大的tags管理功能成为了一款必不可少的插件。

经历了几个版本的演化后，Simple Tags的功能已经越来越强。输出相关日志的功能最终也被集成到了其中。在Simple Tags后台页面，通过简单的设置，就可以轻易实现在Feed、帖子页中，输出相关日志。

但是，通过后台设定添加的相关日志列表不能控制其出现的位置，Simple Tags采用filter来将相关日志列表追加到了文章内容的末尾（关于filter的说明，可以参考[我翻译的文档](http://sexywp.com/wp-docs-plugin-api.htm "WordPress Plugin API")），很多WPer都会在文章末尾添加很多东西，比如版权（如本站），社会化书签，有的还有广告等等，如果相关日志列表没有出现在合适的位置，不但影响美观，还会影响用户友好。

解决办法一般就是采用专门的Related Posts插件，比如[我爱水煮鱼，就提供了一个这样的插件](http://fairyfish.net/2007/09/12/wordpress-23-related-posts-plugin/ "WP-Related-Post")，使用起来也相对简便。现在，大家又有一个选择了，因为，按照查理的理论，同样是直接在页面模板中插入代码，插入一行和插入三行，是完全一样的。既然这样，为什么要多安装一个插件呢？（关于效率和功能的强大与否，查理没有对比过，所以，也就没有什么发言权了，所以，这也不是非要使用这个方法的一个理由，有兴趣研究的同学，可以把你的结果告诉查理，我会把你文章的permalink，添加在本文中）。

好了，闲话已毕，我们来看正题，首先我就把那三行代码贴在这里吧，全部采用默认设置输出相关日志的话，看到这里就可以大功告成了！在你自己的模板文件的single.php（如果使用K2，那么是theloop.php）中的合适位置，加入下面的代码即可输出10篇相关日志列表，如本站效果。

```php
if (is_single() && function_exists('st_related_posts')) { 
    st_related_posts('number=10&include_page=false&order=data-asc'); 
} 
```

简单解释一下，`st_related_posts()`是Simple Tags插件提供的公用函数，可以直接输出相关日志列表。

1.  **`number`**–输出相关文章的数量
2.  **`order`**–输出相关文章的排序。可选值：
    
    *   date-asc - 旧日志在前
    *   date-desc - 新日志在前
    *   count-asc - 相同标签数少的日志在前
    *   count-desc - 相同标签数多的日志在前（默认）
    *   name-asc - 字母顺序
    *   name-desc - 字母倒序
    *   random - 随机
    
3.  **`format`**–不建议设定此参数，用法[参见文档](http://code.google.com/p/simple-tags/wiki/RelatedPosts)
4.  **`separator`**–不建议设定此参数，用法[参见文档](http://code.google.com/p/simple-tags/wiki/RelatedPosts)
5.  **`include_page`**–`true`表示包括页面；`false`表示不包括
6.  **`include_cat`**–需要包含的分类的ID，用半角逗号间隔，不设代表所有分类
7.  **`exclude_posts`**–不想包含的日志ID，用半角逗号间隔
8.  **`exclude_tags`**–不想包含的tags的ID，用半角逗号间隔
9.  **`post_id`**–不建议设定此参数，用法[参见文档](http://code.google.com/p/simple-tags/wiki/RelatedPosts)
10.  **`excerpt_wrap`**–不建议设定此参数，用法[参见文档](http://code.google.com/p/simple-tags/wiki/RelatedPosts)
11.  **`limit_days`**–多少天内的相关日志，不设代表所有日志
12.  **`min_shared`**–包含相同tag的数量，默认1（两篇文章有一个相同tag），设得越大，相关日志越少
13.  **`title`**–日志列表前的标题，可以使用html标签，如<h4>
14.  **`nopoststext`**–没有相关日志时候显示的文本。需要一个字符串，请用单引号括起来。
15.  **`dateformat`**–显示日期的格式，默认和WP的格式相同，想要修改的话参见PHP时间函数的参数设定格式
16.  **`xformat`**–扩展链接格式，默认的就很不错了，想要修改的，看文档吧，或者在Simple Tags的后台也可以设定