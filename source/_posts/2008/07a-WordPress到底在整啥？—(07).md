---
title: WordPress到底在整啥？—(07)
tags:
  - code reading
  - WordPress
id: '110'
categories:
  - WordPress
date: 2008-07-09 11:17:29
permalink: inside-wordpress-07/
---

好吧，还是来到这里了，这回还是支线情节，但是由于其趣味性和实用性，我还是想写写……

### 百宝箱functions.php

这个文件确实是一个百宝箱，里面什么都有，我打算分个几次把这里的函数都给罗列一遍，以后就当成我自己的函数参考好了。呵呵……
<!-- more -->
*   [_config_wp_home( $url = '' )](#_config_wp_home)
*   [_config_wp_siteurl( $url = '' )](#_config_wp_siteurl)
*   [_deprecated_file($file, $version, $replacement=null)](#_deprecated_file)
*   [_deprecated_function($function, $version, $replacement=null)](#_deprecated_function)
*   [_mce_set_direction( $input )](#_mce_set_direction)
*   [absint( $maybeint )](#absint)
*   [add_magic_quotes( $array )](#add_magic_quotes)
*   [add_option( $name, $value = '', $deprecated = '', $autoload = 'yes' )](#add_option)
*   [add_query_arg()](#add_query_arg)
*   [apache_mod_loaded($mod, $default = false)](#apache_mod_loaded)
*   [bool_from_yn( $yn )](#bool_from_yn)
*   [build_query( $data )](#build_query)
*   [cache_javascript_headers()](#cache_javascript_headers)
*   [current_time( $type, $gmt = 0 )](#current_time)
*   [date_i18n( $dateformatstring, $unixtimestamp )](#date_i18n)
*   [dead_db()](#dead_db)
*   [debug_fclose( $fp )](#debug_fclose)
*   [debug_fopen( $filename, $mode )](#debug_fopen)
*   [debug_fwrite( $fp, $string )](#debug_fwrite)
*   [delete_option( $name )](#delete_option)

**_config_wp_home**

这个函数真是让我相当匪夷所思的，为啥？因为这个函数根本没用！唯一使用到的地方就是有一个filter，叫做option_home，而这个filter却从来也没有apply过。很无语……或许是WPMU用的函数？

**_config_wp_siteurl**

这个函数同上一个函数，也没用，绑定到了option_siteurl这个filter上，但是从来也没有调用过……

**_deprecated_file**

告知一个文件已经不建议使用，并且告知使用哪个文件来替代。

**_deprecated_function**

告知一个函数已经不建议使用，并且告知使用哪个函数来替代。检索这个关键字，可以看到所有过期的函数。

**_mce_set_direction**

这是一个filter（tiny_mce_before_init），其作用是在MCE（也就是撰写文章时候的那个编辑器）初始化之前，更改mce的方向，有些国家的人写在是从右往左写的哦~~~

**absint**

绝对值。

**add_magic_quotes**

哈哈^_^，递归！！这个函数本质上就是对数组中的每一个值，运行一次addslashes，说起来PHP的数组，确实是一种树状结构的，只是这个叶子数是很随意的。从这个函数中，可以学习学习遍历数组的递归方法呢~~呵呵

**add_option**

哎呀，按照字母序看来也是有很大的弊端的，比如这个函数，就是options相关函数群中的一个，怎么办呢？这个问题先放一放吧。唉……

**add_query_arg**

这个函数的功能是在一个已经有的uri里面增加一个key value对，形成新的uri。

**apache_mod_loaded**

这个函数有用，可以判断apache服务器是否有安装某个模块。其判断方法也不错，值得学习，一是通过apache_get_modules函数直接取得已经安装的mod的数组，如果该函数不可用，可以通过phpinofo(8)来获得一个字符串，判断是否在这个字符串中包含mod的名字，呵呵，长见识了。

**bool_from_yn**

把“y”和“n”变成bool值，也即true或false。

**build_query**

我前面介绍过compat.php这个文件，里面提到了WP自己修补了PHP5不存在的函数http_build_query 。其作用就是将一个数组转换成url的形式。这个函数没啥的，就是调用了这个函数，不过很值得怀疑的一点是，这里为什么调用的是它自己修补的那个版本呢？应该直接调用http_build_query这个函数的，因为已经经过compat.php的修补，一定不会有问题的。真是莫名啊……

**cache_javascript_headers**

这个东西也是相当的有用哦~调用这个函数，可以发送一个header，要求浏览器缓存一个js文件十天。我搜索了一下WP的所有文件，发现，没有一个地方调用过这个函数的，估计这个函数就是用来让插件或者主题的作者调用的。有些插件会通过PHP生成javascript文件，调用这个函数，可以让php生成的js缓存十天。

**current_time**

返回表示当前时间的字符串。

**date_i18n**

这个函数的作用呢，就是返回一个表示时间的字符串，而且这个字符串是符合WP设定的那种语言的语言习惯的。

**dead_db**

当建立数据库连接发生错误的时候，打印一个页面告知错误，并中止WP的继续运行。

**debug_fclose**

本质上就是fclose。这个函数包括后续的3个，正好就是一套函数，看代码来说，是在$debug这个全局变量的控制下，向文件写入调试信息的一个方法，只是不知道这个$debug是在何处开启的，还是直接在config里面手动设定一下就ok？

**debug_fopen**

打开文件。

**debug_fwrite**

向文件写入字符串。

**delete_option**

option系列函数，以后专门开一篇文章分析一下吧。