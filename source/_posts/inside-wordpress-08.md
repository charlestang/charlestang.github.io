---
title: WordPress到底在整啥？—(08)
tags:
  - code reading
  - WordPress
id: '111'
categories:
  - - WordPress
date: 2008-07-14 12:34:04
---

续上一篇，继续函数参考
<!-- more -->
*   [do_enclose( $content, $post_ID )](#do_enclose)
*   [do_feed()](#do_feed)
*   [do_feed_atom( $for_comments )](#do_feed_atom)
*   [do_feed_rdf()](#do_feed_rdf)
*   [do_feed_rss()](#do_feed_rss)
*   [do_feed_rss2( $for_comments )](#do_feed_rss2)
*   [do_robots()](#do_robots)
*   [form_option( $option )](#form_option)
*   [get_alloptions()](#get_alloptions)
*   [get_num_queries()](#get_num_queries)
*   [get_option( $setting )](#get_option)
*   [get_status_header_desc( $code )](#get_status_header_desc)
*   [get_weekstartend( $mysqlstring, $start_of_week = '' )](#get_weekstartend)
*   [is_blog_installed()](#is_blog_installed)
*   [is_lighttpd_before_150()](#is_lighttpd_before_150)
*   [is_new_day()](#is_new_day)
*   [is_serialized( $data )](#is_serialized)
*   [is_serialized_string( $data )](#is_serialized_string)
*   [make_url_footnote( $content )](#make_url_footnote)
*   [maybe_serialize( $data )](#maybe_serialize)

**do_enclose**

很老实地说，目前还没有看懂这个函数呢！！

**do_feed**

嘿嘿，这个函数真的是非常好玩啊，让我终于找到了以前一直想做但是没有做成的一个功能的方法。这个函数包括下面4个do_feed_xxx函数，是一组，就写这么一段吧。这个函数，揭示了wp输出feed的方法，首先，从query string中提取出关于feed的那个变量，然后，用此变量生成一个hook，检查这个hook是否存在，如果不存在，则wp_die，如果存在，则触发action。

我举个例子吧，比如要访问我的feed：

http://sexywp.com/?feed=rss2

然后，do_feed被调用，然后wp得到了需要的类型“rss2”。

接着，生成一个hook名称叫做“do_feed_rss2”，然后检查这个hook是否存在（当然存在了！就在下面）。

然后，触发action do_feed_rss2。（这个action是在default-filters.php里面添加的）

**do_feed_atom**

**do_feed_rdf**

**do_feed_rss**

**do_feed_rss2**

**do_robots**

这个函数呢，我在这里大胆猜测一下它的功能吧，记得安装WP的时候，让大家选择是否允许google，百度等搜索引擎索引你的博客，这个“允许”，或者“不允许”，就是使用robots.txt这个东西来实现的，具体的使用方法，可以参看http://www.robotstxt.org/，其实，使用wp博客，设定比较合理的robots.txt也是比较重要的，也是seo的一个方面。至于如何设定，其实有个捷径，就是找到你心目中的牛博，直接抄它的robots.txt就OK啦，嘿嘿，够坏吧。

**form_option**

没看明白这个是干啥的，只有一行，信息太少了。以后再说。

**get_alloptions**

取得所有的option。这个应该归入option系列函数的一类，以后专门分析吧。

**get_num_queries**

用在模板里面，用来显示一种执行了多少次query的一个函数，直接打印出来。不过呢，这个query数量一定是要使用wpdb对象执行的才行哦~~

**get_option**

option系列函数。

**get_status_header_desc**

这个函数里面提供了一个http状态编号对应的含义的列表，可以用来查询http状态。后面有一个status_header函数会调用这个函数，差不多是整个wp仅有地调用这个函数的函数。用来查询状态文字，然后作为header发送给agent。

**get_weekstartend**

又是一个只用到一次的函数，在wp-get_archives里面调用的。

**is_blog_installed**

通过在数据库里面查询来判断是否安装。

**is_lighttpd_before_150**

对服务器版本的判定

**is_new_day**

超简单的一个函数，不过没看出是干啥用的。

**is_serialized**

判断一个变量的内容是否已经串行化，很多正则，没有看懂。

**is_serialized_string**

同上。

**make_url_footnote**

这个函数可是很好玩的哦，可以把文章中所有的超链接都转变成脚注。目前只有the_content_rss里面调用过这个函数，不过，据我所见的，还没有人通过参数启用这个功能。奇怪的东西真多，这里面有个抽取链接的正则表达式，倒是可以摘抄一下，不错。
'/<a(.+?)href=\"(.+?)\"(.*?)>(.+?)<\/a>/'

**maybe_serialize**

这个是wp用到的串行化函数，如果本身是string，这个函数，就trim一下，如果本身是数组或者对象，这个函数调用serialize方法，最奇怪的是，如果参数本身已经是经过串行化的，还是会调用一次serialize方法，这个就非我所能懂了，记录一下吧。