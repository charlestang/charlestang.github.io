---
title: 【How To】 使用Git的时候，如何撤销本地更改
tags:
  - git
  - usage
id: '534'
categories:
  - 工作相关
date: 2013-01-27 20:11:33
permalink: how-to-use-git-to-revert-local-changes/
---

在使用Git作为版本控制工具的时候，如何撤销某个文件的本地更改？

为什么要撤销本地更改？

Git规定，在本地变更没有提交的时候，不能够同步其它版本库的更新到对本地，为了防止本地变更丢失，如果本地变更只是一些试验性的调试语句，那就可以完全抛弃（discard），可以使用checkout命令进行撤销。
<!-- more -->
git checkout /path/to/file/to/revert

如果只是急于同步最新的变化，又不想把当前的变更丢弃，同样，也不想把当前的变更给提交的话（真变态），还可以用stash

git stash

这个命令会把你基于最近一个版本的变更给压栈，既不影响你提交代码，更新代码，也没有把代码提交，今后想要，还可以apply回来，非常灵活。