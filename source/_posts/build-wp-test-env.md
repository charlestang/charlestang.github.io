---
title: 建立WordPress测试环境
tags:
  - development
  - enviornment
  - guide
  - test
  - WordPress
id: '328'
categories:
  - - WordPress
date: 2009-03-25 14:07:25
---

下载各个版本的WordPress:

wp2.5.1——http://wordpress.org/wordpress-2.5.1.zip
wp2.6.3——http://wordpress.org/wordpress-2.6.3.zip
当前版本——http://wordpress.org/latest.zip

其他版本依此类推。

建立磁盘目录：

www
—phpMyAdmin
—wp25
—wp26
—wp27
—plugins

我就是按照上面的样子建立的。plugins用来统一存放插件。（如果是xampp的话，根目录是htdocs，phpMyAdmin已经安装好了。）

建立测试数据库。三个wp使用同一个数据库。

配置wp-config.php

```php

//wp263和wp271添加如下两行
define('WP_PLUGIN_DIR', dirname(dirname(__FILE__)) . '/plugins');
define('WP_PLUGIN_URL', 'http://localhost/plugins');
//三个版本都要最后两行
define('WP_DEBUG', true);
define('PLUGINDIR', '../plugins');

```

关闭老版本WP的升级提示：

找到wp-includes/update.php

//add_action( 'init', 'wp_version_check' );

像上面那样注释掉上面那行字。

在plugins目录下，安装ozh的no-login插件。

现在这套测试环境，我自己使用下来感觉是WP 2.5的支持很不好。很多插件走不通。主要就是路径的问题。WP2.6和WP2.7的问题不大。但是如果插件需要引用wp_blog_head.php或者wp-config.php，在这样的环境下无法正常运行，我想这其实也是插件开发者的疏漏吧。