---
title: 修改Firebug的工具栏按钮调用方式
tags:
  - advanced topics
  - DIY
  - firebug
  - Firefox
id: '269'
categories:
  -   - Firefox
date: 2008-12-02 14:22:30
permalink: modify-the-firebug-call-way/
---

昨天晚上，我[写了篇文章，说我在玩Firefox美化](http://sexywp.com/some-problems-when-custom-firefox.htm)，其实，我主要在做的工作，就是清理Firefox浏览器界面上不需要的东西，尽量的压缩界面，扩大网页的可视化面积。

昨天，为了隐藏掉Firefox的状态栏，我已经进行了相当多的努力，要隐藏掉状态来，还要保存状态栏的所有功能，着实不是那么简单的一件事情，老肥的文章只介绍了怎么把显示Active Link的功能搬移到地址栏里显示（使用Fission），还有把Gmail Manager整合到工具栏按钮。而我昨天提出的第三个问题，即firebug按钮，整合到工具栏后，调用方式变成“在新窗口中打开”，我今天终于给搞定了。
<!-- more -->
**以下一段思路分析，可以跳过。**

Firebug内部带的工具栏按钮，是一个双重状态按钮，即开关（toggle），按一下开，再按一下关。其上绑定的动作，就是在新窗口中打开，而不是我们熟悉并且喜爱的在同一窗口的底栏打开。修改的思路就是：

1. 找到这个按钮；

2. 找到在底栏嵌入firebug这个命令；

3. 将在底栏嵌入firebug的命令绑定到按钮上；

确立这个思路，完全是一种直觉，建立在对程序运行原理的理解上的，没错，就是函数调用，一般来说，一个按钮按下去，会调用一个函数，这个函数的运行决定了程序的响应方式，既然firebug有两种出现方式，那么可以简单的猜测，是两个不同的函数，一个从底栏嵌入，一个在新窗口中弹出。

好了，思路定了，就开始执行，那么怎么找？那可是相当难了，因为我完全没有接触过Firefox插件开发，对Firefox底层构架不了解，对于插件的结构更是不了解，于是乎，唯一的办法，瞎找。简单看一下插件目录下的代码，就知道，Firefox插件基本上由js代码，css代码，xml代码组成，除此之外，都是些图片。都是纯文本，打开查看没有什么障碍的。

最大的障碍是什么，就是不知道名字，其实昨天也有提到这个，就是改userChrome.css可以自定义外观，但是改哪个id的属性，改哪个class的属性呢？你不知道工具栏上第4个按钮的id或者class到底是什么，你更不知道按钮旁边的那个小箭头叫什么，凭什么叫dropmarker而不叫droparrow。就好像在茫茫人海中找一个只知道特征，不知道姓名的人一样。你只能傻看，不能调动公安局的数据库帮忙。我终于还是没能找到，毕竟傻找不是办法。

结局，办法总是有的，没有直接的，有迂回的。我想起来，firebug在工具菜单下有个子菜单的，哪个菜单里有两种调用firebug的方式，编过一点Win应用的可能都知道的，菜单的工作方式和按钮是完全一样的。那么找不到按钮，找菜单也可以，找到菜单，可以找到菜单调用的函数名，然后再用函数名去反过来定位按钮，也行。菜单项很多，而且一般会写在一个文件里，目标比较大，应该好找。哈哈，结果，还是不好找……囧。

灵机一动，菜单项里有汉字，汉字是字符串，靠，这下终于跟某个名字挂钩了，可以搜了！！直接打开locale文件夹，找到简体中文的配置文件，搜索菜单项，找到：

原来那个方法叫做DetachFirebug，ok，在整个目录下搜索DetachFirebug，一共没多少，一个个判断，终于找到：

    
 
 
 

**最后，修改方法（刚才跳过的童鞋从这里接）：**

找到:

```xml

%appdata%\Mozilla\Firefox\Profiles\xxxxxxx.default\extensions\firebug@software.joehewitt.com\content\firebug\browserOverlay.xul

```

文件，把上面那段代码找到，然后把cmd_toggleDetachFirebug改成cmd_toggleFirebug，把firebug.DetachFirebug改成firebug.Firebug，保存，然后重启Firefox，按一下工具栏上的firebug按钮，怎么样？是不是变成和状态栏按钮里一样的效果了？

Enjoy it！