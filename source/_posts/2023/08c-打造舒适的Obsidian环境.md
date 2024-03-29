---
title: 打造舒适的 Obsidian 环境
tags:
  - Obsidian
categories:
  - [工作相关]
date: 2023-08-10 23:20:00
permalink: 2023/config-your-obsidian-comfertable/
---

事情都是环环相扣的，决定了要用网站生成器来管理个人博客，就要使用 Markdown 来撰写内容，发现可以使用 Obsidian 作为 Markdown 编辑器和内容管理器，于是更高频率的使用 Obsidian。

于是需要一个更舒适友好的 Obsidian 环境。

<!--more-->

## 外观

### 深色模式

在没有选定主题的情况下，系统默认是深色模式的，也即 dark mode，也可选择浅色或者跟随系统。

### 主题

这年头即使是一款编辑器，也是支持更换主题的，在配置，外观，主题，管理，点击可以打开类似 Market 那样的列表，可以检索和预览主题，喜欢的话点下载并启用，我安装了一款叫“Things”的主题。

后来又尝试了一款叫“Everforest”的主题，也蛮好看的。

### 字体

一款好看的字体，可以让长时间地阅读和写作都不会疲劳，还能产生赏心悦目的美感。

Obsidian 的字体设置，非常丰富，允许设置“界面字体”，“正文字体”，“代码字体”等。

不过，我系统里只有默认安装的字体，大家可以根据自己喜好去安装。

我正文字体进行了定制，选择了“Hiragino Sans GB”，据说叫“冬青黑体”或者“苹果丽黑”。还能设置多款字体，一旦无法展示前面的，可以自动降级用备用的字体，我选择了“Helvetica”，据说是一款传奇的字体。

#### 字号

字号的话，我觉得还挺重要的，我建议大一点。我现在用 27 寸的 iMac 5K视网膜屏，默认的字体太小了，看着很不舒服的。调整到 18 号，好多了。

## 编辑器

对于一个程序员来说，毫无疑问要选择 Vim 编辑模式啊，因为熟悉。很搞笑的是，需要验证用户是否真的会使用 Vi，否则软件不会直接开启 Vi 模式。

## 插件

这可能是网上能搜到的最多的话题了，也是这款笔记软件能充满魅力的一大原因。

### 核心插件

这个软件是插件体系的，软件安装后自带了很多插件，就是核心插件。

#### 大纲

我觉得这可能是最重要的一款核心插件了。撰写 Markdown 的时候，很自然会用标题层级来组织内容，但是 Obsidian 遵循互联网文本的撰写习惯，一般都是左对齐的，顺着写下来，如果内容很长，就很难辨识标题的层级，没有大纲的指引，就真的很难了。

启用大纲后，最好给两个命令定义快捷键，日常使用好提高效率。我给“大纲：显示大纲标签页”这个命令，定义了一个快捷键，是 ⌘ + ⌥ + O，代表 Outline，注意不要跟全局或者其他快捷键冲突就行。

这个命令会在右侧打开一个带有缩进的大纲视图，轻松帮你在各个标题内容中跳转。

### 三方插件

#### Table of Contents

这是一个目录插件，可以在一篇文章中插入目录。我给命令设定了一个快捷键，是 ⌘ + ⌥ + T，就会在光标位置插入一个带有缩进的目录，会自动链接文章中的标题。在给一些平台撰写 Markdown 文档的时候，非常有用。

在客户端编辑器里，都带有大纲这样的插件，很容易在撰写的时候，掌握文档的结构。考虑到最后输出到网页上的效果，如果没有类似的功能，则需要自己在文章最前面提供一个目录，会比较友好。
#### Quiet Outline

也是一款展示大纲的软件，但是更加地美观和智能，有一个可以脱拽的滑块，来控制大纲的展开层级，用起来很方便。

![Quiet-Qutline-Illustrator](../../images/2023/09/images20230908c-打造舒适的obsidian环境.png)


#### Paste Image Rename

这是一个通用的重命名插件，文章中用到的图片，或者其他媒体，在黏贴进来的时候，弹出一个对话框，重新决定其文件的命名。这一点对于想要管理大量的媒体资源的文章库来说，很有必要，会让你的文件显得更有秩序。

#### File Explorer Note Count

我用 Obsidian 维护自己的博客，博客都转换成了 Markdown 格式，按年归档在一个个文件夹里，当我想知道某年到底写了多少篇博客的时候，我发现缺省的目录树，不显示一个文件夹里有多少个文件。

于是，我搜到了这个插件，还有一个很热门的叫 File Tree Alternative Plugin，更流行，下载人更多，功能也强大得多，不过那个对我来说功能太多了，其设计的初衷跟我的这个小小需求也不符合，还是就用这个简洁的小插件好了。

## 总结

想要一个好的工作环境，要不断去摸索，尝试，积累，本文就是我的一种积累，我以后可以随时根据此文来重建自己喜欢的工作环境。永远是不完美的，等我发现什么新的更好的选择，我会补充到这里。
