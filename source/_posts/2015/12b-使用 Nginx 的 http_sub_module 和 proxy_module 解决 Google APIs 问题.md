---
title: 使用 Nginx 的 http_sub_module 和 proxy_module 解决 Google APIs 问题
tags: []
id: '710'
categories:
  - - WordPress
  - - 技术
    - 前端
permalink: use-http-sub-module-and-proxy-module-cache-static-files/
date: 2015-12-25 12:22:07
---

因为网络原因，可能导致某些静态文件无法被用户直接访问到，我这里提供一种解决方案。
<!-- more -->
我发现，不知因为什么原因，我博客里引用的 Google API 提供的静态类库和字体样式，是没法正确加载的。比如：

```txt
https://fonts.googleapis.com/css?family=Open+Sans%3A300italic%2C400italic%2C600italic%2C300%2C400%2C600&subset=latin%2Clatin-ext
https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js
```

类似这样的网址，很多时候都没法正确加载，这会导致我博客（WordPress 4.4+）的一些功能异常，后台打开非常缓慢。

正好了解到 Nginx 有一个特性叫 string subsitute，也即字符串替换，也就是在内容返回给浏览器之前，做一次无脑的字符串替换。于是，我们可以用到这个特性，
国内某些有点良心的 IT 大厂，都提供了相应的 CDN 镜像，只要无脑将上述访问失败的 URL 的服务器地址，替换成大厂的 CDN 地址就好了。

    

```conf
    sub_filter_types text/xml text/css text/javascript;
    sub_filter 'https:/ /fonts.googleapis.com' 'http://ajax.useso.com';
    sub_filter 'https:/ /ajax.googleapis.com'  'http://fonts.useso.com';
    sub_filter_once off;
```

这样，就可以轻松解决问题了。上面的范例里，用的是数字公司提供的 CDN，真是帮了大忙。

上面要注意，sub_filter 在 Nginx 1.9.4 之前的版本，是不可以写两次的，不知道怎么想的，好在现在最新的都可以写多个了。

基本到这里，已经解决大部分面向中国网页用户的问题了，但是如果你的网站不幸用了 HTTPS，那么就会傻逼了，因为数字公司，并不提供支持 HTTPS 的 CDN 镜像。至少在本文成文的时候，是不支持的。

目前我在网上找到的，唯一支持 HTTPS 的国内镜像，是中科大一群学生搞的一个什么博客系统里面的附加服务，虽然想法很好，但是非常不稳定，时不时就加载不了，靠谱程度还不如我的个人博客。

于是，我想，既然可以让这个请求替换到别的任意服务器，完全可以替换成我自己的服务器，这样，我再用 proxy_module 的特性，来个 proxy_pass 代理一下，不就全解决了嘛，试了下，果然轻松顺利，学了半天的 Nginx 知识，终于有机整合了一下，实现了个小小的功能，消除了自己一个小小的烦恼。

有心人，估计看到我上面念的代码里，双斜杠，中间都加了空格，这就是这个特性带来的另一个小烦恼了，应该解决也不难，不过呢，影响不大，我就懒得多想了。嘿嘿……以后有空再说了。