---
title: ExtJS 4 的MVC
tags:
  - analytics
  - development
  - extjs
  - MVC
  - yii
id: '445'
categories:
  - - something-about-daily-work
    - ExtJS
    - 心得体会
date: 2011-07-10 01:39:44
---

ExtJS是我听说了很久的一个js框架了，但是从来就没有用过，读研期间寝室里有个小哥在用，不过那时候醉心于WordPress开发，也懒得理会了。现在公司里，有个上线系统用到了这个框架中的一个TreePanel组件，整个界面上，就正中间扔了一个tree panel，而且不知道什么原因，CSS还有bug，把按钮都搞破了，弄得丑陋不堪，我于是自告奋勇，仔细调试，终于修复了那个显示上的bug，从此算是初次结识了ExtJS。它真正吸引我的原因是，它能够把富客户端应用的开发，从美工和基础交互中解放出来，只需要专注于业务逻辑开发即可，从而让后台工程师也能够有能力快速开发外观专业的网站应用系统。我觉得这真是功德无量的一个事情。（如果我直觉没错，Flex框架也是这一类东西，这也是我对其有兴趣的原因，当然还没有时间尝试）
<!-- more -->
[![ExtJS 4 MVC](https://lh6.googleusercontent.com/-NjYqHh6WjX0/ThiD-8_-xxI/AAAAAAAAB5w/jjqmfY8JrZE/s800/ExtJS%2525E5%2525AF%2525B9%2525E8%2525B1%2525A1%2525E5%252585%2525B3%2525E7%2525B3%2525BB%2525E5%25259B%2525BE.png)](https://picasaweb.google.com/lh/photo/6w-l2AcPyxIcU35pqAdwTA?feat=embedwebsite)

据官网介绍，还有据同事[ishow](http://www.showframework.com/)的描述，ExtJS 4.x 是一个变化很大的版本，相比已经应用广泛的 3.x 来说，变了很多、新特性也很多，MVC就是它提供的新特性之一。由于我最近半年都在学习MVC模式（主要是使用Yii框架），所以这个名词更是引起了我浓厚的兴趣，这几天都在官网上看这个框架MVC的例子，直到今天，总算是摸着一点门道，于是画了上面那个图。这个四不像的图，是我个人对框架的理解的第一个具体化产物。

下面简单描述一下这个图。

1. 每个应用都有一个实体，就是Application对象实例，而每个应用同样也采用单一入口结构，有个快捷函数就是Ext.application({config})，创建一个Application对象实例，并且运行它；这里行为表现和Yii框架的Application看起来很像，创建一个实例，然后run；

2. Application在创建之初，会去加载Controller类，加载完毕后，会正式的lunch；

3. Application在lunch的时候，会创建一个Viewport对象实例，这个东西就像一个骨架一样，上面可以拼装各种View，具体说，就是各种布局形式和窗体控件，可以说是应用界面的载体；

4. Controller的角色完全是个粘合剂，它在加载之初，会帮忙加载跟其有关的Model，Store，View类，而其真正的作用，是通过一系列的事件处理函数，确定了每个View上面界面组件对用户交互行为的响应方法，可以说是一堆事件处理器函数的集合；这里面主要通过一个control成员函数来进行事件绑定，通过另一个叫ComponentQuery的组件，使用类似css selector的语法来定位界面上的组件，并为其绑定事件处理器；

5. Model是对抽象数据的具体化，或者可以这么理解，就是数据库里面的一行记录，到底是怎么变成一个对象的，将数据库字段变成了对象的属性的对应关系；而这里比Yii框架MVC模型多出来的东西，就是Store这个东西，在Yii框架里面，有强大的ORM系统，还有强大的AR将Model直接连接到了DB上，数据一出来就直接变成了对象，而在ExtJS框架中，代码全在客户端，势必就出现了透过网络来加载数据需要，而我认为，Store就是对通过网络来加载数据的过程的一个抽象，Store依赖于Model，通过关联的Model对象来获知如何将取回的数据对象化，以方便View展现，所以View是依赖Store对象的；（这里岔开一点，感觉这个Store的设计理念或许可以借鉴，由于某些原因，我们在使用PHP框架的时候，不能让Model直接连接DB，是不是也可以把数据取回最终拼接成Model对象的这个过程给抽象化成类似ExtJS中Store的这套机制呢？）

6. View就纯粹是一个界面组件，或者说窗体控件的集合，通过Store来加载数据并且展现到界面上，界面控件的响应都写在Controller里面，View对Controller的存在全无所知，也没有代码上的依赖；

总结一下，感觉这套系统的好处是在于，将View和Model都给抽象了出来，以至于它们可以更加好地被复用，做好一个面板，所有的地方都可以调用，而真正业务逻辑又被很好的封装在了Controller里面，这样也便于去模块化地开发系统，基本感觉上，是一套非常优秀的框架，由于我对ExtJS 3系列版本，没有任何经验，也就没法做出其相对于先前版本是否有质的飞跃的判断，通过仔细的挖掘，我发现其易用性上确实比我原来想象的要好，开发人员可能没太多必要去纠结于内部原理，只要理解到跟我现在差不多的样子，就可以快速上手去做一些东西出来，当然还是必须看着文档按图索骥的，嘿嘿:)