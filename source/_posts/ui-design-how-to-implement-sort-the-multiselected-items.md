---
title: 从一个列表中先选中若干项，再对他们进行排序的交互怎么做？
tags: []
id: '629'
categories:
  - - jQuery
  - - something-about-daily-work
    - 心得体会
date: 2014-06-09 00:22:52
---

这是一个交互案例，很多时候，我们可能就是需要一种交互来完成一个操作，但是我们就是没法想出来很好的解决方案，这种的案例，我遇到不胜枚举，但是每次，我都没有把这种奇葩交互给记录下来，今次，我就想到了要记录下来这个事情，以便今后查倒的时候，可以有据可凭。

## 为什么

不知道多少人，看了我的标题，能理解出来我要做的是个什么交互？其实场景是这样的，我写了一个WordPress的插件，功能是显示博客的文章归档，名字叫 [Better Extended Live Archive](http://wordpress.org/plugins/better-extended-live-archive/)，这个插件目前能提供三个 tab，每个 tab 一种归档的纬度，来展示用户博客的文章列表，比如按照时间纬度，按照分类纬度，按照 tag 的纬度。

![](https://www.evernote.com/shard/s44/sh/5a8993a1-0cdc-4bc2-8052-7e2d44eccde1/b2559deec5cceb48e3df65a4669cfa5b/deep/0/Archives.png)

从上图中，我们可以看到，有三个 tab，分别是 By Category，By Date，By Tag，这三个 tab 的显示与否，是可以在后台配置的，同时，这三个 tab 的显示顺序，也是可以可以配置的。所以本文的问题就来了，怎么样让用户决定显示与否以后，再决定其显示顺序？

## 我想出来的方案

其实，要实现这个根本不难，你肯定会这么说对不？左边一个列表框，右边一个列表框，然后右边代表“待选”，左边代表“选中”，然后加一个上下按钮，来调整顺序，这其实就是用标准的 HTML 组件拼装这个交互的例子了，但是，如果我写插件的时候那么去实现，工作量要大好多，第一个，我要用 PHP 去渲染两个列表框，这就很麻烦了，第二，我要再页面上写一堆 js，来实现左右移动的，上下调序的交互，太累。

而实际上，从本质上，一个列表框，就能包含这两重含义了，第一，multiselect，可以让列表框多选，就可以表达选中这层含义；第二，列表本身是有顺序的，就可以表达顺序，那么为什么一个控件能表达的东西，我却要花那么大力气去实现呢？

所以，第一版的时候，我就真的放了一个列表框在那里，可以多选，选中一项点保存后，就会优先显示被选中的，将没被选中的 tab 接到列表的末尾。提交的时候呢，因为只提交选中的项，所以，被提交的顺序，是列表显示的顺序。只有一个单一列表的时候，这个列表通过这么个简单处理，就可以完成我说的两重任务。先显示选中项，这就表示，通过选中某个并保存，可以调整列表显示顺序。也即，通过若干次选中，并保存后，我可以用一个单选框，模拟出任何我要的选中状态和顺序。

![](https://www.evernote.com/shard/s44/sh/0d7d0e28-2a19-4682-acca-551b9a1543a3/859575d37b0469d781ae451fb1c0b1c8/deep/0/Better-Extended-Live-Archive-Options---Becomin'-Charles---WordPress.png)

## 最终采纳的方案

通过论证和实验后，我真的把这样一个版本给提交发布了。因为我认为它在功能上是完备的，完全可以表达我想要表达的逻辑了，当然了，使用这样的东西，还是需要技巧和逻辑的基础的。充其量，这是一个60分的功能，能用，但是难理解，难用而已。不是坏的。

当然了，如你想见，你不能总是交给一个用户仅仅能用的东西。在第二个版本中，我就改进了这个设计。它需要的不仅仅是完备，而且要好用。就好像图灵机很就牛逼了，那又怎么样，我还是需要iPad。作为读者，如果我不做个动画，估计你们光从文字描述都看不懂我在说什么，不过没关系，你只要知道我最终采用那个方案就行了。

我通过搜索“select and sort”这样的关键词，竟然真的找到了解决方案，而且同样不需要我花多大的力气。主要是有人在 StackOverflow 上[问了这个问题](http://stackoverflow.com/questions/11134417/jquery-ui-sortable-on-select-options)，最佳答案里，竟然也给出了让我[相当满意的答卷](http://jsfiddle.net/QRv6d/)。

是一个叫 jQueryUI Multiselect的插件，很赞！第一，我仍然只需要一个列表框就行了，因为我分析过了，一个列表框显然可以表达两重意思，只是交互不友好而已；第二，交互通过 js 完全补全了，而且是渐进式增强式的，就是说，没有这个 js，或者 js 不起作用，就退化到我原来的方案，其作用了，就变得很好用。Perfect！

![](https://www.evernote.com/shard/s44/sh/455183a5-3ee4-41b6-91a2-3eeb05100022/37993b9b50e0cb257b2a3098cca980ba/deep/0/Edit-fiddle---JSFiddle.png)

## 总结

作者能想出来这个插件，并按照这样的方式去构建，简直让我拍案叫绝。真是英雄所见略同，但是我比他懒！