---
title: WordPress到底在整啥？—(10)
tags:
  - code reading
  - WordPress
id: '113'
categories:
  - - WordPress
date: 2008-07-29 01:24:19
---

看官要烦死了吧，还是函数参考
<!-- more -->
*   [wp_get_referer()](#wp_get_referer)
*   [wp_load_alloptions()](#wp_load_alloptions)
*   [wp_maybe_load_widgets()](#wp_maybe_load_widgets)
*   [wp_mkdir_p( $target )](#wp_mkdir_p)
*   [wp_nonce_ays( $action )](#wp_nonce_ays)
*   [wp_nonce_field( $action = -1, $name = "_wpnonce", $referer = true , $echo = true )](#wp_nonce_field)
*   [wp_nonce_url( $actionurl, $action = -1 )](#wp_nonce_url)
*   [wp_ob_end_flush_all()](#wp_ob_end_flush_all)
*   [wp_original_referer_field( $echo = true, $jump_back_to = 'current' )](#wp_original_referer_field)
*   [wp_parse_args( $args, $defaults = '' )](#wp_parse_args)
*   [wp_protect_special_option( $option )](#wp_protect_special_option)
*   [wp_referer_field( $echo = true)](#wp_referer_field)
*   [wp_remote_fopen( $uri )](#wp_remote_fopen)
*   [wp_unique_filename( $dir, $filename, $unique_filename_callback = NULL )](#wp_unique_filename)
*   [wp_upload_bits( $name, $deprecated, $bits, $time = NULL )](#wp_upload_bits)
*   [wp_upload_dir( $time = NULL )](#wp_upload_dir)
*   [wp_widgets_add_menu()](#wp_widgets_add_menu)
*   [xmlrpc_getpostcategory( $content )](#xmlrpc_getpostcategory)
*   [xmlrpc_getposttitle( $content )](#xmlrpc_getposttitle)
*   [xmlrpc_removepostdata( $content )](#xmlrpc_removepostdata)

**wp_get_referer**

这个没有看懂，先放着。

**wp_load_alloptions**

options系列的，先放着。

**wp_maybe_load_widgets**

加载侧边栏Widget支持。

**wp_mkdir_p**

这个函数的作用相当于mkdir命令，就是创建一个目录。但是这个函数写得来真是……递归！这个函数可以创建层叠的不存在目录，比如你可以直接创建"wp-content/myowndir/subdir"，如果直接创建失败，该函数递归的去创建父级目录，我太孤陋了，从没有思考过这些方法，真不错啊

**wp_nonce_ays**

**wp_nonce_field**

**wp_nonce_url**

以上几个函数没有看懂啊。

**wp_ob_end_flush_all**

关闭所有的output buffer。

**wp_original_referer_field**

带referer的这一族函数都让人不知从哪里下手啊。

**wp_parse_args**

这个函数将返回一个数组，接受的参数是一个对象或者数组，一半是用来处理参数，将设定好的参数和默认的参数合并。这个函数应该学习使用下，因为从调用引用来看，引用到这个函数的地方很多，还有很多插件也在用这个函数处理参数。

**wp_protect_special_option**

options系列函数。

**wp_referer_field**

这个又是那个让我看不懂的带referer的函数。

**wp_remote_fopen**

这个函数打开了远程的文件，并读取其内容，这种情况下一般使用CURL来处理，使用这个函数的好处是，兼容没有CURL的情况。

**wp_unique_filename**

通过这个函数可以获得一个唯一的文件名。

**wp_upload_bits**

这个函数是一个将上传文件写到服务器硬盘的函数。前面的几个函数在这里都出现了，包括unique_filename，mkdir等等。

**wp_upload_dir**

返回一个包含着上传文件存储目录的信息的数组。好像没什么特别的。

**wp_widgets_add_menu**

这个函数是[wp_maybe_load_widgets()](#wp_maybe_load_widgets)里面hook到_admin_menu的函数。

**xmlrpc_getpostcategory**

从这里开始的以下三个函数，如果我没有猜错的话，应该是在使用xmlrpc的时候，用来从传来的xml文件中提取信息的。此函数提取分类名称。

**xmlrpc_getposttitle**

此函数提取文章标题。

**xmlrpc_removepostdata**

此函数提取文章内容。