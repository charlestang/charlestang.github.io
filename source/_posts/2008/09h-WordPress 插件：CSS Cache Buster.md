---
title: WordPress 插件：CSS Cache Buster
tags:
  - development
  - my works
  - opinion
  - plugins
  - WordPress
id: '239'
categories:
  -   - WordPress
date: 2008-09-13 16:56:45
permalink: css-cache-buster/
---

众所周知，浏览器一般会缓存CSS文件，以节省下载量和提高页面显示速度，这种机制就叫做缓存。

但是，缓存也有一定的弊端。如果您的CSS文件已经更改，但是浏览器不知道，而缓存下来的CSS文件也没有过期，浏览器仍旧会使用缓存中的CSS文件，也就是旧的样式。

当然，很多有经验的用户都知道，只要使用Ctrl+F5，强制刷新浏览器，就可以让浏览器下载新的样式表文件了，但是作为一个博客网站，你不可能让你的每个用户都去自己Ctrl+F5一下，很傻是不？
<!-- more -->
其实，解决这个问题是很简单的，以前，我就在网上看到过，是为了解决js文件的缓存问题的，js也有相同的问题。要说解决之道，到是非常的简单，因为如果请求css文件，或者js文件的链接变化了，也即url变化了，浏览器就会认为，这是完全不同的两个文件，就不会使用缓存中的文件。所以，只要改变url，就可以让浏览器强制更新缓存了，当然，每次换url也很麻烦，我们一般使用的办法是给url添加一个query string，比如，原来申请的是：

<link rel='stylesheet' href='http://localhost/wp25/wp-content/default/style.css' type='text/css' />

和

<script src='http://localhost/wp25/wp-content/default/custom.js' type='text/javascript'></script>

现在变成：

<link rel='stylesheet' href='http://localhost/wp25/wp-content/default/style.css?120012022' type='text/css' />

和

<script src='http://localhost/wp25/wp-content/default/custom.js?12345678' type='text/javascript'></script>

就是在后面跟了一串数字，我的页面用的一个json，因为每次都要重新下载，所以，我在请求的url链接后面，带了一个随机数，这样，每次浏览器都会认为，这是一个全新的文件，都会去下载。

当然，大多数情况下，是不需要每次都下载，也即在站点没有更改自己的css文件和js文件的时候，浏览器要使用缓存，而更改了后，所有浏览的用户就要自动下载。最好的办法，就是用文件修改的日期来做后面那串数字，既保证了用户那边的效果会实时更新，又保证了能够使用缓存这种机制。

前两天看到个小老外，写了篇文章介绍这个东西，WTC竟然也推荐了，原来这个方法竟然如此的不普及啊~~小老外的文章看这里，讲得和我说得是一回事：

[Smart cache-busting for your Wordpress stylesheet](http://www.alistercameron.com/2008/09/10/smart-cache-busting-for-your-wordpress-stylesheet/)

达人Matt给他提了个建议，让他使用filter来实现这个，这样，每个主题都会因为这个而受益。结果这个小老外就去写了一个插件，叫做[CSS Cache Buster](http://www.alistercameron.com/2008/09/12/wordpress-plugin-css-cache-buster/)（点击链接，查看插件页面，下载插件）。

我本来以为这个小老外这两天迟迟没有动手呢，我就先写了一个，结果发现小老外竟然Updated了，只是我没有看到，赶快把他的插件下回来看了下，发现小老外写的东西用的filter没我好，他不直接，他用了bloginfo_url这个filter，而我直接用了stylesheet_uri这个filter，比他少了一次判断，但是小老外也有优点，就是他考虑了别的插件已经添加过query string的情况，而我没考虑，可见我的经验尚浅，或者说我还是不够勤劳，总之，自我感觉有那么点败给小老外了……

感兴趣或者经常喜欢修改style.css的同学请安装他的插件吧，可以少按很多次Ctrl+F5呢，嘿嘿

下面放上我写的代码，权当是一个纪念吧：