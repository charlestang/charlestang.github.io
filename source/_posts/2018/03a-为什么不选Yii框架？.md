---
title: 为什么不选Yii框架？
tags:
  - Architecture
id: '600'
categories:
  - 日　　记
date: 2018-03-08 16:32:14
permalink: why-not-yii/
---

以前，我也注意到，不在现有项目中引入框架是有原因的，而且，尤其不能选用Yii框架。

## "继承"噩梦

你所有的controller，都继承自CController，其又继承自CBaseController，这个又继承自CComponent。

所有你的model，都继承自CActiveRecord或者CFormModel，它们又继承自CModel，这个CModel也继承自CComponent。

这两者的继承链条，都包含了静态变量，并且执行了其他很多类的静态方法。这两个因素造成调试过程变得极为困难和冗长。

## 全局状态

有多种形式的全局状态。PHP程序员熟知的就是全局变量。但是这并不是唯一的一种形式。类中的静态变量，也是一种全局状态，它（总是）能够造成看起来没有关系的类实例神秘地交互。

（Yii框架）对全局状态的使用是其核心机制。在代码中，你到处都能看到静态方法的调用，而且，Yii的配置文件，离了全局状态就没法工作。

每次你调用Yii::app()的时候，你都在访问或者改变它。

这使得统一测试你的Yii应用，成为了不可能。而调试工作，则变成了练习在你的整个项目中使用grep。

## 紧耦合

当你使用Yii创建一个应用的时候，如果不启动整个框架，你是不可能只运行其中一部分的。大多数时候，取决于你最终在你的代码里用了静态方法。

每次你在你的代码里添加了一个静态方法的调用，这段代码就跟那个静态方法的类耦合起来了。这就是紧耦合。

你可能已经注意到了（我希望你注意到了），有其他的方法可以实现一样的效果，使用new操作符。这是另一个方法让你的代码跟某个特定的类耦合起来。没有接口。

无论Yii项目的配置文件看起来有多吓人，这个配置文件的设计仍然是用心良苦的。这是在本已经一团糟的代码里，再度引入外部代码并代替已经存在的组件的伤害最小的一种方式。

然而，它将（Yii框架）缺少接口和存在耦合带来的问题带到了聚光灯下。

很多程序员想要替换的组件之一是CUrlManager，大多数是因为你能够传递额外的参数（给它）的方式的原因。

OOP中的接口，明确了两个实例间的约定。由你来定义实例的能力，能被别人调用的方法。如果一个大的代码里，没有接口的话，你就不得不猜测，哪些方法是必须的，哪些不是。

在Yii组件里面，问题甚至更加严重，因为使用了静态调用和深度继承。上文提到的CUrlManager继承了CApplicationCompnent，它又继承了CComponent。而CUrlManager的同一个文件里，还定义了CUrlRule和CBaseUrlRule。

当你编写一个他们的替代品的时候，你必须写一些代码，将他们插入到配置文件中，并在你自己的Application中测试，使用这种方式，你才知道下一个需要你填写的方法是什么。

基本上来说，这是一种“保存，然后看看什么东西爆掉了”的研发方法。

这绝不是MVC！

Yii并没有实现MVC或者任何受MVC启发的设计模式。它叫做“MVC”的东西，实际上可以用“ActiveRecord－Template－Logic”模式来描述。

Yii框架的作者，实现了一组active record和表单封装，而不是一个恰当的模型层，这导致应用的逻辑必须写在controller里面。

另一方面，你有光彩夺目的模版，而不是恰当的视图实例，来包含展示逻辑。

On the other hand you have glorified templates, instead of proper view instances for containing presentation logic. It is somewhat mitigated by use of widgets, but those instead suffer from SRP violations, because widgets are forced to contain bits of presentation logic and perform partial rendering. The rest of presentation logic ends up again in the controllers.

And to make it all worse, the "controllers" also have to deal with authorization. This usually will mean, that whenever you change the access scheme, you will have to go through every single instance of CController to check whether it needs to be changed too.

It's not MVC. It's a mess with names taken from MVC design pattern and slapped on some components.
All the small things ..

The framework also comes with few minor issue, that do not deserve a separate section:

Defining more then one class per file:

This will get annoying quite fast, because there will be classes that are shoehorned at the class files with completely unrelated filenames. This will mean, that debugging will quite often require use of search.

Slapped on "modules":

By the looks of it, the modules where added to the framework after the fact. Which is why, when you need to set default module, you will have to set it in the configuration files parameter, that is called 'defaultController'.