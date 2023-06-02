---
title: 无法打开 PopClip 控制面板的问题
tags:
  - mac
  - usage
id: '1154'
categories:
  -   - Mac
date: 2022-09-29 11:16:16
permalink: popclip-not-coming-back-after-unchecking-show-in-menu-bar/
---

PopClip 是我非常喜欢也非常依赖的一个软件，属于 “润物细无声” 这个类目的软件。

软件的功能是，当你用鼠标选中一个文本的时候，弹出来一个浮动菜单，提供一系列的快捷小功能。缺省的功能有，搜索引擎，相当于划词搜索，还有字典查询，可以立刻激活系统的字典，还有拼写检查等。

<!--more-->

除了这些基础的功能，还可以识别选中的文本的类型，提供一些特定的功能，比如拼写检查，链接跳转，文本翻译，总之，通过插件，扩展能力近乎是无限的，只要你能想到。

它还有一个小功能，算是一个非功能性需求，就是隐藏 Menu Bar 的图标，软件启动后，会在菜单栏显示一个小图标，可以激活控制面板。不过大家都知道，Mac 的菜单条是非常局促的，尤其是新版的电脑使用了刘海屏，菜单栏的位置更是不够用。隐藏了图标后，就可以节省一个位置。

不过我用了 2021 年生产的 M1 Macbook Pro，默认安装了 Monterey 后，就遇到一个问题，PopClip 的控制面板无法展示出来了。以前，隐藏了 Menu Bar 图标后，在 Applications 目录中，双击 PopClip 应用图标，就会临时在 Menu Bar 展示一次 PopClip 的图标，可以修改配置。现在，竟然怎么都找不到打开控制面板的方法了。软件功能倒是正常，就是无法修改配置。

在网上到处搜索，这个问题的解决，竟然很不好搜，因为这软件本来就是浮动菜单，涉及到现实隐藏的问题，我竟然耗费很长时间才找到了正确的搜索关键字。

> This is something I need to look at because it has happened a few times to people on Monterey and above. What is supposed to happen is that re-launching the app temporarily puts PopClip back in the menu bar. But it seems that isn’t happening for you.
> 
> Here’s what I’d like you to try:
> 
> **1)** Quit PopClip (since you can’t access the controls, you can use Activity Monitor to do that, or type `killall PopClip` in Terminal) and then paste the following command in Terminal:
> 
> `defaults write com.pilotmoon.popclip NMStatusItemHideIcon -bool NO`
> 
> then restart PopClip - it should hopefully come back in the menu bar.
> 
> **2)** Failing that - do you have any menu-bar managers running like Bartender, Vanilla, Hidden Bar? Those can sometimes throw a spanner in the works.
> 
> [PopClip Forum Page](https://forum.popclip.app/t/popclip-not-coming-back-after-unchecking-show-in-menu-bar/338) - From **[nick](https://forum.popclip.app/u/nick)** the PopClip Developer

以上是一位 PopClip 的程序员给出的回应，原来在 Monterey 下，真的有 bug，我还以为我记忆出现问题了呢，怎么都想不起来正确恢复控制面板的方法呢，好在他给出的方法是有效的，通过命令行修改启动参数后，就真的恢复了。

特此记录一下此问题。