---
title: WordPress到底在整啥？—Special
tags:
  - code reading
  - themes
  - WordPress
id: '224'
categories:
  - WordPress
date: 2008-08-24 11:52:28
permalink: inside-wordpress-special-01/
---

### 模板文件的加载

从plugin_loaded这个action执行之后开始。

在wp-settings.php的最后一段，我们会看到，这里构造了一系列的对象。

首先是WP_Query，然后是WP_Rewrite，然后是WP对象。
<!-- more -->
这个三个对象构造完，是两个常量，TEMPLATEPATH和STYLESHEETPATH。这两个常量是非常有用的，在模板制作的时候，可以直接用来指明自己的模板目录。

之后构造WP_Locale对象。

接着，模板文件就开始涉足了。

首先是functions.php，本质上就是把这个文件里写得代码执行一遍。注意，此时模板文件夹里的其他文件还没有动，这个文件就已经被执行了。

然后，才是WP对象的初始化，然后是init这个action的执行。

再其次，是WP主程序的执行，也即WP对象的main函数被执行。

最后，是template-loader.php登场。该文件会按需加载不同的模板文件。

最后说一下functions.php，这个东西的本质是一个插件文件，只不过是最后一个加载的插件，注意这个文件的加载顺序。这时候，作为一个主题作者，其实是可以做很多事情的，比如，加载本模板所必须的插件，你可以探测用户是否已经安装，如果么有安装，你可以加载自己内嵌的版本。同样，你可以在这个时候卸载掉一些插件，因为插件一般都是用add_action或者add_filter这样的hook的，而且执行functions.php的时候，都已经执行完毕了，这个时候完全可以去探测一下跟模板冲突的插件是否存在，然后给remove掉。

模板里甚至可以带有一些模板作者自己定义的feed，在我看来，wp的feed的rss2版本写得是很一般的，很多人都会通过插件来扩展那个rss2，其实作为一个模板作者，你完全可以自己写一个更好的feed，来取代rss2的原版feed，比如可以添加帖子留言，相关文章，广告到feed当中，甚至你可以在feed里面加上自己的模板的小广告链接。