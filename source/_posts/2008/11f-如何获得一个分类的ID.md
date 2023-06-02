---
title: 如何获得一个分类的ID
tags:
  - advanced topics
  - development
  - DIY
  - WordPress
id: '254'
categories:
  - WordPress
date: 2008-11-02 00:18:15
permalink: how-to-get-a-cat-id/
---

摘要：本文主要讲述了，在Archive页面里，在侧边栏进行函数调用时候（也即在the loop外部），如何取得category的ID的方法，以及发现这个方法的过程，希望对大家有帮助。
<!-- more -->
今天，我在改进我模板的Archive页面，我希望能在Archive的侧边栏能够根据情景做出一些细微的变动。我希望当一个用户浏览我某个分类的Archive的时候，侧栏能够显示这个分类下展示最多的文章。

正好，我的博客上安装了WP Post Views Plus插件，这个插件就具有这个功能，只需要调用该插件提供的一个模板标签，get_most_viewed_category()即可。但是这个标签需要一个比较特别的参数，就是目标category的id，即一篇文章的cat_id字段。搜索了一下Codex，没有发现有哪个function或者template tag可以提供我需要的这个功能。只好自己找了。

首先，这个功能只有在Archive页面显示分类的Archive时候才能出现，平时不应该出现，这个很简单，可以用is_category()这个tag来判断，但是怎么能够知道现在展示的这个category的id呢，我第一个想到的就是去is_category里面看，先看看wp怎么判断is_category或许能够找到思路，进去一看，答案就揭晓了。

```php

is_category )
return false;

if ( empty($category) )
return true;

$cat_obj = $wp_query->get_queried_object(); //看这里

$category = (array) $category;

if ( in_array( $cat_obj->term_id, $category ) ) //还有这里
return true;
elseif ( in_array( $cat_obj->name, $category ) )
return true;
elseif ( in_array( $cat_obj->slug, $category ) )
return true;

return false;
}
?>

```

上面代码中的term_id就是cat_id了。到了这里，得到我们要的变量已经很容易了。

```php

get_queried_object();
$cat_id = $cat_obj->term_id;
?>

```

ok，这样，我们就拿到了我们要的东西了！万事大吉了~~

不过呢，我们继续去看看get_queried_object()函数的源代码，我们发现其实wp_query这个对象把它查询的某些内容抽象成一个query_object来对待，其实几乎那一系列的conditional_tag都有对应的query_object。更进一步，我们在这个函数里发现了，对于每一个query_object来说，都存在一个query_object_id。对于一个category来说，我们要的query_object_id就是我们要的category id。再往下一点，我们就看到了得到cat_id最简单的方法了。

```php

get_queried_object_id();
?>

```

哈~