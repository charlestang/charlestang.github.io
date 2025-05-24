---
title: WordPress插件：选项查看器
tags:
  - plugins
  - WordPress
id: '335'
categories:
  - - 历史归档
permalink: plugin-options-inspector/
date: 2009-04-08 16:20:47
updated: 2025-05-10 14:03:53
---

Options Inspector is a tool with which you can list all the options in your database, view a certain one in detail, even its data is serialized, and alter exactly a certain part of option value. It is mainly designed for plugin developers and theme designers.
<!-- more -->
When I am debugging a plugin, I always want to konw, whether the options in this plugin are saved exactly or not. Usually, I add var_dump statement in my source code to print the options out. Everything looks good, but when I finished my job, it bothered me a lot to remove this debug statements. What annoyed me even more is that when I change my mind and changed the structure of the option, I must use additional statement to alter the option or directly use SQL in phpMyAdmin. Finally, I created this tool to assist the plugin development.

**Features**:

*   List all options order by option_id.
*   Search option through keyword.
*   View unsierialized value of options.
*   Modify option use PHP code.

**Demo**: (Click to see the full size.)

[![](http://lh5.ggpht.com/_QYicOeu89Bk/SdxZnJK0e8I/AAAAAAAABTc/QNlqGHvAGGs/s400/Options-Inspector-Screenshot.png)](http://picasaweb.google.com/lh/photo/YrsYFnG7FbRWZUArgNwFOw?feat=embedwebsite)

**Download**: [Options Inspector v1.0.1](http://wordpress-tools-box.googlecode.com/files/options-inspector_v1.0.1.zip)

选项查看器是一款开发辅助工具，用于显示，修改和删除选项。免去了使用打印语句和使用phpMyAdmin的调试后台选项的麻烦。愿大家能够更轻松地开发WordPress插件和主题。

一般，不建议您在您的主力博客上尝试该插件的修改和删除功能。

 
 
 
 ![](https://www.paypal.com/zh_XC/i/scr/pixel.gif)