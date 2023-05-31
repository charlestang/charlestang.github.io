---
title: 【WordPress】【插件开发】【插件】简易下载链接计数器
tags:
  - develop
  - plugins
  - source code
  - WordPress
id: '550'
categories:
  - - wp
    - Plugins Develop
  - - WordPress
date: 2013-05-01 23:57:57
---

写PHP是我工作的主要内容之一，我尤其喜欢使用的IDE是Netbeans，所以，之前心血来潮，做了一个Netbeans的皮肤站点（[http://netbeanstheme.com](http://netbeansthemes.com/ "Netbeans Themes")）供大家交流Netbeans配色方案用。

因为是心血来潮，就要一个“快”字，火速申请域名，用WordPress搭了小站，然后用了一个极简的Portfolio类型的皮肤，每个Post一个Feature Image作为截图预览，然后用Custom Fields来记录下载链接，一个Download键用来记录链接，一个Author域用来记录作者，然后又用cformsII插件做了一个上传皮肤配置文件的表单，一个小站就算完毕了。

然后，网上随便挂了几个月，发现貌似挺受欢迎，获得了很多的反响。于是乎，发现一个现象，就是有些皮肤下载的人多，有些下载的人少，根据留言数目看出来的。当然了，做互联网的这种直觉一开始就该有的，当初太偷懒了。当然，现在也不迟啦，马上加一个统计，记录所有的配色方案的下载次数。既要兼容以前已经有的Post，又要使用简单，肿么办？
<!-- more -->
继续使用Custome Fields作为计数器的变量，然后，使用[WP AJAX API](http://codex.wordpress.org/AJAX_in_Plugins "AJAX_in_Plugins")作为Download Request的Handler，使用插件注入一段代码，实行统计和下载代理的功能。轻松搞定这个问题。怎么会想到这样做的？就是玩WordPress很多年的一种直觉……（草）以下给出整个插件的完整源代码，供大家参悟。一共72行代码，连写带调试带上线部署2小时，有疏漏之处，请指正。后续可以继续扩展比较复杂的功能，比如防盗链，按照下载次数排序等功能，不一一详述，供诸君举一反三。

```php

This link is broken';
 echo 'Back';
 die(0);
 }
 $download = get_metadata('post', $post_id, 'Download', true);
 if (empty($download)) {
 echo 'This link is broken';
 echo 'Back';
 die(0);
 }

 $count = get_metadata('post', $post_id, 'DownloadCount', true);
 if (empty($count)) {
 $count = 1;
 } else {
 $count++;
 }
 update_metadata('post', $post_id, 'DownloadCount', $count);

 $filename = basename($download);
 $download = str_replace(get_site_url(), '', $download);
 $filepath = ABSPATH . $download;

 header('Content-type: application/zip');
 header('Content-Disposition: attachment; filename="' . $filename . '"');
 header('Content-Transfer-Encoding: binary');

 echo file_get_contents($filepath);

 die();
}

function download_count_init() {
 add_action('wp_ajax_download_count', 'download_count_handler');
 add_action('wp_ajax_nopriv_download_count', 'download_count_handler');
}

add_action('plugins_loaded', 'download_count_init');

```