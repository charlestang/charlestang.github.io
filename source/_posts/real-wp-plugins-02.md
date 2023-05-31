---
title: WordPress插件开发实例--(02)
tags:
  - develop
  - plugins
  - WordPress
id: '222'
categories:
  - - wp
    - Plugins Develop
  - - WordPress
date: 2008-08-21 11:16:14
---

插件源于需求。——Charles

我有一个私人博客，目前使用的WordPress的development version，该版本可以提供WordPress的一键升级。各位WPer应该是有福了，不过呢，这个一键升级，却给我带来一点小麻烦。
<!-- more -->
我选用了default主题，而这个主题是WP的一部分，所以，每当一键升级的时候，就会使得我自定义的样式被覆盖>.< ，太糟糕了。两次，粗心大意，我于是乎决定，开发个插件，摆平它！

其实很简单的啦。上次，我们使用了一个filter，还记得不，是the_content。这次，正好，我们就用到了一个action。这个action叫做wp_head，是在模板的header.php加载接近结束时候触发的，具体位置视模板不同而有所不同。但是，有一点是确定的，就是wp_head，会在</head>标签之前被触发。

这个action的作用，就是专门在模板中添加插件需要使用的css或者javascript文件的。正好，我利用这个action，将我自己的自定义css文件给插入到当前使用的模板中。

贴点代码吧 :mrgreen:

```php

';
}
add_action('wp_head','insert_custom_css');

?>

```

很简短吧，真正的代码只有四行噢~~