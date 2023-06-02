---
title: 使用Google AJAX Libraries API替换WordPress自带的js库
tags:
  - advanced topics
  - google
  - usage
  - WordPress
id: '249'
categories:
  - [WordPress, Plugins Develop]
date: 2008-10-18 17:09:53
permalink: replace-the-wp-js-lib-by-googleapi/
---

![google code logo](http://lh6.ggpht.com/_QYicOeu89Bk/SRKlFRbGXUI/AAAAAAAAA2Q/AwVseiUy1sE/s288/googlecode.png)
为了使用方便，WordPress系统内部已经带有了很多的js类库，几乎涵盖了目前市面上流行的所有类库。包括jQuery，prototype，scriptaculous，thickbox等等等等，这些类库用到的重要的插件，也带了不少，到底有多少呢？大家可以去/wp-includes/js目录下查看。

WordPress自带的这些js类库有个弊端，就是基本上都没有经过minify和zip（这两部操作的作用，就是将js代码的体积，尽可能减到最小，以加快下载速度），所以引用WordPress自己的js类库，往往会浪费很多流量（比如，没有zip过的jquery有30KB，prototype有122KB，而压缩过后，jquery只有17KB，prototype只有28KB）。
<!-- more -->
### 我是否使用了类库？

WordPress是一个灵活的系统，用户可以通过插件扩展系统的功能，所以，一个博客上是否使用了某个类库，取决于你博客用到的所有的插件对类库的使用情况。如果你想看看自己到底使用了哪些，你可以用一个简便的办法，就是查看源文件。

```html



```

看上面的代码，是我模板中的一段代码，类似这个样子的就是对类库的引用了。这是我的本地调试系统，使用的是wp2.5.1，引用到了jQuery类库，版本1.2.3。

如果你看到了类似“xxxxxxxxxxxxxwp-includesjsxxxxxxxx?ver=xxxxxx”的字符串，那么，你的博客里，调用了类库。

### 使用Google AJAX Libraries API

什么是Google AJAX Libraries API（GALA）？使用它有什么好处？简单来说，Google是个很牛X的公司，很乐意做好事，它专门优化了这些类库，包括代码精简，压缩，然后用高性能地服务器来Host这些类库，供用到的网站调用，帮助这些网站节省流量。我爱水煮鱼写了个小短文，介绍过这个，大家可以看看（[点这里](http://fairyfish.net/2008/05/29/google-ajax-libraries-api/)）。Google为什么做这种事情？好吧，这个问题，我不知道。

### 怎样用GALA来替换WordPress自带的类库？

关于这一点，首先我想说说WordPress对于引用脚本的一些机制，那就是scripts loader。这是个什么东西呢？一句话：对于博客使用到的所有脚本，进行统一的管理的一个装置。这个装置是怎么管理的呢？首先，所有的脚本登记注册，包括名称，路径，版本号，依赖关系，一一详细记录。然后，是对脚本的调用，通过这套系统来调用。最后，由系统负责把所有需要用到的脚本，无重复的，满足依赖关系的，满足前后顺序的，有条不紊的加入到你的最终的博客页面里面。怎么样？是不是非常酷？**不过呢，总是有“不过”，这种秩序高度依赖模板作者和插件作者的自觉性。**

好吧，我们的方法不得不建立在所有的模板作者和插件作者都自觉使用scripts loader系统的基础上。在这种情况下，一个模板或者插件使用到某个类库，会使用wp_enqueue_script函数来调用需要的类库，使用这个方法，一般不会直接指明类库的路径，只是说明类库的版本号和依赖关系（因为，WP默认就会给所有wp-includes/js目录下的类库进行登记register）。

发现又废了很多话，到这里，我们的替换方法，已经呼之欲出了，因为所有的类库引用都是对已登记的类库的调用（建立在我的假设之上），所以，我如果想要替换，那么只要替换登记在册的那个名单就OK了，完全跳过了去修改每个有可能引用到类库的插件这种繁琐的事情。而且，WordPress确实提供了能够替换那个名单的方法。使用wp_deregister_script可以注销一个脚本，然后使用wp_register_script可以重新注册一个脚本。用这个办法，我们可以把wp自己注册的脚本给注销掉，然后换成GALA的，重新注册，就OK了。

根据WordPress的源代码显示，所有类库的引用，是在最后页面生成的时候才真正进行的，准确一点并且专业一点来说，是在wp_head这个action发生的时候，对类库的引用才通过wp_print_scripts函数写入到页面里面。我们的替换动作只要在此之前完成就OK，所以，我们把替换这件事情，写到functions.php里面，当然，更好的做法，是使用一个单独的插件里。

具体的写法，我曾经在侠姐的文章里见过，大家可以去看看，我就不想进行重复劳动了。[《wordpress里js文件的调用》from 轶侠的网上小窝](http://www.e-xia.com/2008/06/js_call_in_wordpress/)

有没有学习写插件的小朋友写个干这个事情的插件呢？亲爱的读者，如果你写了，请告诉我，我会把你的作品列在下面的。

Updated:

经由侠姐提出，如果直接替换掉WP自带的js类库可能会在后台造成冲突而导致某些功能失灵（比如Simple Tags的标签推荐功能，详情可见讨论），不得不在使用的做出一定的修正。

通过is_admin()标签，可以将前后台区别对待。但是这种情况还不能涵盖所有的例外，如果某个插件正好引用了prototype或者jquery，并且正好利用了WP对齐进行的无冲突修正，那么以上方法可能导致部分功能失灵。有经验的用户可以酌情使用。

Updated2：

经小墨提醒，已经找到了一个这样的插件的实例了。我看了代码，是利用了两个hook，一个是我说过的wp_print_script，这个hook用来探测jQuery和prototype是否同时存在，然后解决冲突问题，另一个是script_loader_src，用来替换里面的src地址，并指向到google提供的js库。不过，我个人觉得，这个方法很可能还是不能完美解决后台的类库冲突问题，但是我没有验证过。

插件主页：

http://blog.clearskys.net/2008/05/28/google-ajax-libraries-api-plugin/