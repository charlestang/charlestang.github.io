---
title: 【Git】使用Git的第一个任务
tags:
  - git
  - usage
id: '673'
categories:
  - - 工作相关
  - - something-about-daily-work
    - 心得体会
date: 2015-04-14 22:52:37
---

说实在的，Git我已经学习了很久很久，从最开始的，零星的学习，然后偶尔使用，到现在成为公司的唯一版本控制方式，断断续续没有两年，也有三年。Git官网上写着，简单易用（easy to learn），我就是被这四个字骗了，开始用上了Git。现如今，它已经成为一种避无可避的工具了，必须学会。

要开始上手使用Git，可能真的是很简单的事情，如果你翻开一些成体系的文档或者书籍，可能上来会教你使用git init命令。这个命令的目的是创建一个新的git版本库。但是，就我个人的经验来看，一个新人，接触版本控制系统，可能第一件事情，往往是融入一个开发团队，接手一块业务，然后开始贡献代码，不太会是上来先建立一个版本库。
<!-- more -->
所以，我认为，使用Git的第一个任务，是学会使用git clone命令。（什么？你可能争辩，第一个任务当然是安装了！那么说也不算过分吧，不过，我看很多文章，包括官方自己的文档，第一个章节都是这个，实在是乏味，以至于我根本不想提起，也不愿意看到这个部分，尤其是，现在Windows环境的安装，已经越发友好了，甚至有图形界面，最不济，可以使用GitHub提供的客户端）

git clone命令实在是太简单了，以至于我甚至觉得，这一篇简直无法展开来写。因为你运行git clone命令的必须要知道的参数，只有一个而已——那就是版本库的地址。

版本库的地址，是什么形式，取决于你所在的团队使用的托管方案，视情况，可能是一个URL，一个URI，甚至是一个磁盘路径。

最常用的形式，是一个URL，也即，你所在的团队，使用Web服务器托管代码，然后提供一个http或者https协议的网址，作为版本库的地址。

然后，还可能是一个类似 git:// 开头的URL，这是使用Git自带的协议提供服务的版本库URL。

如果你所在的团队，在公用的开发服务器上开发，你需要clone的，可能就是服务器本地的一个磁盘路径了，类似/path/to/repo,指向一个具体的文件夹，那个文件夹就是一个git版本库。这种情况，也可能是一个ssh协议的远程服务器地址，类似 ssh://user@pass:server.domain:/path/to/repo

如果说，这个命令还需要一个参数能给你提供一点方便的话，可能是第二个参数，就是自定义版本库的文件夹名称。因为你可能同时维护两个名字叫api的版本库，你可以给他们起名为 mobile-api 和 web-api，这样即使在同一个父目录，也不会冲突。

那么clone命令到底干了点什么事情？描述起来，你仿佛做了类似svn checkout一样的事情，但是，上一篇文章，我已经说了，尽量不要用svn的方式去理解Git，clone其实做了远比checkout要多的事情。

第一，该命令拷贝了整个版本库到你的本地目录，包括所有人的所有历史记录，甚至所有的分支和tag，你可能会惊讶，为什么有的版本库体积达到1G，其实代码只有几十兆而已；

第二，该命令为你的版本库，添加了远程源，虽然你已经是整个版本库了，但是如果你需要与另一个版本库同步代码的话，那么你需要一个源地址，clone另一个版本库的时候，那个版本库已经作为一个远程源添加到你的版本库里了；

第三，为你建立一个本地分支，名叫master，然后自动checkout到这个分支上了；

看起来，有点厉害，但是更厉害的是，其实这个命令可以通过很多参数自定义其行为，比如我就知道，第三件事情，可以不做，具体参考文档就行了，不过，一开始，真没必要搞那么清楚就是了。

所以，你再把它当成svn的checkout的话，你就会错过太多太多了，不要再那样去类比了。