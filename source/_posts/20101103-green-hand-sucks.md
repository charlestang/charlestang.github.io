---
title: 20101103 今天犯了好几个严重低级错误
tags: []
id: '389'
categories:
  - - 工作相关
date: 2010-11-03 10:24:11
---

工作有半年多了，一直顺风顺水，今天一下子接连犯了几个严重的错误。记录下来，时刻惊醒。

1. **执行删除文件操作，一定要备份，应该让备份过程内化到自己的本质中去。**以前在自己的电脑上，想怎么折腾，怎么折腾，文件丢了也没什么大不了，现在到了工作岗位，所有的文件都很重要，其中有些甚至关乎客户，文件数据直接等同于金钱，不能随便删除。这次我犯的错误只是丢失了服务器的log，后果还不是特别严重，估计产品经理会帮我掩盖过去，如果捅到用户那里，不追究就好，追究的话，我就得背一个事故在身上了。

2. **使用*NIX的crontab运行定时任务的时候，一定要使用绝对路径。**这个错误实在是太低级了，我感觉自己就像个白痴。说明对Linux的理解，仍旧是一个小白级别的。正是因为填错了路径，造成我上面干的蠢事，把服务器log丢失了。**以后执行任何自动化脚本，应该尽量使用绝对路径。**这个也要内化到自己的本质中。本来自动化脚本就是写好了不用动的东西，为什么要偷懒少写一点路径呢？？蠢死了，路径用变量存储，已经非常省事了，还要再偷那么一点懒干什么呢？相对路径害死人啊。

3. **不能相信实习生。**以前，作为一名实习生，我要求自己要可靠。我想每个实习生也对自己有所要求。但是，说白了，责任不会让任何实习生承担的。不管他们多么负责，也轮不到他们来承担任何责任。所以，你分发出去的任务，本质上都是你的责任。出了问题也要你负责。别人可以帮你做事，但是不会帮你承担责任。所以，不要相信实习生。其实我对实习生没意见，只是想说，一定要对自己负责。**要把所有从自己身上分出去的事情，都当成是自己的事情。**

**引以为戒，引以为戒！！**