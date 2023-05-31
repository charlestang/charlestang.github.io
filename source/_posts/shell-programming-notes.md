---
title: Shell 编程的备忘录
tags:
  - programming
  - shell
id: '1178'
categories:
  - - 工作相关
date: 2022-11-10 18:32:33
---

作为程序员工作十几年了，Shell 编程这项技能，就好像“你永远得不到的爸爸”一样，每次想用的时候，都觉得自己从来没学会过。本文的编写作为一篇学习笔记，或者一个备忘录，或者一个作弊小抄，我会在每次遇到的时候，不断前来添砖加瓦，说不定有朝一日，能有望凑成一本秘籍。虽然网上类似的内容很多了，但是那些终究是别人的东西，自己用着总是不得劲，所以，做笔记这项技能总是伴随着人类的发展。

### 内建变量

在大牛写好的脚本里，你是不是看到过`$#`，`#@`，等等符号，然后并不认识？关键是，这个系列的变量，长得都差不多，就好像白雪公主的七个小矮人，你总是分不清谁是谁。

这些变量叫做“内建变量”，Built-in Shell Variables，通过内建变量，我们可以方便地引用或者访问一些值。

变量 Variables

用途 Use

`$#`

通过命令行传递给 shell 程序的参数的数量

`$?`

上一个执行的 shell 命令的 exit value，也即返回值

`$0`

当前执行命令的第一个字（word），通常是 shell 程序的名字

`$*`

当前执行命令的所有参数

`$@`

当前执行命令的所有参数，每个参数用引号括起来

`$-`

显示shell使用的当前选项，与set命令功能相同

`$!`

当前 shell 的最后一个后台进程的 PID

`$$`

当前正在执行的进程的 PID

以上说明引用自[这里](http://linuxsig.org/files/bash_scripting.html)，以及[这里](https://superuser.com/questions/247127/what-is-and-in-linux)

## 参考

[Shell Programming](http://linuxsig.org/files/bash_scripting.html)