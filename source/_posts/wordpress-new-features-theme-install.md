---
title: 【新闻】WordPress新特性预览—主题自动安装（多图）
tags:
  - admin
  - feature
  - news
  - themes
  - WordPress
id: '316'
categories:
  - - WordPress
date: 2009-03-03 00:07:14
---

今天，从SVN源上更新了WordPress，看到添加了70多个文件，更新了近200个文件，不由得非常好奇，到底是变动了什么功能，竟然牵涉到这么多文件。本文带您先睹为快。
<!-- more -->
迫不及待的安装上了，在菜单里面找了一圈，就发现多了两项，（我的判断方法是，没有中文翻译的那项，就认为是新的，不知道准不准），我们先来看最抢眼的一项。

**Add New Themes**

像插件安装功能一样的主题安装功能，哈哈，此前在邮件列表里面也看到过好几次讨论这个的了。这次终于看到实作了，说实话，效果还是相当惊艳的，想到以后找主题不用漫天海找了，真是幸福。好了，我们先来看看这个界面的样子吧。

[![WordPress Install theme](http://lh3.ggpht.com/_QYicOeu89Bk/Sav9a1CMbEI/AAAAAAAABKo/UmqzRNMX0Cw/s400/install-themes-1.png)](http://picasaweb.google.com/lh/photo/fptb_iH9UZSJerckXHRhHQ?feat=embedwebsite "点击看大图")

在这个界面上，我们可以看到，一共提供了五个主要的功能，默认进入的是搜索页面。可以按照“Term”，“作者”，“Tag”来搜索主题，下面的标签云也可以点击，那样就会直接进入“主题超市”随便选择。还有四个选择是**上传**，**特色主题**，**最新主题**，**最近更新主题**。上传界面比较简单，我就不截图了，就是一个文件上传框，可以从本地文件中直接上传主题压缩包到你的主题目录自动解压。另外三个都是直接打开主题选择页面了。

[![WordPress theme picker theme install](http://lh5.ggpht.com/_QYicOeu89Bk/Sav9bHwlToI/AAAAAAAABKw/uKIy8pkZk7o/s400/install-themes-2.png)](http://picasaweb.google.com/lh/photo/VLrCX8-nThAkPG2oyUyHIg?feat=embedwebsite "点击看大图")

主题选择页面的样子如上图所示。跟主题管理页面有点像，每个主题下面有两个链接，一个是预览，另一个就是安装。我在特色主题里面看到了一款主题，相当漂亮，所以，我就预览了一下子，我们一起来看看。

[![WordPress theme preview install feature](http://lh5.ggpht.com/_QYicOeu89Bk/Sav9cBfZtUI/AAAAAAAABK4/TOOz2jijzxA/s400/install-themes-3.png)](http://picasaweb.google.com/lh/photo/1I6Cz2ZNrdtPiwRpQCgXiA?feat=embedwebsite "点击看大图")

可以看出来，这个界面基本上延续了主题管理界面的那个预览功能。只不过这次是从远程服务器直接下载预览页面来看，而非将远程的主题套用到你现在的博客上。这样预览速度倒是极快，就跟打开一个普通网页一样。好，接下去如果想安装，还要先退出预览界面才行，因为安装链接在外面，我觉得这里可能还会改进吧，为什么不像主题管理页面的那个预览一样，直接把下载链接放在预览窗体的右上角呢？现在这个样子有点麻烦，当然，也有可能，萝卜青菜各有所爱吧。

[![theme install panel WordPress theme manage feature](http://lh5.ggpht.com/_QYicOeu89Bk/Sav9cfugkeI/AAAAAAAABLA/KeLNma9rU04/s400/install-themes-4.png)](http://picasaweb.google.com/lh/photo/RoNQxxD3p-akQcWy2W8xMA?feat=embedwebsite "点击看大图")

这个面板倒是十分地简洁，基本上没有什么花哨的东西，有个温馨提醒，主题在您的WP版本上未通过测试。按下安装，这个主题被顺利安装了。看来现在，这个主题从后台直接安装的特性基本上已经开发完毕了，当然样式上还有点乱，这些就是细节问题了，相信不久，大家就能用上这个很酷的功能了。

**Post Tags**

另一个功能，就是出现在“文章”子菜单里的Post Tags功能了，这个功能也是相当的酷，类似于Simple Tags提供的批量标签管理。这个功能我就不截图了，直接描述一下吧。

首先是发布新标签。在这个界面，你可以直接创建一个空标签。而且，现在的**标签都是支持slug功能的，这点已经使得标签和分类没有什么分别了**。

其次是一个标签列表，像是管理分类的分类列表一样。提供了快速修改标签slug和标签名字功能，还有删除单个标签或者批量删除标签功能。

目前，这个功能就者有这些吧，从全面性上看，这个功能只实现了Simple Tags的管理标签功能，还缺乏批量修改文章标签，智能标签的功能。不过我估计这个功能里面带有的api，可以帮助插件开发者开发出更丰富的应用。看来，著名的Simple Tags也要和Thread Comment一样，最终退出历史的舞台了。

好，今天就到这里，祝您晚安！！