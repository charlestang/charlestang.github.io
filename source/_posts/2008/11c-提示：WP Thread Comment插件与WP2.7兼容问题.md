---
title: 提示：WP Thread Comment插件与WP2.7兼容问题
tags:
  - advice
  - DIY
  - notice
  - plugins
  - usage
  - WordPress
id: '266'
categories:
  -   - WordPress
date: 2008-11-21 11:32:22
permalink: let-wptc-compatible-with-wp27/
---

Updated:目前该插件的功能已经修复了~~

今天凌晨，Leo提出了给霍霍更换WP2.7，操作完成后，发现WP Thread Comment插件的**后台直接评论回复功能失效**。

这里特别提醒想要升级到WP2.7并且同时在使用WP Thread Comment插件的朋友，目前的WP Thread Comment插件版本的**后台评论回复功能**无法正常使用。
<!-- more -->
除此功能之外，该插件的其他功能尚未发现问题。如果平时就不用后台评论功能的朋友，可以放心。

**原因分析**

该插件在后台admin_footer部分，插入了一个表单，该表单内部有两个隐藏域，comment_post_ID和comment_reply_ID，还有文本框，其id为comment。大家更新到WP2.7后就会发现，实际上WP2.7在评论系统改进很大，本身就内置了后台评论功能，而这样的功能其实现原理都雷同，恰巧，WP2.7自身也在后台隐藏了一个表单，这个表单里也有两个隐藏域和一个文本框，又恰巧id也是上文提到的那3个。而且这个表单所在的位置比WTC插件插入的表单位置靠前。所以，WTC插入的js代码每次都读到WP2.7自己插入的表单域，这就导致了这个功能的紊乱。

**解决方法**

手动修改WP Thread Comment插件，将其插入到后台admin_footer部分的表单的隐藏域的id重新命名，如改成wptc_comment_post_ID，将textarea的id重新命名为wptc_comment。

然后将对应的**后台评论提交部分代码**（其他部分代码，如前台嵌套回复部分的代码不能改）里调用到这两个id的地方改名。

**使用建议**

没有足够的把握，请不要DIY。

禁用WP Thread Comment插件的后台回复功能，等待其原作者更新插件。

**后记**

原本以为WP2.7改进评论部分后，将会带来完美的体验，但是实际上，无论是其提供的嵌套评论功能，还是评论分页功能，都不是那么好用的，操作复杂，代码繁杂，定制性有限，极大地增加了主题开发者的负担。

作为用户来说，我本人也不是很想用WP2.7提供的评论系统的。不过，总体来说，我对WP还是有信心的，它的tag功能一开始也是相当地烂，后来也渐渐改好了。我想评论部分也会如此的。