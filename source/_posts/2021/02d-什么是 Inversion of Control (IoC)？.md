---
title: 什么是 Inversion of Control (IoC)？
tags:
  - design pattern
  - object oriented
id: '1003'
categories:
  - [工作相关, 心得体会]
  - [工作相关, PHP]
date: 2021-02-25 13:12:47
permalink: inversion-of-control-ioc/
---

局限于英文水平和对软件工程“学术界”了解的浅薄，我对 Inverstion of Control —— 中文或许可以翻译成“反向控制” —— 的理解，总是停滞在一种似是而非的程度。我尝试通过搜索来学习，发现我能搜到的中文文章，都不能给我很大的帮助，有的在大谈特谈 Spring 框架如何如何；有的又说，想搞清楚 IoC，你先要理解 DIP …… ；也有的，干脆就说，所谓的 IoC 根本就是 DI。一时间，各种术语满天飞，越发让我觉得糊涂了。

不得已，我又开始搜寻英文资料，发现基本也是各种意见都有，但是无一例外都会指向一个地方，就是 Martin Fowler（马丁・福勒）的文章（很感谢国外这些博客的作者，都有良好的习惯，让人比较容易找到一个概念的发展脉络）。通过学习和对比各种国内的文章，我似乎对这个概念更加清晰了一些，不敢说全懂了，但是总算比以前明了了一点。特此记录。
<!-- more -->
## 缘起

我是一个 PHP 程序员，一直使用 Yii 框架，[从 2.0 版本开始，就显式地出现了 DI 这个概念](https://sexywp.com/yii2-abstraction.htm)，不怕丢人，我就是看不懂，不过就像大多数情况一样，看不懂也根本不会影响使用。不过，时不时遇到的时候，还是觉得萦绕心头，偶尔搜些资料看看，才知道了 IoC，[把 IoC 和 DI 联系在一起的人，是 Martin Fowler](https://martinfowler.com/articles/injection.html)（[中文版](https://insights.thoughtworks.cn/injection/)），就算他不是第一个，但是极有可能是影响力最大的一个。

对我来说，DI 和 Service Locator 之外，又出现了一个新概念，就自然而然顺藤摸瓜去了解，没想到我非但没有更清楚，反而更糊涂了，继而又陆续看了很多资料，才又出现了一丝丝清明。

## Inversion of Control

日常我们用到的词汇里面，有一种很常见的情况，就是除了这个词汇本身的内涵，在使用过程中，其外延不断扩展，有些甚至出现了引申意义，于是经常使得自然语言变得隐晦难明，给 NLP 带来困难的同时，人类自己也负担不轻。

这个经常被缩写成 IoC 的术语，如果翻译成中文的话，字面意义就是“反向控制”，但是，一般人读到四个汉字，基本是莫名其妙的。如果你使用了百度去搜索中文资料，看了一堆网友写的文章，相信你就离其真实含义更加遥远了（也包括本文）。

如果你在认真阅读本文的话，我试图传递给你的一个建议就是，不要相信所有的资料，包括本文。这样，或许你真的可以建立一些对这个概念的准确理解。这恐怕就是道可道，非常道吧，哈哈。

## IoC 是什么？

关于 IoC 是什么，国内外网友也莫衷一是。有人说，这是一种设计模式，“设计模式” 是随着 GoF 的著作传开的一个专有名词，其实是描述了在面向对象软件设计（OOD）过程里，为了实现解耦与复用，软件工程界惯用的一些优秀的（起初识别了 23 个）类关系设计方案。每一个模式，都有其比较具体的场景，以及相对来说比较具体的设计模板，渐渐已经成为工程师交流的一套工具。从设计模式的特点来看，IoC 恐怕不能说是一种设计模式，因为，首先就没有比较具体的场景，也没有比较具体的设计模板，实现方案也有多种。所以，决不能称其为一种设计模式。

常见的一种说法，说 IoC 是一种设计原则，维基百科也如此定义。我想，这可能是比较接近事实的一个说法。但是，比起软件工程里其他一些更为显而易见的原则，比如 DRY 原则，SOLID 原则等等，IoC 的含义就显得模糊，尤其 SOLID 里面的 D 代表的依赖倒置（Dependency Inversion Principle，也叫 DIP），跟 IoC 看起来似乎又像一个意思。不少中文世界的博客，甚至就蠢蠢欲动地想要完成两者的替换，从而避免对其进行解释。

也有说 IoC 是一种实现。这可能是一种隐晦的表达。因为提及 IoC，不少人就要说 Spring，说起 IoC Container，这就使其变得非常具体，好像它是一个框架，或者甚至是一个类。我想，头脑稍微清明一点，不至于误解如此，但免不了，还是有人似是而非地如此认为。

Martin Fowler 在一篇词源追溯的文章里，对 IoC 的定义，是一种“现象”，或者说一种“特点”。介于他是这个领域最权威的专家和最早探讨这个概念的人之一，我个人比较倾向于相信他的话。其实我比较佩服的就是他的写作能力，他精挑细选地这两个词汇，避开了人云亦云的“Principle”或者“Pattern”，可以看出他的态度。

> Inversion of Control is a common phenomenon that you come across when extending frameworks. Indeed it's often seen as a defining characteristic of a framework.
> 
> —— bliki: InversionOfControl Martin Fowler

其实，在 Martin 老爷爷另一篇文章里，就是那篇著名地介绍了 Dependency Injection 的文章里，他也很巧妙地避免了混淆，那里他用了 IoC Container 和 DI 放在一起讨论，而不是 IoC 本身。IoC Container 和 IoC 不是一个概念，就算没有“雷锋”和“雷锋塔”区别那么大，其实也差不多了。

## “好莱坞” 原则

有个趣谈也值得在这里谈起，就是大家都不约而同提到了 “好莱坞原则”，其实就是一句话，“别给我打电话，我们会打给你的！”，如果是英语的话，会更形象一点，因为打电话的那个单词是 Call，和函数调用的英语单词 Call 是一样的，所以，是一语双关。当然，所有人都提及了，就说明这个好莱坞原则比较容易看懂，但不能代表二者完全等价。

这么说的原因是，IoC 是关乎 Control 这件事情，虽然也是 C，但是，Call 和 Control 显然是两码事情，好莱坞原则，应该也暗含了 IoC，所以，两者才拿来一起说，是为了帮助去理解 IoC 的，不能代替之。

## 什么是 Control

有不少文章提到了，如果你想知道什么是“控制反转”，那么你先要知道什么是“控制”。这话说得大义凛然，然而到了具体分析什么叫控制的时候，没几篇文章给出让人眼睛一亮的答案。当然，我不能鄙视他们，因为我也给不出来，不过我还是能看出来他们给出的答案不够让人满意的。

Martin 老爷爷给举了一个例子，是这样的：

```ruby
  puts 'What is your name?'
  name = gets
  process_name(name)
  puts 'What is your quest?'
  quest = gets
  process_quest(quest)
```

这是一段 Ruby 脚本，纯命令行的程序，模拟了一个交互式 Shell 命令的实现，这个例子用以说明什么叫“控制”，用以对比后面要给出的“反向控制”的例子。从这个例子里，我们看到程序员作为程序的编写者，控制了这个程序的执行流程，先询问用户的名字，然后等待用户输入，然后处理此输入，再询问用户的需求，等待用户的输入，然后处理用户的输入。

很显然，这是一个简单的“过程”，从编程范式来理解，这是过程式（指令式 Imperative）编程的产物。程序员从头到尾，用编程语言描述了事情发生的步骤，也叫 Control Flow。用户在使用这种应用程序的时候，必须按照预先设定的顺序来操作软件，完全被软件所引导进行操作。

## Inversion 的例子

然后，我们再来看看同一个例子改换一下样子：

```ruby
  require 'tk'
  root = TkRoot.new()
  name_label = TkLabel.new() {text "What is Your Name?"}
  name_label.pack
  name = TkEntry.new(root).pack
  name.bind("FocusOut") {process_name(name)}
  quest_label = TkLabel.new() {text "What is Your Quest?"}
  quest_label.pack
  quest = TkEntry.new(root).pack
  quest.bind("FocusOut") {process_quest(quest)}
  Tk.mainloop()
```

这是同一个功能的另一个图形界面的程序，在这里，我们看到，这回因为是图形界面，程序员通过给特定的事件“FocusOut”，绑定了一个闭包，来处理用户的输入。我们可以假想一下，在这个图形界面上，有两个输入框，同时出现在用户的面前，不像上面的例子，先出现第一个问题，再出现第二个问题，这次是一个平铺的表单，用户先填第一个也行，先填第二个也行。一旦填写了其中一个，对应的处理程序，就会被调用，被谁调用呢？被 `mainloop()` 这个程序调用。

在这个例子里面，传递给我们的 Inversion of Control 有两个层面。第一个层面是，原本应用程序的执行流程，由编写的程序员控制，由程序员决定，先执行哪个方法，再执行哪个方法，而在这个例子里，编程了事件驱动，用使用应用程序的用户去很大程度决定，先执行哪个部分，再执行哪个部分。

第二个层面，则是在这个例子里，出现了框架，就是 Tk，这个框架，通过一个 mainloop() 方法，来发射所有的事件，从而驱动不同的事件处理程序运转，虽然程序员编写了这个程序，但是 Control Flow，不由程序员决定，运行哪个处理程序，由框架层面决定。

## 框架与类库的区别

看了上面的例子，你可能要想了，框架不都是这样的么？当我们使用框架进行编程的时候，都是我们实现一些特定的类，方法，业务逻辑，然后用配置组装起来，一旦框架运转起来，就会自动调用我们提供的那些类和方法。

没错，我想 Martin 老爷爷就是这个意思。所以，才说 IoC 其实是框架的 defining characteristic。正是因为框架这样设计，才使得框架区别于类库。对于类库来说，就是一系列设计完好的类，但是他们不会自动运行，需要程序员按照正确的顺序去构建对象并调用，而框架也同样是一群类，但是它们都实现约定了执行的顺序和方法，对程序员的扩展开放，但是修改封闭，程序员只能去扩展框架的功能，从而实现自己的业务目的，执行层面的控制由框架负责。

由此，IoC 成为了框架和类库的根本性的区别。

未完待续……

后续文章：

1.  《[为什么需要 Inversion of Control (IoC) ？](https://sexywp.com/why-need-inversion-of-control-ioc.htm)》
2.  《[怎么实现 Inversion of Control (IoC) ？](https://sexywp.com/ioc-implementation.htm)》

## 参见：

1.  [《Yii 2.0 框架学习笔记-基础抽象》](https://sexywp.com/yii2-abstraction.htm)
2.  《[bliki: InversionOfControl](bliki: InversionOfControl)》— Martin Fowler
3.  《[Inversion of Control Containers and Dependency Injection Pattern](https://www.martinfowler.com/articles/injection.html)》— Martin Fowler