---
title: 为什么需要 Inversion of Control (IoC)？
tags:
  - design pattern
  - object oriented
id: '1005'
categories:
  - 工作相关
permalink: why-need-inversion-of-control-ioc/
date: 2021-02-26 11:15:39
updated: 2025-06-29 11:01:18
---
[上一篇文章](https://blog.charlestang.org/inversion-of-control-ioc/)洋洋洒洒介绍了一些关于我对 IoC 的学习和理解，这篇文章继续来说说这个话题。认识一个事物，常用的方法就是 5W1H 法，这个方法提醒我们，尽可能全面去认识，不要遗漏某些方面，这里，最最重要的，可能就是 Why，也就是为什么。

这其实是一个非常艰难的话题，我只能硬着头皮来写写，因为能参考的东西实在是不多，就算是 Martin 老爷，也更多谈及了 What 的问题，比较少谈及了 Why，对于他来说，似乎是不言自明的。但是，说实在的，我不明白。比如说，我不明白，我们为什么要 IoC？如果不使用 IoC 的话，我们还有什么选择？IoC 和其他选择之间，优劣如何？

如果细看 Martin 老爷的文章，话里话外似说，其实所有的框架都是 IoC 的。我们似乎不能去对比 IoC 和非 IoC 的框架。等于就失去了和从差异去认识的机会了。

<!-- more -->

## 抽象

只能先从 IoC 本身的特点着手去理解一下为什么吧。软件开发里面，有一个核心的目标，就是管理复杂度，因为大千世界是复杂的，如果我们需要去程序语言实现这个大千世界的方方面面，就免不了要面对复杂。解决复杂基本的方法有两个，就是抽象和封装。

抽象的本质是什么？是抽取出关注点，抽取出共性，这样使得我们可以刻画一类事物，或者一类过程，在抽象后，我们可以忽略那些不重要的点，单独去处理抽象。但是，那些忽略的点，并不是真正的完全就忽略了。只是，放在不同的层次去关注而已。

举个很简单的例子，其实我们住的房子，是怎么盖起来的呢？是用水泥，砖头，钢筋等拼起来的。可以水泥是什么？砖头有是什么？其实他们还有他们内部的构造和组成方法。但是在盖房子的时候，我们关注水泥和砖头就行了。不用关注组成其的本来面目。这就是抽象层次的问题。在建筑这个层次上，我们关注到水泥，砖头，钢筋。到了房子完工了，我们居住前，需要装修，在装修这个层次上，我们关注的是几面墙，几块地板，几块屋顶，我们不需要管这个底本，这个屋顶这个墙是怎么用水泥和砖头组成的。只有在需要拆墙的时候，才需要关注是承重还是非承重，那是我们需要推测墙是钢筋混凝土还是砖墙，这等于是我们在重构墙壁，所以不得不关注其内部的实现。

抽象始于对具体事物的抽象，当有了很多对象后，我们需要的就是组合和调度这些对象，使得他们可以组织起来，然后实现我们的业务。当这样的事情规模越来越庞大的时候，我们其实就有了对流程和顺序的复杂度的管理需要。于是，我们需要对事情发生的流程进行抽象。

当我们对一类流程进行抽象后，本质上就是我们找到了这类事情的共性，排除了这些共性，得到的就是这类事物的抽象，这个时候，就出现了框架，所以我觉得框架就是这么一回事情。

![](../images/2021/02/request-lifecycle.png)

Yii 框架请求处理生命周期，程序员主要实现好自己的 MVC 就可以快速开发应用

例如，我熟悉的 Yii 框架，本身就是对 Web 请求处理的一种抽象。首先是一个 HTTP 请求，送达了服务器，然后我们要分析这个请求，过滤掉风险，然后找到正确的响应程序进行请求处理，其间，调用缓存，调用数据库，拼装响应，最后允许对响应进行再次过滤，返回给请求来源处。这个处理过程，凝聚成了 Yii 框架。我们还可以进一步抽象看待这个过程，给出一个输入，等待一个输出，就是这个过程的本质。看起来好像一个函数调用一样直接。于是，我们发现，似乎可以用这个框架处理一切满足这个特征的流程。所以，我们可以用 Yii 框架去实现命令行程序也没什么不妥，无非就是给出一个输入，等待一个输出嘛。

## 分工

抽象的事物，封装成了对象，抽象了过程，封装成了框架。对象和框架的创建，是为了复用，是为了我们能在更高一个层次上，用更大的抽象颗粒进行思考和建设。现在，程序员可以选择一种热爱的语言和框架，开始构建自己的业务了。

框架毕竟只是一种抽象，要变成具体业务，还需要程序员去下达指令。这其实是一种社会分工。有些人创建了框架，另一些人使用这些框架进行工作。但是这两类人完全不认识，要隔空进行合作。这种协作的基础，就是协议。每个框架理论上都允许程序员自行创建自定义的业务过程。框架必然要对这件事情有所考虑，才能让这种隔空协作变得流畅和自然。

比如，实现业务的程序员，不应该太过关注框架的实现细节，那样就有了很高的学习成本，使用一款框架也变得困难重重。为了某个框架专门去写的代码，恐怕也不能在另一个场景重用。这显然不美。像程序员隐藏实现细节就成了必然的选择。框架本身就是对事物流程的抽象，程序员又不必了解内部的细节，就只能是控制反转了。只要按照协议的约定，实现自己想要的业务流程，剩下的交给框架去调度就可以了。所以，框架极有可能全部是 IoC 的。因为这几乎是一个必然的理智选择。

大家都按照协议约定实现好自己的功能，等着别人去调用，这就成为了一种惯用法。在框架和应用逻辑之间，这种反向控制显而易见。但是因为这种思路的优势，应用逻辑与应用逻辑之间的组合，也可以受益。我们可以去封装细小的业务逻辑，然后在更高的抽象层次上组合这些逻辑，从而构建出庞大的应用。

## 隔离和组装

协议的隔离，是大家能够有效分工的关键，不过，隔离完分工实现细节后，免不了还是要组装。不然没法形成一套系统。但是怎么组装起来呢？负责组装的这个对象，必然要了解所有被组装的对象。而“了解”，就代表了耦合。本质上这是无法避免的。

不过，我们已经做了很多事情，以实现尽可能在更大范围内去避免耦合了。最后这个最小程度的耦合，就分化出来不同流派的实现。

组装其实要面临很多的问题，首先，组装点不可能只有一个，因为业务有大小，不可能每个业务点都组装所有的组件，最好要按需去组装，组装完后。刚才说过，我们要使组装的点尽可能少，以减少耦合，但是这里又说，各个不同的大小业务，要按需分别组装，两者几乎是矛盾的，一个是少，一个是多。

![](../images/2021/02/abstract-factory.jpeg)

Abstract Factory 模式，体现了 IoC 思想

还有一个办法，就是组装的时候，把组装的这个过程再次抽象，要把耦合的部分尽可能封装在一处。业务与业务之间通过协议来协作，可以互相调用，剩下的事情，就只有组件的创建了。因为不同业务的实现，需要不用的资源，有的用磁盘，有的用缓存，有的用数据库，有的用网络连接。如何构建不同组件，组织各种组件的必须资源，就成了一个不得不去耦合的知识，我们要尽可能把这种对组件构建的耦合知识封装在一处。

到这里，我们可以看到，IoC 的问题，在实现层面，最终聚焦到了一个问题，就是组件对象的创建问题。因为这里蕴含了最多无法避免的知识的耦合。可能，这也是提及 IoC 的实现的时候，各种具体的实现，都没什么 Control 的气味，反倒都是在讲怎么创建对象，怎么处理依赖了。

未完待续……

系列文章：

1.  《[什么是 Inversion of Control (IoC) ？](https://blog.charlestang.org/inversion-of-control-ioc/)》
2.  《[怎么实现 Inversion of Control (IoC) ？](https://blog.charlestang.org/ioc-implementation/)》
