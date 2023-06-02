---
title: 【Git】 如何批量删除远程的tag
tags:
  - git
  - usage
id: '685'
categories:
  - [小窍门]
  - [工作相关]
date: 2015-06-25 15:44:56
permalink: how-to-bulk-delete-tags-local-and-remote/
---

在我最新任职的团队里，我们采用Git正式作为我们团队开发管理的工具。我们使用Git来做版本控制，研发管理，和线上部署。我们将Git的版本库直接作为代码目录，来存放线上代码，发布的方法，就简化成了，将线上环境的代码目录，checkout 到指定的 tag，简单，快捷。

这个方法执行了一段时间后，发现一个新的烦恼，就是中央版本库的tag数量会变得非常多，多的时候，达到300多个，这其实也没什么了不起，但是我们自己采用gitlab来搭建自己的中央版本库，这个gitlab，还是很多bug的，当tag多了以后，整个网站都呈现出不是特别正常的样子，所以，就需要保持较少的tag列表，让网站保持比较高的性能。然后我就有了一个动机，就是删除远端的tag列表。

我用Google 搜了 how to delete git tags batch，发现老外的说法大概是，bulk delete，哈哈，英语不行啊。

无非就是shell下的一些做法，感觉实际使用上也够了。

首先就是找到远端要删除的tags列表，关键是用对指令。 

    

```shell

    git show-ref --tag

```

这个指令可以列出所有的远端的tag列表，然后就是shell下的一般处理手段了。

    

```shell

    git push origin :

```

如上指令，会致使远程的tag被删除。用管道一连接，万事大吉。

    

```shell

    git show-ref --tag  awk '/(.*)(\s+)(.*)$/ {print ":" $2}'  xargs git push origin

```

上面的指令就是拼接完整的指令了，不过这个指令，会删除远端所有的tag，慎用，如果希望删除符合条件的，应该修改awk指令的正则表达式。

删除完了远端的tag，本地的tag，删法还不是太一样，不过原理相同。

    

```shell

    git tag  grep "v1.1.0.\d$"  xargs git tag -d

```

举个例子，上述命令删除本地所有 v1.1.0.x 的tag，这个指令，会最多删除10个tag。