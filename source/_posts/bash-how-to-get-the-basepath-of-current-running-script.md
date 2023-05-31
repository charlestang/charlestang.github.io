---
title: 【HowTo】【Bash】如何取得当前正在执行的脚本的绝对路径？
tags:
  - bash
  - code examples
id: '577'
categories:
  - - 工作相关
date: 2013-07-15 19:37:18
---

如题，一般我们写Shell脚本的时候，都倾向使用绝对路径，这样无论脚本在什么目录执行，都应该起到相同的效果，但是有些时候，我们设计一个软件包中的工具脚本，可能使用相对路径更加灵活一点，因为你不知道用户会在哪个目录执行你的程序，就有了本文的题目。
<!-- more -->
当然，更简单的办法，是给一个配置文件，要使用，必须先配置，告知脚本自己所在的根目录。

此外还有一种方法：

```shell

#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
echo $basepath

```

常见的一种误区，是使用**pwd**命令，该命令的作用是“print name of current/working directory”，这才是此命令的真实含义，当前的工作目录，这里没有任何意思说明，这个目录就是脚本存放的目录。所以，这是不对的。

另一个误人子弟的答案，是**$0**，这个也是不对的，这个$0是Bash环境下的特殊变量，其真实含义是：

> Expands to the name of the shell or shell script. This is set at shell initialization. If bash is invoked with a file of commands, $0 is set to the name of that file. If bash is started with the -c option, then $0 is set to the first argument after the string to be executed, if one is present. Otherwise, it is set to the file name used to invoke bash, as given by argument zero.

这个$0有可能是好几种值，跟调用的方式有关系：

1.  使用一个文件调用bash，那$0的值，是那个文件的名字（没说是绝对路径噢）
2.  使用-c选项启动bash的话，真正执行的命令会从一个字符串中读取，字符串后面如果还有别的参数的话，使用从$0开始的特殊变量引用（跟路径无关了）
3.  除此以外，$0会被设置成调用bash的那个文件的名字（没说是绝对路径）

很靠近了，但是还是不对，最后，我们说一下上面的脚本是什么意思，从里往外看：

1.  dirname $0，取得当前执行的脚本文件的父目录
2.  cd `dirname $0`，进入这个目录（切换当前工作目录）
3.  pwd，显示当前工作目录（cd执行后的）

由此，我们获得了当前正在执行的脚本的存放路径。