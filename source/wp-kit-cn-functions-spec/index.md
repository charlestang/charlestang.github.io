---
title: 中文工具箱函数说明
id: '91'
tags: []
categories:
  - - uncategorized
date: 2008-06-08 14:27:32
---

**注意：**如果要在侧边栏调用中文工具箱函数，应该在调用前增加一个语句：  
`global $ct_wp_kit_cn;`  
（这么做是因为侧边栏是在一个函数体内部的，所以，全局变量必须声明。看不懂这个不要紧，调用方式如下面所列，调用之前，前面添加一个如上述的声明语句即可。）

1、**获取最新反馈（评论，pingback，trackback）**

**说明**

*   number为显示最新反馈的数量，默认是5。
*   before为每条记录前面要添加的标签或者字符，默认是"<li>"
*   after为每条记录后面要添加的标签或者字符，默认是"</li>"
*   show_pass_post是否要显示密码保护的文章的反馈，默认是false，不显示，可选值为true，显示
*   sublen每条记录显示的字数，默认为50

**调用规范**

```php

get_recent_responses();
//最复杂的调用方式
$ct_wp_kit_cn->get_recent_responses(10, '', '', false, 30);
?>

```

* * *

2、**获取最新评论（本函数提供Wiget支持，可以直接插入侧边栏）**

**说明**

*   number为显示最新评论的数量，默认是5。
*   before为每条记录前面要添加的标签或者字符，默认是"<li>"
*   after为每条记录后面要添加的标签或者字符，默认是"</li>"
*   show_pass_post是否要显示密码保护的文章的反馈，默认是false，不显示，可选值为true，显示
*   sublen每条记录显示的字数，默认为50

**调用规范**

```php

get_recent_comments();
//最复杂的调用方式
$ct_wp_kit_cn->get_recent_comments(10, '', '', false, 30);
?>

```

* * *

3、**获取最新Ping（pingbacks或者trackbacks或者both）**

**说明**

*   number为显示最新Ping的数量，默认是5。
*   before为每条记录前面要添加的标签或者字符，默认是"<li>"
*   after为每条记录后面要添加的标签或者字符，默认是"</li>"
*   show_pass_post是否要显示密码保护的文章的反馈，默认是false，不显示，可选值为true，显示
*   sublen每条记录显示的字数，默认为50
*   type表示ping的类型，默认是both，还可以是trackback或者pingback

**调用规范**

```php

get_recent_pings();
//最复杂的调用方式
$ct_wp_kit_cn->get_recent_pings(10, '', '', false, 30,'trackback');
?>

```

* * *

4、**留言最多的文章（该函数有对应的Widget版本可以直接插入侧边栏）**

**说明**

*   limit为显示记录的数量，默认是5。
*   days为显示记录的时间段，默认是7天之内，填数字7。填入-1则没有时间限制。
*   before为每条记录前面要添加的标签或者字符，默认是"+"
*   after为每条记录后面要添加的标签或者字符，默认是"<br />"

**调用规范**

```php

get_mostcommented();
//最复杂的调用方式
$ct_wp_kit_cn->get_mostcommented(5, 7, '', '');
?>

```

* * *

5、**最近一个时期内最活跃用户（靠留言数判断）**

**说明**

*   threshhold活跃用户评分起点，默认是5，也即一个用户留言超过5条才会显示他名字，填写-1表示没有限制。
*   days为显示记录的时间段，默认是7天之内，填数字7，注意7天内和本周不是一个概念。
*   master为自己的名字，默认是admin，比如我，就填成Charles

**调用规范**

```php

get_most_active_commentors();
//最复杂的调用方式
$ct_wp_kit_cn->get_most_active_commentors(5, 7, 'Charles');
?>

```

* * *

6、**最近最活跃用户（按照周、月，靠留言数判断）**

**说明**

*   threshhold活跃用户评分起点，默认是-1，也即一个用户留言超过5条才会显示他名字，填写-1表示没有限制。
*   type默认为week，即本周评论最多用户，也可以填month，为本月评论最多用户。本周起始点为周日，本月起始点为1号。可以好好体会一下与上个函数间的差别。
*   master为自己的名字，默认是admin，比如我，就填成Charles

**调用规范**

```php

get_recent_commentors();
//最复杂的调用方式
$ct_wp_kit_cn->get_recent_commentors(-1, 'month', 'Charles');
?>

```

* * *

本文档尚未完成，还在不断完善中。谢谢关注！！