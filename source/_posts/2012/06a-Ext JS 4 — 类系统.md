---
title: ExtJS 4 — 类系统
tags:
  - extjs4
  - how-to
id: '486'
categories:
  - - 技术
    - 前端
permalink: ext-js-4-class-system/
date: 2012-06-08 16:19:26
updated: 2024-04-22 13:42:58
---
因为工作的关系，最近参与的一个项目中，我目睹了 ExtJS 在项目中发挥出来的强大的生产力，以及在 Web 界面方面强大的表现力，另一方面又很喜欢 js 这个语言，所以，下决心学习以下 Ext JS，正好新版 4.1 发布了，可以学新技术了。本文章为系列文章，内容或来自翻译，或来自自己的学习感悟，属于理解、记忆、融会贯通的一个辅助，也希望对诸君有利。

<!-- more -->

本文内容来自[ExtJS 的文档](http://docs.sencha.com/ext-js/4-1/#!/guide/class_system "ext-js-class-system")，并非字字对译，请读者自行斟酌。

## 设计初衷

Ext JS 是一个非常流行的框架，据说，迄今为止，大概有 20 万左右（自吹自擂？）的开发者在使用 Ext，这些开发者拥有不同的编程语言背景，并非全部专业，这就要求 Ext 能有一个通用的代码架构，必须有以下一些特性：

- 熟悉易学
- 开发迅速、调试简单、部署方便
- 良好的组织，易扩展、易维护

Javascript 是一门非常强大的动态脚本语言，纯面向对象，原型继承，灵活是其最大特性。所以 js 代码往往维护困难，复用困难。面向对象是一种优秀的方法论，强类型，要求开发者遵循一些编码约定，从而使得代码更佳易读，容易扩展和维护，但是一般的面向对象语言，不像 js 这样拥有这样的灵活性和动态特性。

ExtJS 是一种解决方案，在 javascript 编程和面向对象编程中，寻求一种平衡。使得开发者即能享用 js 灵活强大的特性，又能写出面向对象编程范型所能达到的规范性、扩展性和维护性。

其实，我个人觉得 js 是我接触过的语言中，特性最多的一个语言，据说很多东西脱身于 LISP，所以 js 也应该拥有面向语言编程的能力，就是首先构造一门最容易解决当前问题的语言，然后用这个语言把问题给解决掉，这是我的一点浅见，所以 Ext 我感觉，也是这么一种领域语言，要解决的问题是使用 Web 页面作为用户交互界面这么一个领域的问题，在这个问题的前提下，构造了 ExtJS 类库，用于帮助快速解决构造 Web 交互界面的问题。所以，学习的时候应该抱有这么一种心态，ExtJS 是一门全新的语言，领域语言（Domain Language）。既然是 Domain 的，那也一定有其合理的局限性，这个学习之前应该有个合理的心理预期，没有银弹。

## 命名规范/编码规范

简单说就几条东西，也是老生常谈，我连例子都懒得挪过来了：

 1.  所有代码都要放到特定的名称空间中
 2.  名称空间的第一层，应该是驼峰形式命名的
 3.  不要使用字母和数字以外的字符，数字在绝大部分情况下也不建议使用
 4.  类型名字使用驼峰
 5.  除了第一层的包名字和类名，全部小写
 6.  使用句点分割多层的包
 7.  包名字应该和存放路径相对应
 8.  缩略语只有首字母大写，如 Http，不是 HTTP，Json，而不是 JSON
 9.  方法名和属性名采用驼峰，首字母小写
 10. 类常量，要全大写字母组成

还是比较清晰明了的，也很容遵守，知道了规则，照着猜方法名字也应该比较简单。

## 类的定义和继承

js 语言本身是面向对象的，所有的东西都是对象，没有类的概念，支持的原型继承，也没有我们一般了解的继承的概念，所以 ExtJs 在这个方面进行了一些扩充。ExtJs3.x 是使用一个 extend 函数：

```javascript

Ext.ns('My.cool');
My.cool.Window = Ext.extend(Ext.Window, { ... });

```

函数第一个参数是要继承的类，后面是子类的属性。这种形式有几个问题，比如代码范例中，要继承 Window，如果页面上 Window 类还没有加载，则这个地方会报错，另一个是等号左边，如果类名中间部分不存在，也会报错。所以还必须引入一个 namespace 的函数，在声明类的时候，声明名称空间，如果不存在，会自动创建。

从 ExtJs4 开始，这个部分得到了优化，这两个步骤都统一使用一个 define 函数来实现：

```javascript

Ext.define('My.sample.Person', {
    extend : 'My.sample.Man',
    name: 'Unknown',

    constructor: function(name) {
        if (name) {
            this.name = name;
        }
    },

    eat: function(foodType) {
        alert(this.name + " is eating: " + foodType);
    }
});

var aaron = Ext.create('My.sample.Person', 'Aaron');
    aaron.eat("Salad"); // alert("Aaron is eating: Salad");

```

首先不再需要等号左边的部分，直接在 define 函数的第一个参数来指定类名，而需要继承的类，采用参数中的 extend 属性来指定。这样的好处是，不再需要使用 ns 函数来指定名称空间，define 函数会自动接管这部分；其次，是不需要担心继承的类页面上不存在，define 函数会自动探测，如果类的定义还没有引入，ExtJs 会尝试自动加载，直到加载完成才继续往下执行。这个特性会造成代码阻塞，所以实际运用时候，可以通过事先调用 import 之类的方法，来优化代码加载。

## Configuration

ExtJs3 的类也有 config，在构造实例的时候，可以传入 config 对象。ExtJs4 中，这个有所改变，文档中是说这里是 configuration，我实际理解下来，这个地方其实是事先了类的属性和方法。首先 config 中定义的类属性，其封装方法跟一般的类属性不同，都会通过各自的 getter 和 setter 来访问，基类中都有缺省的 getter 和 setter，而且在子类中可以覆盖这些方法，从而实现在其中追加业务逻辑。

```javascript

Ext.define('My.own.Window', {
   /** @readonly */
    isWindow: true,

    config: {
        title: 'Title Here',

        bottomBar: {
            enabled: true,
            height: 50,
            resizable: false
        }
    },

    constructor: function(config) {
        this.initConfig(config);
    },

    applyTitle: function(title) {
        if (!Ext.isString(title)  title.length === 0) {
            alert('Error: Title must be a valid non-empty string');
        }
        else {
            return title;
        }
    },

    applyBottomBar: function(bottomBar) {
        if (bottomBar && bottomBar.enabled) {
            if (!this.bottomBar) {
                return Ext.create('My.own.WindowBottomBar', bottomBar);
            }
            else {
                this.bottomBar.setConfig(bottomBar);
            }
        }
    }
});

```

在上面的代码段中，我们看到类定义了两个属性，一个是 title，一个是 bottomBar，并且为这两个属性实现了自定义的 setter，title 不能被设置为 null，否则会报错，bottomBar 的逻辑是如果不存在属性，会在设置的时候创建。

## statics

ExtJs4 中，实现了类的静态成员，类似上面的 config，使用一个 statics 属性来定义静态成员，调用静态成员的时候，不需要实例化类对象。

## 错误处理和调试

ExtJs4 引入了一个新的函数 Ext.getDisplayName()，可以用于返回发起调的用函数的名称，可以在抛出异常和错误的时候用于显示相关信息，另一个改进，是使用 define 定义的类和方法，如果抛出异常，可以在基于 webkit 内核的浏览器 console 中，显示出调用堆栈。

## 总结

ExtJs4 在类系统方面，有着很多的加强，很多类都从底层开始，全部重新实现，给我们带来了很多激动人心的新特性。相信在开发中，也会因此而带来更好的编程体验。
