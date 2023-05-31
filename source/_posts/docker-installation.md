---
title: 在 Mac 安装 Docker 环境的种种
tags:
  - docker
id: '738'
categories:
  - - 工作相关
date: 2016-08-21 14:27:14
---

其实很早就听说了 Docker 了，这正是现在世界上最炙手可热的容器技术。直到去年 2015 年，我们公司才有小伙，尝试使用 Docker，当时，我们公司是全 Mac 办公，而 Docker 只支持 Linux，于是各种非官方爱好者，做出了各种方案，比如当时，如果要在 Mac 上用 Docker，就必须安装一个 boot2docker 的组件，是一个在 Mac 上使用 Docker 的封装，同时还要依托 VirtualBox 才行，当然也有 VmWare 的版本，但是又是收费的。
<!-- more -->
这个 boot2docker 的方案，不但安装麻烦，其命令行界面也丑陋不堪。而负责去研究这个方案的小伙子，最终也没有给出特别好的技术方案，只是浅尝辄止的一个分享演讲而已，比较令人失望。

直到四个月前的 2016 年 4 月份，我终于有点空闲时间，用于研究 Docker，这个时候，Docker 官方网站，已经提供了 Docker Toolbox 用于解决在 Mac 和 Windows 系统使用 Docker 的难题。这个 Docker Toolbox 的实质，其实还是 boot2docker，只是这回，从非官方，变成了官方，名字也正名了，比较好听了，其核心，包含的组件和原来差不多。一个 docker engin，一个 docker compose，一个 docker machine，最后是 Kitematic。

所谓的 Docker Machine，其实质，仍然是 VirtualBox 里面的虚拟机，但是这回，提供了 docker-machine 这样的命令行接口，使得整个事情变得更加的简单，命令行接口被很大的简化了，用户需要搞懂的原理更少了。到这里，docker 对于 Mac 环境已经十分友好了。

后来，因为一些事情，我对 Docker 的研究又搁置了，直到这回，到官网一看，这回竟然提供了一个 Docker.dmg 来支撑 Mac 系统环境。这回，使用到的技术有了变化，其核心是一个叫做 xhyve 的组件。这个东西是 bhyve 在 Mac 上的一个移植，而 bhyve 是什么东西呢，其实是 FreeBSD 系统环境上的一个虚拟机管理器，而 Mac 底层也是 Unix 系统，所以一脉相承被人移植到了 Mac。这回，Docker 提供了一个叫 Docker.app 的图形化界面的 Docker 运行环境，执行起来，会在系统 Menu Bar 显示一个鲸鱼图标，这回就更具体，更可视化，更友好了。完全给了用户一个 0 学习成本的 Docker 使用环境。

这个官方的新组件，只支持 MacOS X Yosemite 10.10.3 以上版本，对于低版本来说，还是要使用 Docker Toolbox 里面提供的 docker-machine，而我在这个组件内部看到，docker-machine 指令也被打包到了这个里面。看来也是可以使用的。

Docker 是一个新兴技术，主要用于虚拟化和容器化，特别适用于现在流行的微服务架构，但是，不管怎么说，Docker 还是太新了，我想，我目前秉持的态度是，拥抱新技术，但是不能立即投入生产，技术架构的进化，还是要遵循规律，不是说 Docker 火，为了用 Docker 就去改造既有架构。架构是为了解决业务问题而存在的，除非有业务问题，既有架构模型解决不了，我不会轻易选择 Docker 用于企业生产。因为 Docker 不解决问题的情况下，一定免不了引入 Docker 本身有关的问题，那就得不偿失了。

以上是我几个月以来安装 Docker 环境时候的一点思考和记录。