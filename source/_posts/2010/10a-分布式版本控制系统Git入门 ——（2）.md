---
title: 分布式版本控制系统Git入门 ——（2）
tags: []
id: '386'
categories:
  - 日　　记
date: 2010-10-10 17:08:02
permalink: introduce-git-2/
---

上一篇介绍了Git的一些基本信息和安装方法，这一篇来介绍一下Git的基本使用。首先声明，我不是使用这个的专家，哪怕连熟手也说不上，我这里只是记录了我自己在学习使用Git的过程中的一些领悟。大家要抱着怀疑态度和试试看的态度来利用我的文章，千万不要我说啥信啥。

## 回忆我在SVN下的工作流程

我不知道一般人的思路是怎样的，我在了解Git的时候，我最迫切的愿望就是，首先能够让我像使用SVN一样来使用Git。我可以不关心Git的各种优秀特性，如果它不能像SVN一样地工作，那么对我来说，学习它的动力就会大打折扣。

先来看看我在SVN的帮助下，是如何工作的：

首先，我会找一个免费的项目托管服务，通常情况下，是Google Code或者是WordPress Plugins Directory，这是因为我大多数情况下开发的东西都是WordPress插件，而上述两个地方都提供以SVN为平台的项目托管；

创建一个名为my-foo-bar-project的项目，然后，我就已经在服务器上有了这个项目的根目录，一般我会这样设计我的项目根目录，根目录下会有三个子目录，一个叫trunk，一个叫tags，一个叫branches，第一个用来存放我大多数情况下在其上工作的版本，tags经常用来备份我项目的一个稳定并且已经发布的版本，branches通常情况下我并不使用；

事实上，这个时候my-foo-bar-project已经有了其基础的代码框架了，我并非一无所有。这时候，我会首先svn checkout http://svn.wp-plugins.com/my-foo-bar-project/trunk my-foo-bar-project，执行这个命令，我会在磁盘目录上得到一个叫做my-foo-bar-project的目录，并且，这个目录已经被纳入到了svn的管理之下，刚开始学习的时候，我用TortoiseSVN来做这部操作，要做的事情只是找到项目的url，然后在资源管理器里点点鼠标；

接着我会把我以后的项目代码拷贝到这个目录中，然后执行svn add . 命令，将所有的文件都加入到svn的监管之中，然后执行svn commit –m “Init commit.” ，如果我有乌龟SVN的话，我不需要add，只需要直接commit，然后用鼠标勾选新加入的文件，就可以完成任务；

到这里为止，我的项目的主要代码已经纳入到了SVN管理中，我可以放心地不断提交我的工作副本（working copy），因为我知道我可以随时回滚到旧的版本；

当我发布好一个稳定版本之后，我会用svn cp命令或者乌龟SVN的tags/branches命令来备份一个版本；

以上就是我在SVN管理下的全部日常工作了，注意，里面没有提到怎么回滚文件，因为事实上，我真的很少做文件回滚操作，我不喜欢回滚，我提交代码相当谨慎。或许以后，我会研究一下，到底怎么回滚，为了回滚而回滚。

## Git的入门级用法

我花了很多的篇幅来介绍我在SVN下如何工作，就是为了要说明我下面的一些举动以及尝试的指导思想，我只是想要一个更好的，更安全的SVN，然后，我才想要一个Git。