---
title: WordPress到底在整啥？—(09)
tags:
  - code reading
  - WordPress
id: '112'
categories:
  - - WordPress
date: 2008-07-24 10:48:45
---

依旧续上一篇，仍然是函数参考
<!-- more -->
*   [maybe_unserialize( $original )](#maybe_unserialize)
*   [mysql2date( $dateformatstring, $mysqlstring, $translate = true )](#mysql2date)
*   [nocache_headers()](#nocache_headers)
*   [number_format_i18n( $number, $decimals = null )](#number_format_i18n)
*   [path_is_absolute( $path )](#path_is_absolute)
*   [path_join( $base, $path )](#path_join)
*   [remove_query_arg( $key, $query=FALSE )](#remove_query_arg)
*   [require_wp_db()](#require_wp_db)
*   [size_format( $bytes, $decimals = null )](#size_format)
*   [smilies_init()](#smilies_init)
*   [status_header( $header )](#status_header)
*   [update_option( $option_name, $newvalue )](#update_option)
*   [wp( $query_vars = '' )](#wp)
*   [wp_check_filetype( $filename, $mimes = null )](#wp_check_filetype)
*   [wp_die( $message, $title = '' )](#wp_die)
*   [wp_explain_nonce( $action )](#wp_explain_nonce)
*   [wp_ext2type( $ext )](#wp_ext2type)
*   [wp_get_http( $url, $file_path = false, $red = 1 )](#wp_get_http)
*   [wp_get_http_headers( $url, $red = 1 )](#wp_get_http_headers)
*   [wp_get_original_referer()](#wp_get_original_referer)

**maybe_unserialize**

反串行化。

**mysql2date**

这个函数还是很有用的，可以根据指定的格式来翻译日期字符串，php自己倒是也有日期翻译的函数，这个函数不过是在外面包裹了一层，实现了对于不同语言的日期字符串翻译。

**nocache_headers**

这个函数发送了一个不让浏览器缓存的header。这里很好玩，我看到了一句注释：
why are these @-silenced when other header calls aren't?
这也是我想问的，呵呵。

**number_format_i18n**

返回一个格式化的数字串。

**path_is_absolute**

判断一个路径是否是绝对路径。

**path_join**

连接两个路径，处理好了中间斜杠的数量。原来php有这种可以trim任意字符的函数啊。

**remove_query_arg**

从一个querystring中移除一个或者数个键值对。

**require_wp_db**

这个函数在会在WP中引入DB类对象，这里我们其实可以看出，WP还是给其他类型的数据库留了接口的，你完全可以自己实现一个dp.php然后放杂wp-content目录下面，不过现在到底有没有使用别的数据库系统的wp呢？

**size_format**

humen readable filesize generate。

**smilies_init**

这个函数很有意思的，有一个全局变量叫做$wpsmiliestrans，这个变量里面存储了wp里面默认表情的符号，和图片的对应关系，其实，一直以来，我都觉得这个东西很有问题，这套默认的表情系统与汉字这样的多字节语言的结合不是很好。我在给别人留言的时候，那个表情符号起始的冒号前面必须有一个空格，如果没有，表情图片就不能正确翻译，这真的是让我很困扰，难道就不能换成别的字符码？其实看了sohu（用的shortcode样式），新浪（用的是斜杠），他们的表情翻译系统都工作良好，wp不能在这里有所改进么？

**status_header**

此函数和get_status_header_desc是一对，向浏览器发送一个带有HTTP状态的header。

**update_option**

又是一个option系列函数中的一员。

**wp**

这个函数，本质上就是WP的主函数，这个函数会在wp-blog-header.php中被调用，此函数内部，也调用了WP的main函数，这也放到以后去看吧。当此函数返回的时候，所有的一切就已经准备好了，也就到了装载模板的时候了。

**wp_check_filetype**

该函数接受参数为一个文件名，返回的是一个数组，该数组包括两个字符串，一个是扩展名，一个是相对应的MIME类型串。估计是在处理附件的时候使用的函数。

**wp_die**

这个函数也比较眼熟，前面也遇到过了，调用这个函数，可以显示一个能展示wp出错信息的页面，并且是wp中止运行。

**wp_explain_nonce**

这个函数很搞笑，是一大堆操作失败的提示，暂时还不知道是用在哪里的。

**wp_ext2type**

从扩展名判断文件类型的函数。

**wp_get_http**

哇哈哈，又见递归函数啊，此函数从一个给定的url获取文件，然后将取到的文件写入到参数中指定的文件里面。如果参数中不给出可写的文件，那么该函数会发送一个HTTP HEAD。如果访问的url被重定向，如301或302，那么就递归地重复过程。

**wp_get_http_headers**

就是上面一个函数，只不过省掉了文件名这个参数。

**wp_get_original_referer**

这个函数没有看得很明白，估计以后还会遇到吧。嘿嘿

===============
今天就到这里了~