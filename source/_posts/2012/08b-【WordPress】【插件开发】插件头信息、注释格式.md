---
title: 【WordPress】【插件开发】插件头信息、注释格式
tags: []
id: '499'
categories:
  - [工作相关, 心得体会]
  - [WordPress, Plugins Develop]
date: 2012-08-15 01:41:58
permalink: wordpress-plugin-develop-header-info/
---

WordPress后台可以看到已安装插件的列表，其中会显示插件的名称（Plugin Name），简要描述（Dsecription），版本（Version），作者（Author），作者主页（Author URI），插件主页（Plugin URI），这些信息并非是存在数据库里的，而是写在了插件入口文件的头部，以注释的形式写在了插件页面中。这种形式，可以将WP系统和插件软件同步元数据信息的成本和复杂度降到最低。
<!-- more -->
## 插件元数据字段

一个插件的元数据字段，到底有几个呢？每个分别又有些什么用途，你可以选择看官方文档，官方文档一般会提供相关说明，但是我认为官方文档也大部分由志愿者来维护，所以，经常没有说出全部的内容，所以，真想彻底搞清楚一切，还是要看源代码，源代码里面没有秘密。

下面罗列了从WP 3.5 alpha版本源代码中看来的，关于插件头的字段，具体查询在文件`/wp-admin/includes/plugin.php`中的`get_plugin_data`函数。

（注：我从WP1.3版本开始玩，现在已经3.5，发展速度非常快，代码变化也非常大，但是常年跟踪下来发现，WP的根本原理还是相当稳定的，所以，本文例子的时效性不会太长，读者应该着力本文描述的方法和阐述的思想，不应拘泥于本文的实际例子。）

 

```php


 Plugin URI: <插件主页网址>
 Version: <版本11.0>
 Description: <插件简要说明>
 Author: Charles Tang
 Author URI: http://blog.charlestang.org/
 Text Domain:[可选:这个用于l10n配置，下文解释]
 Domain Path:[可选:这个用于指定路径，下文解释]
 Network:[可选:bool类型，缺省false，下文解释]
 */

```

## 元数据字段功能分析说明

特意去查看了官方文档关于插件头（headers）部分的说明，比此文上述代码片段罗列的多了一个License字段，少了后面三个看起来很神秘的字段。

上面六个字段，非常容易理解，就不赘述了，License字段就是完全自选字段了，因为读取插件信息的函数，并没有真的去解析，所以大家可以视个人喜好决定是不是指定许可协议，协议字段的格式也是完全随意的。

下面重点说说下面三个字段是干什么用的。

WordPress支持l10n，就是本地化，所有的字符串如果在插件开发的时候，都指定了domain，并用翻译函数返回，那么，后续只要配置好相关的翻译文件，那么就可以实现字符串的本地化了。

插件载入时候，一般会在缺省的路径尝试加载翻译文件，如果翻译文件不在默认路径（一般都不在），就不加载，但是允许在代码中手动调用load_textdomain函数来手动加载翻译文件。

但是插件的元信息是用注释的形式写成的，而且实际WP在读取插件元信息（Meta Data）的时候，也只是通过正则截取的内容，不可能执行翻译函数，所以，就出现了Text Domain字段和Domain Path字段，第一个指定了翻译文件的domain，第二个指定了翻译文件的路径，有了这两个东西，插件管理页面在渲染插件列表的时候，就会正确按照用户配置的语言来载入存在的翻译文件的内容了。

Text Domain指定的值为你的domain字符串，Domain Path的值应该为一个路径，以/开头，路径为相对路径，相对的是这款插件的目录。可以使用..表示父级目录向上回溯，一般会把翻译文件放在wp-content下面的某个目录下。翻译文件的命名也是有规则的，一般是-.mo，比如Flash MP3 Player的中文翻译文件为fmp-zh_CN.mo只有这样，WP才能正确加载翻译文件。

最后一个字段Network，是我们一般用不到的，设为true，表示这个插件只能用于Multi Site的情况，是使用WordPress做博客网络，多站点运营的时候使用到的一个参数。