---
title: 创建自己的filter
tags:
  - advanced topics
  - apis
  - hooks
  - WordPress
id: '232'
categories:
  -   - WordPress
date: 2008-09-03 23:31:31
permalink: create-your-own-filter/
---

我用这篇文章来简单介绍一下如何创建一个filter。
<!-- more -->
用简单的话来说，就是调用`apply_filters`函数。

然后，我们来复杂点说：

如果你调用了`apply_filters('my_own_message', $mess);`，那么，你就创建了一个名字为my_own_message的filter了。

那么这个my_own_message的含义是什么呢？按照我个人的理解来说，就是将来有一群接受一个参数$mess的函数，可以被调用。而且，就恰恰会在你调用apply_filters的地方被调用。

再举个不恰当的例子，就好像你是一个小朋友，你从你大款同学那里借了一个变形金刚，爱不释手，但是终于玩够了，要还了，又觉得还是不爽，这时候，你喊了一嗓子，“要玩变形金刚的排队过来玩，玩完还给那款爷”，小朋友们兴高采烈，但是秩序井然地过来玩了，当然，你们这么一坨人玩过了，那个玩意儿能完好无损的可能性也很小了，不是少了条胳臂缺了条腿，就是脸上多了两撇小胡子……最后，那可怜的变形金刚面目全非的回到了大款小朋友的手上……

你喊那一嗓子，就好像是apply_filters了，然后那些小朋友就是名字为“要玩变形金刚”这个filter上的函数，那个变形金刚就是那个传递给函数的参数，缺胳臂少腿，多了小胡子，就是这些filter们作用在变形金刚这个参数上的效果，最重要的是，这个变形金刚最终还给了那个大款小朋友，也即filter们必须要把拿来的东西返回去。

哈哈……又胡扯了一番……

举个例子：

下面是某主题的footer.php

```php



WordPress : xhtml : 
Entries (RSS)
and Comments (RSS).





```

然后，这是某主题的functions.php节选

好，我创建了一个filter了。

最后，思考题：

1. filter到底有什么用？

2. 对一个插件作者来说，filter意味着什么？

3. 对于一个主题作者来说，filter又意味着什么？