---
title: Git 文章集锦
tags:
  - git
  - usage
id: '1010'
categories:
  - 工作相关
date: 2021-03-08 19:53:34
permalink: git-summary/
---

从 Git 出来，到我逐渐用上，过去了多年，我搜了一下，这个博客上竟然写了很多关于 Git 的文章，于是我打算做个合集，把关于 Git 的内容汇总一下，便于大家查看。

### 《[签名你的每个 Git Commit](https://sexywp.com/sign-your-every-git-commit.htm)》

Git 有个功能，可以对每次的 commit 进行签名防伪，GitHub 上会为这样的 commit 展示一个 `Verified` 标签，这篇文章介绍了，如何在本地配置 GPG key，并配置 git 来实现给每一个 commit 签名。

### 《[[Git]分支的意义](https://sexywp.com/git-the-meaning-of-branch.htm)》

介绍了我对代码版本控制过程中，分支的理解，也谈及了一些 Git 分支的优势和用法。

### 《[git术语解释staging，index，cache](https://sexywp.com/git-staging-area-index-cache.htm)》

Git 文档和书籍里面多次出现了 staging area 这个属于，而 git 的命令行参数里也有 index 和 cache 的字样，如果不弄清楚这三个概念的意思，就始终觉得模模糊糊的心里不通透，于是我在网上各种搜，找到了这几个概念的缘由，记录在这篇文章里面。

### 《[我为什么更喜欢用 git](https://sexywp.com/why-i-like-git-better.htm)》

这篇文章介绍了我爱 git 的几个理由。在 git 早期的时候，还是有不少人没有切换过来的。现在基本已经全民 git 了。可能这篇文章就不那么有意义了。

### 《[SVN 为什么比 git 更好](https://sexywp.com/why-svn-is-better-than-git.htm)》

在 git 出现早期，各个大公司还没有跟进，还在普遍选用 SVN，而整个程序员群体，也还没能熟练使用 git，而 git 本身也不像现在那么完善，对应的工具链也好，研发管理流程也好，都还不成熟，那个时候，我更推荐小团队或者创业公司选用 SVN，因为有更少的管理成本而人员摩擦，小团队找不到高素质的人，SVN 的多年成熟，市场上的程序员普遍会用。不过，中文互联网圈的人看了我的文章，说我在一本正经地胡说八道。其实你一个人开发，爱用什么用什么，当你组织团队生产的时候，你不得不降低自己的标准，因为不可能所有人都有相同的理解力和执行力啊。

### 《[[Git] 如何批量删除远程的tag](https://sexywp.com/how-to-bulk-delete-tags-local-and-remote.htm)》

遇到这个问题是因为我们的研发流水线使用一个图形化界面的上线系统。这个系统每次需要用下拉列表展示待上线的 tag，我们是用 tag 管理线上版本的。结果因为天长日久积累了太多的 tag，导致这个下拉列表渲染极其缓慢。Gitlab 的 tag 页面也都展示不正常了，不得不去删除一些 tag 来解决问题。

### 《[[Git]代码提交](https://sexywp.com/git-commit-you-code.htm)》

这篇文章用文字描述了 Git 代码提交的过程，以及在 Git 里提交代码时候的一些概念。此外，还对比了 Git 与 SVN 的不同。

### 《[[Git]使用 Git 的第一个任务](https://sexywp.com/the-first-thing-you-use-git.htm)》

使用文字介绍了使用 Git 时候，你将会接触到了第一个命令 clone 的一些用法和解释。并且把 clone 与 SVN 的 checkout 命令进行了比较，分析了两者的异同，帮助读者理解这个 git 特有的概念。

### 《[[Git]Git是什么？Git不是什么？](https://sexywp.com/what-git-is-and-what-it-is-not.htm)》

本文是对版本控制工具 Git 的简介。

### 《[[Howto]在Git中怎么回滚](https://sexywp.com/howto-rollback-changes-in-git.htm)》

本文介绍了在 Git 中，怎么回滚变更。因为在 Git 中，代码所处的状态有很多种，所以，从每种状态中，回滚代码的操作都不一样。更为关键的是，理解每种状态的原理和设置原因，才能用正确的命令去回滚它们。

### 《[[How To] 使用Git的时候，如何撤销本地更改](https://sexywp.com/how-to-use-git-to-revert-local-changes.htm)》

介绍了一个基础操作，怎么撤销本地的更改。

### 《分布式版本控制系统Git入门 》--[（1）](https://sexywp.com/introduce-git-1.htm)[（2）](https://sexywp.com/introduce-git-2.htm)

尝试从 0 开始介绍 Git 版本控制系统的使用，似乎当时想写一本介绍 Git 的书来着，然而，并没有坚持下去，就也放在这里吧。这篇精华帖子看，我还是写了很多内容的，凑齐来也差不多够本小书了。

### 《[我们为什么需要版本控制系统？](https://sexywp.com/why-we-need-vcs.htm)》

直击灵魂的根本性问题，我们到底为什么需要版本控制系统？VCS，被发明出来的根本原因，我们为什么需要保持代码的多个版本？因为长久以来这就是一个毫无疑问要遵守的惯例，以至于我们根本想不起来是什么原因了。这个篇文章为您解惑。