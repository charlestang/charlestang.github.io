---
title: MVC最佳实践
tags:
  - development
  - MVC
  - programming
id: '414'
categories:
  - - something-about-daily-work
    - PHP
    - Yii
  - - 工作相关
date: 2011-03-07 17:44:39
---

前一段日子，写了一篇《[MVC就是一个选择题](http://sexywp.com/mvc-chose-where-to-put-your-code.htm)》，重点描述了我对MVC模式的迷惑。随着我对这个模式应用时间的深入，渐渐感到得心应手，这个模式早在30多年前就已经发明了，确实经受了时间的考验，可以说是千锤百炼。但是，实践过程中，我也发现，更多的时候照猫画虎还是有很多弊端的，想要真正做好MVC的选择题，必须在项目中不断犯错误，不断修正，才能逐渐走上正轨。我参加的项目主要运用了Yii框架，是目前比较流行的一个Web开发框架。随着前不久，1.1.6版本的发布，我发现Yii框架的文档中，多了一篇MVC最佳实践的文章。我想，这个文章对于初学者来说，应该具备相当的指导性，而且指导相当具体。如果也有跟我相同的迷茫，应该好好钻研一下这篇文章，并且身体力行去验证之，[这里给出链接](http://www.yiiframework.com/doc/guide/1.1/en/basics.best-practices)。我在这篇文章中，就是概括简述一下那篇文档的内容。
<!-- more -->
MVC的核心理念是代码的重用和关注点的分离（Separation of concern 我个人对这个理解就是将数据和表现进行分离）。如何正确遵循MVC的原理来编写代码是有一些基本指导原则可以遵循的。为了便于理解后面将要叙述的指导原则，我们这里认为一个典型的Web应用由以下几个子应用（部分）组成：

*   前端——网站界面，面向普通用户
*   后台——一部分有管理权限的用户用于维护Web应用的正常运转
*   控制台——在终端中执行的命令，或者是定时任务如cronjob，用于日常运维
*   API——用于第三方合作，或者二次开发

### Model

模型用于表示底层数据结构，经常在整个应用的不同部分共享，有些模型在前后台、API中都会用到，所以一个模型应该遵循的指导原则有：

*   包含属性用于描述特定的数据
*   应该包含业务逻辑，以确保数据能够满足表现的需要
*   应该包含数据操作的代码，比如数据存储、检索
*   不应该使用$_GET $_POST这样的只有在前端才会出现的数组，在控制台和API用到时候，可能就无法复用了
*   不应该出现HTML代码，负责表现的代码应该放到view文件中

在上述指导原则下，可能会写出非常庞大的Model类（过多数据操作，业务逻辑代码包含其中）。这种情况下，建议进一步抽象，提炼出一个基类，包含最通用的功能，然后前端、后端和API在用到时候，将各个子应用才相关的逻辑放到基类继承出来的子类里面。

### View

视图主要就用于前端表现的代码。

*   包含HTML，以及所有负责表现的代码，可以出现PHP，但是只用于遍历数据、格式化数据
*   不应该包含DB请求
*   不应该出现引用$_GET $_POST这类数组的代码，这应该是Controller的工作。View只是专注于表现，布局等和页面呈现有关的业务，用户的请求数据应该由Controller和Model负责处理
*   如果必要，可以访问Model和Controller的属性，不过这是为了满足表现的需要

可以使用诸如布局、部分视图、HTML Helper类、Widget等框架特性来最大程度重用View的代码。

### Controller

控制器是将模型、视图和其他组件组装在一起形成一个应用的粘合剂。控制器直接负责处理终端用户的请求。

*   可以访问$_GET $_POST这样的用户请求数组
*   创建模型，并决定一个模型对象的生命周期
*   不应该出现SQL语句，数据库请求应该放到Model中
*   不应该出现HTML代码，而应该将其放入到View中

在一个设计良好的MVC应用中，控制器是非常轻量级的，经常只有几十行代码的样子；而Model总是非常复杂而且庞大，包含了所有的用于表现的数据及其操作方法。这是因为由数据结构和业务逻辑组成的模型对每个应用来说，都是独特的，需要大量的定制化工作来满足应用的需求；控制器的逻辑经常遵循一个特定的套路，在各个应用中都差不多，因此可以被框架底层代码极大程度地简化（也就是说不是控制器代码少，而是Web开发框架已经都抽象出来并且都帮你做好了，这也就是框架的价值和能够实现快速开发的原因）。