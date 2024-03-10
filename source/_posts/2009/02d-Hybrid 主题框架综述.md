---
title: Hybrid 主题框架综述
tags:
  - develop
  - framework
  - hybrid
  - themes
  - WordPress
id: '297'
categories:
  - WordPress
date: 2009-02-15 13:44:55
permalink: introduction-to-hybrid/
---

Hybrid主题框架首次发布于2008年11月，该框架功能完备，定制性强，得到了很多开发者的青睐，以本文为首的系列文章，将向您介绍这款主题框架的方方面面。
<!-- more -->
[Hybrid 是 Justin Tadlock](http://themehybrid.com/archives/2008/11/hybrid-wordpress-theme-framework) 开发的一款主题框架，该框架功能非常强大，下面简单罗列一些。（该列表原文来自原主页，其翻译来自[上善若水](http://edwardright.com/archives/a-new-wordpress-framwork-theme-hybrid.html)。）

> *   如同 SandBox 主题框架一样，用户可以自定义主题样式；
> *   内置了基本的 SEO 选项，基本可以取代 All In One SEO Pack 之类的插件；
> *   拥有一个完备的[主题选项](http://themehybrid.com/blog/wp-content/uploads/2008/11/hybrid-theme-settings.gif)；
> *   内置了常用的13个页面的模板，用户可以利用这些模板来完成许多事；
> *   自 WordPress 2.5 版本至最新的 2.7 版本全兼容；
> *   原生支持至少15个插件；
> *   附件处理功能；
> *   迷人的 [Tab 式位置导航变体](http://www.junchenwu.com/2007/04/the_tabbed_breadcrumb_navigation.html) 菜单；
> *   基于 [960 GS](http://960.gs/)、[Blueprint](http://www.blueprintcss.org/) 和 [Tripoli](http://devkick.com/lab/tripoli) 相当可靠的 CSS 样式；
> *   可以建立各种样式的站点；

Hybrid 是一款名副其实的“框架”。其整体架构，就是一个良构的XHTML布局，具体来说，就是一个页头，一个页面内容容器，里面分为主要内容，侧栏等；然后是页脚。除了一个最基础的DIV+CSS的XHTML布局之外，剩下的就是Hook，在上述基础布局中，所有可以插入元素，或者有必要插入元素的地方，都带有WordPress的Action。

当然，Hybrid除了是一个框架之外，它还是一个主题。Hybrid主题本身，就建立在其自身搭建的框架之上。为什么这么说呢？因为一个博客模板里，所有最为基本的东西，如<head>标签内部的一些meta tags，博客标题，站点描述，页面导航，侧边栏，页脚版权信息，等等等等，绝大多数主要内容，也即除了“骨骼”之外的那些“肉”，都是通过action来挂载的。既然是挂载上去的，当然也可以摘除。

Hybrid框架最适合作为开发子主题的基础，因为该框架本身布局灵活，通过框架内部带有的action，子主题作者可以从原本基础上摘除任何不需要的功能块，同样也可以挂载任何自己开发的功能块。这一系列的操作，都不需要对Hybrid本身动手术，这保证了Hybrid框架的完整性，为日后升级提供了极大的方便。

上手Hybrid，一定要有框架思维，把它当成一个真正的框架，才是正确的用法。（写给程序员：你在编程时有想过修改.net framework或者MFC或者JFC或者STL的代码吗？答案如果是没有，那么你也不需要去修改Hybrid的代码。）我这里这么说，主要是想告诉一些希望定制Hybrid框架的朋友，直接DIY Hybrid的源代码，是不被禁止的，但是Charles个人及其不推荐的。Hybrid虽然是一款非常优秀的主题框架，但是其目前版本只有0.4.1，其内部代码还有至少3处被标记成under active development，整个框架还处在活跃地开发状态，保持随时升级非常重要。

未完待续

下一篇，拟介绍《[使用Hybrid的起点](http://blog.charlestang.org/use-hybrid-to-build-child-theme.htm)》，欢迎给位在下面跟帖讨论，并给我提供写作建议，谢谢！