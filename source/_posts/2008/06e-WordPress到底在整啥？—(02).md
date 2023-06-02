---
title: WordPress到底在整啥？—(02)
tags:
  - code reading
  - WordPress
id: '102'
categories:
  - WordPress
date: 2008-06-27 16:22:31
permalink: inside-wordpress-02/
---

上一篇文章主要来说，是个序言，所以，讲个路标就拉倒了。这回我们来看看真正的入门是个啥。

### wp-blog-header.php

哇，这个文件代码就多了，算上空行，有二十多行了，比上一个多了一个数量级。所以，你大概猜到了，我懒得帖代码了。那没有意思，真的。当然，我还是可能会帖个局部啥的，不会全部帖。
<!-- more -->
先看看这个文件干了啥，整个代码被一个if给套牢了，也即，这个文件的执行是有条件的。啥条件啊，wp_did_header 不存在，就是说，wp的入门这个动作，没发生过，这里的代码才会执行。如果，这里的代码执行过一次，那么wp的入门动作就发生了，这个header也did了，那么这个时候，我再来访问index.php会怎么样？Ok，你已经知道了，网页还是会出现的>.<。为啥？每一次访问一个页面，都是重头开始，一遭是一遭。这次访问，和上次访问是断开的，你可以简单理解成执行php代码的那个家伙完全不记得你真的did过那个header。

就是啥意思呢？每一次，你访问wp博客中的某一个页面，这个wp都兢兢业业地从头到尾地跑了一遍。至少来说，我是这么理解的。

然后，我们来看看，这个条件执行的内部，在干啥。首先，检查一个文件的存在性，谁呢，wp-config.php。这个文件，我们安装过WP的，都知道，这个是配置文件。如果配置文件不存在，会咋样？

#### 结局

结局是确定的。wp_die()，看到没？死了。没有config，人家就死了。当然了，死前，有些遗言的，也就是说，我的死因是没有config，关于如何设置config，参考blabla，如果你硬是懒得设置，那么可以自动生成blabla……

#### 迷局

终究还是有点奇怪的东西：

```php

//疑点1，为啥这个path上还有些花头？难道，有别的入口？
if (strpos($_SERVER['PHP_SELF'], 'wp-admin') !== false) $path = '';
else $path = 'wp-admin/';
//疑点2，都要die了，还弄这么一陀干啥？
require_once( dirname(__FILE__) . '/wp-includes/classes.php');
require_once( dirname(__FILE__) . '/wp-includes/functions.php');
require_once( dirname(__FILE__) . '/wp-includes/plugin.php');

```

疑点2，我倒是看出些端倪来的，就是这个WP驾崩的时候，用的是wp_die()，这个可以说是个WP独特的死法，关于此死法的描述，应该在functions.php里面，所以，要这个。而这个functions.php想要给WP一个安乐，就不得不了解WP的身体构造，所以，要看classes.php，但是这个plugin.php的问题还是解决不了案，奇怪了，可见我的猜测方向不一定对，先往后看吧，以后就会水落石出了，我相信，真相只有一个！

### 侥幸没死

如果说，wp-config.php是存在的，那么故事就比较多了，所以呢，我先写个故事梗概在这里，后面发生了四件事情。

1. header确实被did了，这个够简单，一句话，以后就不表了；

2. 装载wp-config.php，这真的只是一个配置？恐怕不止吧，预知后事如何……别拿番茄砸我啊，靠……

3. wp(); 然后wp了，按照一般的故事篇章理解，这个是故事的高潮部分。

4. 伟大的模板，让无数人换了看，看了换的模板，要出场了，template-loader.php，嗯，模板加载器，这个看来就是故事的结局了：小WP，从此穿上了衣服……

嘿嘿嘿，今天先到这里。