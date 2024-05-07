---
title: Visual Studio Code 小集锦
tags:
  - IDE
  - 工具
  - 开发环境
id: '888'
categories:
  - - 小窍门
  - - 工作相关
permalink: 2020/visual-studio-code-tricks/
date: 2020-03-03 15:57:31
updated: 2024-05-07 21:01:22
---
前两天写了如何给 Python 项目设置 Virtualenv，然后又发现了一个新的小问题，于是，干脆把文章也改了，改成小集锦了，以后各种小问题，都记录到这篇文章里面好了，省得开新的文章了。

## Mac 上如何给 Python 项目设置 Virtualenv

这两天，写了个小小的 Python 代码，基本功能实现了，需要完善一下的时候，突然想起来，VS Code 那么好用，应该也支持 Python 吧，我就不用在命令行用 vim 写那么辛苦了，主要是对中文字符的渲染不好看。

没想到，相当尴尬了，用 VS Code 打开以后，无法识别我在项目文件夹设置的 virtualenv 环境。而 Python 扩展的官方帮助赫然写着是支持的。介绍的设置方法什么的，完全都是扯淡，毫无帮助，还说会什么自动识别之类的，都是不起作用的。想起来了著名的直升机飞行员笑话。

最后，救世主还是 SO（StackOverflow），只有一个[老哥提到了一句](https://stackoverflow.com/questions/54106071/how-to-setup-virtual-environment-for-python-in-vs-code)，在用 VS Code 打开一个文件夹的时候，就创建了一个 Workspace ，然后，你的目录下多了一个隐藏目录 .vscode ，这个目录里有一个 settings.json 文件，这个文件里，设定了一个 Workspace 级别的配置。

如果你使用 ⌘ + ⇧ + P 来设置 Python: Select Interpreter 的时候，是无论如何都没法发现你的项目目录下的 bin 目录的。这就很尴尬了。所以，方法是直接在 Workspace 的 settings.json 中，手动编辑加入使用的解释器路径：

```json
{
    "python.linting.pylintEnabled": true,
    "python.linting.enabled": true,
    "python.pythonPath": "./bin/python3.7"
}
```

然后，重启 VS Code，就可以发现完全兼容了现在这个项目目录下的 virtualenv 环境了。又可以愉快的 Python 了。

我解释一下，我一般是进入一个项目目录，然后执行 virtualenv . ，这个项目目录会变成一个 virtualenv 环境，只会影响这一个项目，不会影响别的项目，这样我可以在每个不同的项目里，使用不同的 Python 环境。这会在项目根目录下多出来一些目录，bin，include，lib 等，加入到 .gitignore 文件就好了。

## 调整左侧目录树的缩进

连续用了几天的 VS Code，发现左侧目录树的展开折叠后，子目录的缩进实在是太小了，目录层级多了，展开以后真的看着很难受，很累眼睛，经常有迷路的感觉。

![](../images/2020/03/visual-studio-tree-screenshot-709x1024.png)

VS Code 左侧目录树的缩进感觉

放狗搜索了一下，在知乎找到了一个答案，原来可以在设置里面，通过设置 Tree:Indent 选项的值来控制缩进。

![](../images/2020/03/vscode-tree-settings-1024x555.png)

在设置里搜索 Tree:Indent 选项 可以找到

在这里，我们看到 VS Code 的缩进控制是用像素做单位的，真是吐血。调整为 24 或者 32 比较好，另外，下面那个选项，说的是，展开一个目录时候，绘制一条垂直线，就像上一张图 alt 目录下面有一条竖线一样，把 onHover 改成 always ，总是显示竖线，这样，目录树就会显得好辨认很多了。

## 如何左边展示目录树，右边展示 Outline

这个是困扰了我很久的问题，因为一直以来，目录树和大纲都缩在左边，好难受。今天终于知道了。

首先调出终端，然后终端可以停靠在右侧，终端所在的容器，可以停靠大纲的面板，把大纲拖去终端的面板就行了。

感觉上，这些面板有两种，一种是可以让别人停靠的，另一种是只能是停靠到某个面板的。想要左边一个 bar，右边一个 bar 的话，你需要两个可以停靠的容器面板。

不过，如果我想左边目录树，右边大纲，下面是 Console ，又怎么操作呢？
