---
title: WordPress到底在整啥？—(05)
tags:
  - code reading
  - WordPress
id: '107'
categories:
  - WordPress
date: 2008-07-02 12:54:05
permalink: inside-wordpress-05/
---

我们已经开始了正式的WordPress之旅，接下去就是在Settings这条主线上，每每看到什么重要的景点，我们都会钻进去看个究竟的。开始吧。
<!-- more -->
首先是个内存大小的定义，WP_MEMORY_LIMIT，关于这个也没啥好说的，就知道这里定了个数字是32M，目前还没看出什么关键的来。

### wp_unregister_GLOBALS()

这是wp-settings.php里面执行的第一个非php内建函数，其实，这个东西涉及到php语言的一个特性，不管了，先看看吧。

#### register_globals

这是php.ini中的一个指令，指定是否将EGPCS(Environment, GET, POST, Cookie, Server) 变量注册为全局变量。在高于4.2.0的php版本中，这个变量已经被默认设定为off了，从PHP6.0开始，这个变量将不推荐使用或者被移除。其实，最主要的问题是，这个选项的开启，会使得php的执行有严重的安全隐患，因为并不是每个程序员都那么严谨地会注意到这个问题。详细的东西，大家可以[参考这里](http://cn2.php.net/register_globals)。

#### wp怎么处理的

如果，这个选项没有被开启，则函数直接返回；如果开启了，也即意味着所有的东西（EGPCS）都会变成全局变量，这个意味着啥呢？简单说，就是当你使用一个global $xxx的时候，你必须确认一次这个xxx到底来自何处，否则后果很可能会很严重。所以，wp在这个选项开启的情况下，率先将所有不该出现在GLOBAL里面的变量，全部给unset掉了。具体做法请参看代码，我也并没有完全看懂，还是对php执行的某些机制不了解，也先存个疑。

### 杂

这里，我实在是没啥名字可以用了。后面做了很多事情。

先是尝试修复WP的运行环境，然后检查了PHP的数据库扩展是否安装。

接着定义了计时开始函数，和计时结束函数，在很多模板的末尾，都有一个执行了多少时间和多少查询的统计，其中那个时间，就是在这里开始的。到了这里，我们来看看这个时间函数的代码。

```php

function timer_start() {
global $timestart;
$mtime = explode(' ', microtime() );
$mtime = $mtime[1] + $mtime[0];
$timestart = $mtime;
return true;
}
//这里在放一个timer_stop的函数头
function timer_stop($display = 0, $precision = 3) {}

```

我主要是想说，其实，我们可以参考这个写法，在写插件的时候，利用这个来给自己的插件计算一个执行时间，也算是一个插件作者测试过程中的严谨作风了吧，毕竟，如果你发现你的插件执行时间非常恐怖，就要考虑改进你的算法或者策略了。编写主题的话，也可以考虑在footer中添加一个timer_stop（你完全可以放在注释里面），这样也能观察一下自己主题的性能。这个函数竟然还可以指定精度，倒是让我挺意外的，不过默认的3位已经相当足够了。

然后是一些常量。

DEBUG，我想，以后，我可能会用到这个吧，主要是调试WP的时候用的。

CACHE，这个常量是可以在wp-config.php里面定义的，如果你自己实现了一个advanced-cache.php的话，你可以把那个文件放到wp-content目录里面。

WPINC，引用目录，指向wp-includes目录。

**LANGDIR**，这个东西蛮好玩的，允许用户指定语言文件的目录，默认是在wp-content/languages或者wp-includes/languages里面。

**PLUGINDIR**，这个目录也可以指定，当然我不知道，更换这个目录到底有什么用。或许以后会发现。

上面加粗的常量，都是可以放到wp-config.php里面去指定的，以后也会沿用这一记法。

========罪恶分割线=========

终于把闲杂说完了，后面，就开始成批成批的引用其他的php文件了，所以，这里就先打住了。