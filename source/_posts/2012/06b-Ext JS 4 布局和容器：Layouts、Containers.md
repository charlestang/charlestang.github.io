---
title: Ext JS 4 布局和容器：Layouts、Containers
tags:
  - component
  - container
  - extjs
  - layout
id: '488'
categories:
  - [工作相关, ExtJS]
date: 2012-06-15 14:08:16
permalink: ext-js-4-layouts-and-containers/
---

布局系统，是Ext JS中功能最强大的部分之一。系统中的每一个组件在页面上的尺寸和位置，都由该部分负责管理。这篇文档是Ext JS布局入门的文档。
<!-- more -->
## Containers

ExtJS的图形界面，是由组件构成的。容器，是一种特殊的组件，其功能就是包含其他组件。一个典型的ExtJS应用由若干层嵌套的组件构成。

最常用容器类组件是Panel。下面的代码展示了Panel作为一个容器如何包含其他的组件：

```javascript

Ext.create('Ext.panel.Panel', {
    renderTo: Ext.getBody(),
    width: 400,
    height: 300,
    title: 'Container Panel',
    items: [
        {
            xtype: 'panel',
            title: 'Child Panel 1',
            height: 100,
            width: '75%'
        },
        {
            xtype: 'panel',
            title: 'Child Panel 2',
            height: 100,
            width: '75%'
        }
    ]
});

```

上面的代码创建了一个Panel，在HTML的Body元素上渲染，里面添加了两个子面板。

## Layouts

每个容器类的组件都有一个布局用来管理其内部组件的尺寸和位置。这里，我们要展示一下一个容器如何通过配置来使用某种特定的布局，并且看看布局系统如何保证每个部分都同步。

### 使用布局

在上面的例子里，我们没有制定最外层Panel的布局，所以内部子Panel就是一个挨着一个，从上到下顺次排列在外层的Panel上面。其布局形式跟一般的Html块级元素在页面呈现的布局相似。这在ExtJS中，也是一种布局方式，叫做Auto Layout，该种布局方法，不指定任何子组件的位置和尺寸。假如，我们需要两个子Panel并排排列，各占50％的宽度，我们可以使用Column Layout列布局，只要通过指定容器的layout属性，就可以做到这一点：

```javascript

Ext.create('Ext.panel.Panel', {
    renderTo: Ext.getBody(),
    width: 400,
    height: 200,
    title: 'Container Panel',
    layout: 'column',
    items: [
        {
            xtype: 'panel',
            title: 'Child Panel 1',
            height: 100,
            columnWidth: 0.5
        },
        {
            xtype: 'panel',
            title: 'Child Panel 2',
            height: 100,
            columnWidth: 0.5
        }
    ]
});

```

ExtJs有全系列的布局方案，可以实现几乎任何你能想象出来的布局。

### 布局系统的工作原理

一个容器的布局负责初始化所有子组件的位置和属性。框架内部会调用容器的doLayout方法，这会触发Layout来计算出所有子组件正确的尺寸和位置，并且更新到DOM。doLayout方法是递归调用的，所以，所有子组件的doLayout方法，也会在那个时候被调用，一直到最底层级的组件为止。你在使用框架的时候，没有必要自己手动调用doLayout，框架会为你做好这个工作。

当容器被resize的时候，会触发容器的re-layout，或者子组件内部的对象被添加或者删除的时候也会触发这个过程。通常情况下，我们只要依赖framework提供的功能来处理布局更新的事宜，但是有些时候，我们可能希望框架不要替我们做这件事情，因为我们可能需要连续操作若干的组件，我们会希望等所有操作完成后，一并重新计算布局信息。这个时候，我们可以用容器的suspendLayout标志来阻止自动的layout，当我们处理完容器内部的组件后，我们要做的工作是取消suspendLayout，然后手动调用doLayout方法。

## 组件布局

就像容器有布局一样，组件也可以通过指定布局来管理位于其上的控件和对象。组件布局使用componentLayout属性来指定。一般情况下，你是不需要指定这个属性的，除非你在自定义组件，因为所有的预定义组件都已经带有了他们各自的布局管理器来里管理位于其内部的元素尺寸和位置。大部分组件使用Auto Layout，但是复杂的组件需要一个自定义的组件布局，比如Panel。

## Layout盘点

![ExtJS 4 Layout](https://lh5.googleusercontent.com/-oW-XrAA_kF0/T9SYqQ4n6pI/AAAAAAAACAE/Emq5KWd4jmI/s800/%25E5%25B1%258F%25E5%25B9%2595%25E5%25BF%25AB%25E7%2585%25A7%25202012-06-10%2520%25E4%25B8%258B%25E5%258D%25888.43.20.png)

从这个图里面，我们可以看到组件布局中，只有一种布局就是Auto，而大部分布局都是在容器布局下面。下面逐一来罗列一下这些布局的用途：

布局

用途

Anchor

使包含的元素相对于容器的尺寸发生变化。如果容器被resize，那么内部包含的元素就会根据指定的规则来自动重绘。这种布局一般不使用new来创建，也没有直接的配置选项。此种布局没有任何直接的配置选项。缺省情况下，AnchorLayout基于应用容器的尺寸来计算锚定规则。使用AnchorLayout的容器，可以通过anchorSize属性来设定可供内含组建计算尺寸用的虚拟容器。（经我实际在Panel上测试，该属性不起作用，不知道什么原因）

Absolute

是AnchorLayout的子类，在Anchor的基础上，提供了通过x、y的值来指定内含组建位置的能力。

Box

不能直接使用，是HBox和VBox的基类。

VBox

在容器中，垂直布局内含组建的布局。这个布局将垂直方向上的空间，按照flex属性指定的值分配给内含组件，作为其高度。可以设置内含组件的宽度width和水平对齐属性align。flex相当于是按照比例分配高度的意思。比如可以通过flex属性，将内含三个组件的高度设为2：3：3，它们会按照这个比例，占满容器的高度。将flex设定为0或者undefined，组件的高度将不会变化。

HBox

水平排布内部组件的容器布局方式。同VBox，也有个flex属性，行为相同。

Accordion

VBox的子类，实现了一种让许多面板在垂直方向上可以折叠展开的布局方式。任意时刻，只能展开一个面板。折叠和展开的行为都是自动支持的，不需要额外的编程。只有Panel和Panel的子类才能用于使用了Accordion布局的容器内部子组件。

Auto

这是一个缺省布局方式，如果一个容器没有指定layout的话，都会使用Auto布局方式。Auto布局什么都不做，只是把布局的调用透传给子容器。

Form

这种布局方式用于渲染表单域，表单域一个一个纵向排列并且会被拉长到填满容器的宽度。在这种布局内，内部元素上设定的padding值都会被忽略。

Border

这是一种多窗口，面向应用的UI布局样式。支持多层嵌套面板，块于块之间自动的分界，支持某块区域的展开和缩起。通过border关键字来指定或者扩展，一般不用new关键字来创建。此布局内的空间被分为东南西北中五个区域。设定split属性为true，可以使某块区域能被resize。所有使用这种布局的容器，至少要指定一个子元素，来占据“中间”区域center。中间区域的子组件总是会撑满容器没有被设定的剩下区域。西侧或者东侧的子组件可以指定初始宽度，或者通过flex属性来指定宽度占比。同理，南北两侧的可以指定高度。可以用collapsible设定是否可以折叠。

Fit

对于只包含了一个组件的容器，这种布局使得内部组件撑满容器。这个布局没有配置选项。如果容器中有多个组件，所有的组件的尺寸都会设为相同，这一般来说都不是我们期望的行为，所以在fit布局的容器中，只能放一个子组件。

Card

这种布局形式，将容器内部子组件都撑满到容器的大小叠放，所以一次只能显示位于最上面的那个组件。这个布局方式，通常用来创建应用的向导程序。这种布局有个方法setActiveItem来决定显示哪个组件，参数是id或者下标。布局本身不提供UI来实现内部组件的导航，所以开发向导的时候，要自己开发导航按钮。

CheckboxGroup

这个布局用于实现复选框和单选框在页面上的布局管理。它根据组件的columns属性值和子组件的vertical属性值来组织布局容器内的元素。

Column

对容器进行分栏布局，分栏的宽度可以用百分比，也可以用固定宽度。分栏的高度是可以根据内容来指定的。此布局本身没有什么配置选项，但是位于此布局中的面板，可以使用columnWidth属性来指定分栏宽度。

在指定宽度的时候width属性和columnWidth属性都是有效的，width的值必须是大于1的整数，columnWidth的值是百分比，取值范围是0到1的左开右闭区间。

在渲染布局的时候，外层容器首先遍历内部宽度固定的面板，然后算出剩余没有分配的宽度，然后按照columnWidth所指定的百分比，分给其他面板。所以，此布局中所有使用columnWidht指定宽度的面板的columnWidth值之和必须是1，否则该布局的行为不可预期。

Table

使界面按照HTML的table的形式来进行布局，可以指定总的列数，然后配合colspan和rowspan来生成复杂的表格结构。这个布局背后的思想就是一个table元素，所以，所有的注意点都跟table的注意点一样。该布局只需要指定列数column，然后会将其内子元素按照从左到右，从上到下的顺序排布在界面上。

## 总结

ExtJS 4 给我们提供了丰富的界面布局，帮助我们能够快速简单的创建用户界面。