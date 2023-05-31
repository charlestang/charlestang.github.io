---
title: 在插件管理页面给你的插件添加“设置”链接
tags:
  - code examples
  - development
  - DIY
  - plugins
  - WordPress
id: '383'
categories:
  - - wp
    - Plugins Develop
date: 2010-09-27 21:53:31
---

在插件管理页面，每个插件下面有2-3个Action link，包含了用户可以对该插件进行的几种操作。在插件为禁用状态时，可用的操作有：Activate（启用），Edit（编辑），Delete（删除）；在插件为已经启用的状态下，默认有两个可用的操作：Deactivate（禁用）和Edit（编辑）。如果我们在这个列表里仔细观察，就会发现，有些插件会多出一个Settings（设置）操作。本文记录了，为插件添加Settings link的方法。没有什么过多的描述，直接放代码了。在插件主要文件中（包含了插件信息注释语句的那个文件），使用下面的代码，就可以为这个插件添加一个Settings link了。

    

```php

    function fmp_add_setting_link( $links ) {
        $links[] = 'Settings'; //怎样构造这个link呢？大家可以自己想想
 return $links;
 }
 if(is_admin()){
 add_filter( 'plugin_action_links_' . plugin_basename( __FILE__ ), 'fmp_add_setting_link' );
 }

```