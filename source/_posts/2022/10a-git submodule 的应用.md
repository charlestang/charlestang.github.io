---
title: git submodule 的应用
tags:
  - git
  - submodule
id: '1145'
categories:
  - 工作相关
date: 2022-10-13 10:31:28
permalink: git-submodule-application/
---

大家有没有发现，有些技术点，我们每次想用的时候，都不会用，然后学会了，用一次，又很久不用，然后到了要用的时候，又开始新一轮的循环。比如 git 的 submodule，对我来说就是这样一个技术点。

<!--more-->

## 为什么使用 submodule？

完全一个人不可能写出来大型的软件项目，不得不站到巨人的肩膀上。另一个方面说，虽然，一个人可以开发出所有软件，但是万事万物都从零做起，也是比较笨拙的一种做法，君子善假于物，如果有人发明了很好的工具，那就应该尽量使用，尤其是在一些专业的领域里。

我常用的语言是 PHP，Python，Dart，这三种语言，在编写项目的时候，都有强大的包和依赖管理工具。比如，PHP 里面，可以使用 Composer，在 Python 里面，可以使用 pip，而在 Dart 里，可以用 pub 命令。

语言，或者框架层面提供的依赖管理，可以很好地解决 90% 以上的问题，非要将源代码引入到自己的项目里，而且不是以分发版本的形态，真的不多见，这也解释了我为什么每次用到 submodule 都不会用的原因，因为真的不常用。

我自己现在遇到的一个场景是这样的，我有个项目，叫 [env](https://github.com/charlestang/env.git)，这个项目是我用来在一台服务器上初始化我自己常用的环境的一个项目。如果，是一台 Mac，我会安装 oh-my-zsh，然后，如果是 Linux 服务器，我会安装 `bash-it`（类 `oh-my-zsh` 的 bash 工具），为了配置 vim，还需要安装一个 `vim-plug`，有了这个工具，才能有效管理 vim 的依赖插件。

这三个工具，恰巧都是通过 github 来安装和管理的。env 是一个混合代码的项目，有 shell 脚本，python 脚本，vim 配置等等，而且刚提到的三个工具也不是某一种语言的包，所以，就自然而然用 submodule 来管理了。不知道你有没有那种非要用 submodule 管理的项目场景呢？希望能留言告诉我，让我也学习一下。

## submodule 是什么？

submodule 本质上是一个标准的 git repo，也即一个标准版本库，只是 submodule 允许将一个版本库内嵌到另一个版本库里面。

submodule 可以直接以版本库的管理形式来管理依赖的代码，而不让被管理的代码和主体项目混淆。“主体”项目，是相对于“sub-”来说的。

## submodule 的常见操作

在项目中添加一个 submodule：

```shell
git submodule add https://github.com/robbyrussell/oh-my-zsh.git
```

查看项目存在的 submodule 列表：

```shell
git submodule status
git submodule # status 可以省略
```

首次 clone 一个项目后，里面依赖的 submodule 需要初始化：

```shell
git submodule init
git submodule update # 同步回所有的代码
```

不过，使用 git submodule update 命令，不能更新依赖的版本库。如果想要更新依赖的版本库的版本，可以直接 cd 到那个模块中，刚才说，submodule 实质上是一个标准的 git repo，在那里可以随意使用 git 命令。

当我们对依赖的版本库进行了 pull 操作后，我们在项目根目录执行 submodule status 命令，就会看到对应的模块的 hash 值前面多了一个 +，而且整个项目的状态也变成了 dirty，意思是，当前项目依赖的代码库的版本发生了变化，如果这个变化是接受的，需要进行 commit 操作。

一般来说，我们设置了一个 submodule 后，这个依赖的 submodule 会进入到 `detach` 状态，以防止意外的切换版本，导致出现预期外的问题。

每个 submodule 升级的时候，可以选择在 tag 之间进行切换的方式，cd 到 submodule 目录后，执行：

```shell
git checkout <tag>
```

这样，就会将依赖的 submodule 切换到新的版本。然后，host 项目里，执行 commit，就可以固化这个切换，如果想放弃这个切换，可以在 host 项目里执行 git submodule update 命令即可恢复。