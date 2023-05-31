---
title: Flutter/Dart 中常见的问题
tags:
  - documents
  - experience
  - usage
id: '1069'
categories:
  - - something-about-daily-work
    - Flutter
  - - 工作相关
---

## Dart 里面无法探知一个 late 变量是否已经初始化

如题，设计如此。在 Dart 里面，没有提供一种手段，来检测一个 late 变量是否已经被初始化了。当你访问一个 late 变量的时候，如果还没有初始化好，就会抛出一个异常。一般当时在构造的时候，立刻去初始化一个 late 变量。

如果你非要知道一个 late 变量是否已经初始化，只能再声明一个布尔变量来了记录这个事情。不过非常不建议这么做。因为 Dart 内部是会有一个类似机制来记录这件事情的。这时候，不如把变量声明为可空类型，然后检测变量是否是空值。

不过因为可空类型在访问的时候有一个非常啰嗦的语法，惊叹号或者探测是否为 null，所以对于访问频次很高的变量，声明为可空类型，确实给后续编码带来很大的不便。还不如声明一个布尔值来记录这件事情。(无奈，逃

## factory 构造器 vs 普通构造器 vs 静态方法

参见 [SO](https://stackoverflow.com/questions/52299304/dart-advantage-of-a-factory-constructor-identifier)

factory 构造器有如下特点：

1.  只能返回当前类实例或者子类的实例；
2.  因为这种构造器不直接创建一个实例，所以不能使用初始化列表，如（`: super()` 这种写法）；
3.  可以调用其他的构造器，可以返回一个已经存在的实例，可以返回 null；
4.  可以被声明为 `const` ；

## 设计模式系列文章

参见 [medium](https://medium.com/flutter-community/flutter-design-patterns-0-introduction-5e88cfff6792)

##  Incorrect use of ParentDataWidget

规则一：只能在 Column，Row 和 Flex 中使用 Expanded；

规则二：如果一个 Column 内部嵌套了一个子 Column 被 Expanded 包裹，则外面的 Column 也要被 Expanded 包裹。

## 在 GridView 里怎么绘制分割线

目前找到了一个模拟分割线的方法，就是给 GridView 用 Container 增加一个背景色，然后设置 MainAxisSpacing 和 CrossAxisSpacing，也即元素间间距，然后元素与元素之间就会露出一道缝，正好是背景色的颜色，好像画了分割线一样。

## 如何挑选合适的 Icon

经常需要选择一个小图标的时候，不知道图标叫什么名字，这个时候，最好的办法是使用搜索引擎，你得知道那个图标叫什么名字，才能比较容易搜到那个图标。Google 提供了一个 material 图标的检索网站：https://fonts.google.com/icons

## 如何获取屏幕宽度

使用 MediaQuery 可以查询屏幕的宽度：

```generic
double pixel = MediaQuery.of(context).size.width / 375;
```

上面的代码展示了如何计算一个宽度比例的代码，使用 MediaQuery 查询了屏幕的宽度。在这个代码里，用到了 context，只能在提供了 context 的情况下使用此查询。

此前，我有一个使用场景，在 MaterialApp 构造的时候，我想设定 Theme，这里设定字体的字号的时候，需要用到上面的那个宽度比例数据，这时候我发现，在 MaterialApp 还没有创建的时候，context 是不存在的，这时候，可以使用这样的方法来查询屏幕宽度：

```generic
var pixel = MediaQueryData.fromWindow(WidgetsBinding.instance!.window).size.width / 375;
```

如上，用到了 WidgetsBinding，这是从 SO 查询到解决办法，请见[这里](https://stackoverflow.com/questions/50214338/flutter-error-mediaquery-of-called-with-a-context-that-does-not-contain-a-med)。

## 使用 sqflite 的时候，Like 语句如何正常替换

```generic
result = await Db.instance!.query(
            'node',
            where: 'userId = ? AND name LIKE ?',
            whereArgs: [userId, '%$nodeName%'],
          );
```

我一开始以为是要写成 LIKE %?% 这个是思维定势，应该是 LIKE ?，然后在参数列表里加 %，哈哈……后来，我看到别人说，%?% 也是可以的，只是我忘记了加引号，好吧……是 LIKE "%?%"，这让我有点无语。

## GridView 每个 Item 怎么设置高度

我发现 GridView 不论怎么设置 Item 的宽高，绘制出来都是方形的。所以，如果每个 Grid 不是方形的话，还是需要在 GridView 里进行设置，是设置一个 childAspectRatio 的属性，这个属性的意思是，itemWidth/itemHeight，这样就可以让每个 Grid 不绘制成方形。参见[这里](https://stackoverflow.com/questions/48405123/how-to-set-custom-height-for-widget-in-gridview-in-flutter)。