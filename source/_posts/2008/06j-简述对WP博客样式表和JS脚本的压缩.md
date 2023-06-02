---
title: 简述对WP博客样式表和JS脚本的压缩
tags:
  - DIY
  - optimize
  - WordPress
id: '96'
categories:
  -   - WordPress
date: 2008-06-18 13:40:15
permalink: simple-guide-to-css-js-compress/
---

应朋友的要求，才决定要写这个文章，我想，我对这个问题的理解是比较肤浅的，恐怕也讲不清楚，所以，我只简述一下步骤，高手就直接跳过吧。

先从文件在网络上传输说起，浏览一个网页，一般就是浏览器从服务器上下载文件的一个过程。举个例子，如果浏览我的网页，你要下载这么几个文件：

*   由index.php输出的一个HTML文件，也就是主页上的文字、链接还有他们的逻辑结构
*   style.css样式表文件，决定了页面的外观
*   jquery.js和vg.js脚本文件，决定了主页上的一些小功能，表单验证啦，ajax之类的
*   其他若干文件如logo.png，日志中引用的图片，或者留言中的头像，等等

浏览一个网页要下载这许多文件，如果每个文件又都很大的话，得到的结果只有一个，就是网页展现时间相对来说要长。如果能对传输的文件进行压缩，就能缩小文件的体积，加快浏览器的下载速度，减少服务器的流量。
<!-- more -->
还好，浏览器本身就是支持压缩格式的，比如gzip，现在问题的关键就是怎么让服务器把输出的文件压缩。我在网上搜了一下，一般最好的做法是使用服务器来压缩，Apache带有一个模块，叫做deflate，就专门干这个，如果你的服务器支持这个功能，那么你就很幸运，直接开启这个，然后配置一下就可以了。当然，我没有，所以，我也搞不清楚怎么配置啦。

服务器本身不支持，我们还有别的办法，那就是使用PHP来压缩了，PHP是支持gzip的。当然，又是一样，我讲不清楚怎么写那些代码，也搞不懂，但是这不代表我就不能用。

一个个说，压缩HTML文件，我用的是一个插件，就是WP Super Cache，这个插件自己就可以对Cache下来的文件进行压缩，只要在控制面板里面打个钩就行了。（WP 2.3 以前的，WP本身就有压缩功能）

刚才只说了压缩HTML，剩下的东西怎么办呢？本来我也是没有办法的，是看到了伟大的K2的代码，才知道，原来还可以这样。起作用的是这么段代码，这段代码在js文件夹的gzip-header-js.php和css文件夹的gzip-header-css.php中都有，内容几乎是一样的，其作用就是对这个文件进行压缩，并且要求浏览器缓存这个文件，缓存时间是两个月。

```php

=') and ob_get_length() == false) or ob_get_length() === false) ) {
ob_start('ob_gzhandler');
}

// The headers below tell the browser to cache the file and also tell the browser it is JavaScript.
header("Cache-Control: public");
header("Pragma: cache");

$offset = 5184000; // 60 * 60 * 24 * 60
$ExpStr = "Expires: ".gmdate("D, d M Y H:i:s", time() + $offset)." GMT";
$LmStr = "Last-Modified: ".gmdate("D, d M Y H:i:s", filemtime($_SERVER['SCRIPT_FILENAME']))." GMT";

header($ExpStr);
header($LmStr);
//注意！！！！！：以下两个header是二选一的，千万不能全放上去啊！！！！！
//此段代码专用于js代码的压缩，看下面这句Content-Type就知道了。
header('Content-Type: text/javascript; charset: UTF-8');
//如果是CSS文件，替换成下面这句
header('Content-Type: text/css; charset: UTF-8');
?>

```

大家要做的也是很简单的，把上面这段代码，插入到你的js文件，或者CSS文件中，然后将他们的扩展名加一个.php就可以了。注意看我写的注释啊，不看清楚就照抄，你肯定搞不定。

现在来举个例子，比如我的页面使用了jQuery类库，那么我原本要这样写：

```html



```

然后，我把上面的代码拷贝到jquery.js文件的最前面，然后重命名成jquery.js.php，引用时候写法也变成下面的样子了：

```html



```

jQuery的那个文件原来的尺寸为55KB，经过这样的处理，浏览器实际下载量是17KB，只有原来的三分之一。

但是对样式表的压缩，并非那么一帆风顺，因为主样式表文件是不能重命名的，必须叫style.css，这是WP机制决定的的，如果你换了名字，模板根本不会出现在模板列表里面。

处理这个问题的方法我知道两个：

1，把style.css里面的内容，拷贝到另一个css中，比如，myzipstyle.css中，然后使用上面我说的方法，最后在header.php中加上对myzipstyle.css.php的引用，就可以了。而style.css里面就只有7行注释，你可以把对它的引用从header.php中去掉。但是这个style.css，及其文件内前面那些注释，都是必须的，不能删掉（虽然你可以不用）。

2，像伟大的K2那样，在style.css里面引用另一个css文件，写法如下：

```css

//K2的style.css，除了注释，就只有下面一行。相信聪明的你已经看懂了，我就不再费唇舌了。
@import url('css/core.css.php');

```

乱七八糟，洋洋洒洒一大堆，希望能对你有所帮助吧~~

当然，还有更高级的方法，也更厉害，但是我是没有搞清楚的，我提提名字，如果你有志于再深入一步的话，可以有个出发点。再后面的方法就是，自己编译一个专门用于压缩的CGI程序（也可以用别人编译好的），然后放到服务器的cgi-bin文件夹里面，然后，手动修改.htaccess，让浏览器访问的每个文件，都从“压缩机”里面过一遍。你可以去：阅微堂（[http://zhiqiang.org/blog/posts/speedup-your-blog.html](http://zhiqiang.org/blog/posts/speedup-your-blog.html)），主人对博客优化有着深入而系统的研究。