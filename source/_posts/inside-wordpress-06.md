---
title: WordPress到底在整啥？—(06)
tags:
  - code reading
  - WordPress
id: '109'
categories:
  - - WordPress
date: 2008-07-07 14:59:30
---

上回把前面一对闲杂都说了一遍，今天开始一个个看吧^^

### compat.php

具我猜测，compat这个词是compatibility的意思，没错，就是兼容。
<!-- more -->
做了点啥呢？主要是把新版本有的，而老版本没有的函数，都给实现了一遍。从源代码里面可以看出，WordPress最多兼容到>PHP4.3.0。这是前面看过的代码里面的，我希望我没记错。

这里补充的函数倒也不多，我就罗列一下好了：

*   http_build_query()
*   _()
*   stripos()
*   hash_hmac()
*   mb_strcut()

新版本的php手册里面，对这些函数都有解释的，我不想赘述了。我对这里的那第二个函数是非常好奇的，到底是干什么的？接受一个字符串参数，返回那个字符串，那就直接写一个字符串不就得了？我终究还是有点天真的，如果谁知道那个是干什么的，请告诉我，真是太奇怪了，搜索了全部源代码，好像只有class-pop3.php里面用到了。

另一个想唠两句的是最后一个函数，mb_strcut()，按理说，就是 multibyte string cut，也即多字节文字字符串剪切函数，不过从这个函数来看，只对utf8编码的字符串奏效，所以，wp推荐每个博客尽可能使用utf8编码。这个时候，我就想起了著名的中文工具箱，里面用了个utf8_trim，其实是否有可能用这个函数代替呢？还有就是yskin的CJK-excerpt，里面用了一个mb_strlen，是不是也可以用这个函数来代替？我只是一说，希望真正的高手看到这里，能给我指点一二吧。（我个人的感受是，utf8_trim的效果还不是很干净啊，最后还会有一个乱码，有时候是个小方块。也可能我没用对。）

本来今天想在往下写点的，但是我一看，后面两个都是重量级的，马上打了退堂鼓了。一个是WP的百宝箱，functions.php，另一个就是WP这个类的定义了，那个里面有WP这个程序的main函数哦~~~这个算是对后面内容的简短预报了吧，嘿嘿^^