---
title: jQuery里面用到“打包盒”
tags:
  - code reading
  - jQuery
id: '463'
categories:
  - - jQuery
date: 2011-10-23 01:45:43
---

想学学怎么写jQuery的插件，结果发现举步维艰，于是想通过研究插件代码的案例，来积累经验，结果看到第一行，我就郁闷了，天下间最郁闷的事情莫过于你出门去约会，结果刚打开门，就摔个狗吃屎，现在我就那个感觉。看代码：

```javascript

//第一种“包装盒”
(function($){
    // to do things here, I like use this way
})(jQuery);

//第二种“包装盒”
(function(window, undefined){
    // this is the wrapper of jquery
})(window);

//第三种“包装盒”
(function($, undefined){
    // this is the wrapper of jquery ui components
}(jQuery));

```

闭包是个好东西啊，自打初窥门径后，我干什么都喜欢在外面套个闭包，我把这个称为是打包盒，而且这个盒子很神奇，里面看得到外面，但是外面看不到里面。好处很多，比如可以放心大胆地命名变量啊，不用担心污染全局空间，也不用担心被全局空间的其他变量污染，还有像上面片段里，第一种那种写法，可以非常安全地去使用$符号代表的jQuery对象。因为在全局空间里，如果一个页面上引入多个类库的话，$符号很可能代表的不是jQuery对象，而用了第一种写法后，$符号变得很安全了。

翻开jQuery和其各类插件的源代码，你会发现，它们都被安放在一些“打包盒”里面，不禁有种英雄所见略同的感觉，但是不要感觉太好，为什么人家用的，跟我用的不太一样呢？看第二种，是jQuery用的“打包盒”。乍看跟第一种很像，但是那两个形参，简直匪夷所思。第一个是window，这明显是地球人都知道的全局变量啊，第二个是undefined，这更加神了@#$%^&。[淘宝UED](http://ued.alipay.com/wd/2010/05/17/using-window-and-undefined-as-parameter-in-closure/)有篇文章解释了这个问题。文章观点大体是，将window由全局变量变为形参，可以在后期代码最小化时候，通过对局部变量名的替换，来大幅度减小代码体积，这算是一个优化吧，undefined那个同理。另一点文中提到的是，undefined可以被重新定义成自定义的值，也即可能被污染，使用这种方式，会得到真正的一个undefined。当然，我的眼光和专业程度也止于此了，但是我还是觉得，还有可能有一些额外的好处，如果看官童鞋你知道，请不吝赐教。

第三种的话，看过了两种，基本上已经有点差不多全懂了，但是仔细一看，还差那么一点的。$形参，和undefined形参不多解释了。请大家关注那个不同点，就是最后一个闭合小括号的位置，发现了吧，最后闭合小括号，为什么是放在最后面了呢？由此我也发现了一个特性，就是在小括号里面的匿名函数，如果在函数结束的大括号后面，直接跟一对小括号的话，会使那个匿名函数立刻执行。如果离开了外面那对小括号，匿名函数是不能生存的，如果是具名函数呢，在闭合大括号后，跟一对小括号，也无法实现对函数的立即调用，反倒会有语法错误。但是还是来看最关键的那个不同，如下：

```javascript

//写法A
(function($, undefined){
    // this is the wrapper of jquery ui components
}(jQuery)); 

//写法B
(function($, undefined){
    // this is the wrapper of jquery ui components
})(jQuery); //不用找茬了，这行不一样，看“)”的位置

```

这两种“包装盒”到底有何不同？第一种比第二种有什么特别的好处么？