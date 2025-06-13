---
title: Sass：强大的 CSS 预处理器
permalink: 2025/sass-css-preprocessor/
categories:
  - - 前端开发技术
tags:
  - Sass
  - CSS
date: 2025-06-02 17:03:23
updated: 2025-06-04 23:22:15
---
我认识很多 Web 后端开发程序员，他们多多少少会写一些前端的代码，但是很少例外，大都 **不擅长写 CSS** 样式，我自己也不例外。

后端开发程序员为什么都不擅长写 CSS？我想，因为 **CSS 不是一门编程语言，而是一门设计语言**。而 Sass 的发明，使得写 CSS 变得更像一般的面向对象编程，从而大幅度缩小了后端程序员编写 CSS 的难度。

<!--more-->

## 什么是 Sass

Sass 是 Syntactically Awesome Stylesheets 的缩写，是一个由 Hampton Catlin 设计并由 Natalie Weizenbaum 开发的 CSS 预处理器。它最初（2006）是为与 Ruby 的 Haml 模板引擎配合使用而设计的，目的是通过引入变量、嵌套和函数等功能来简化 CSS 编写，从而减少重复和提高可维护性。

## 解决什么问题

我们都知道，把一个具体的数值，例如 3，写入到代码里，是一种糟糕的做法，叫做“魔法数字”（Magic Number）。魔法数字散落在代码各处，含义不明，修改不便。

CSS 里用到的字体大小，间距，颜色等等属性值，就好像一个个魔法数字，散落在各处。早期的 CSS 里没有变量和常量的概念。

### 使用变量

Sass 则是弥补了 CSS 的不足，允许定义变量。

```scss
$brand-color: #fc3;
a {
  color: $brand-color;
}
nav {     
  background-color: $brand-color;
}
```

这样，需要修改颜色值的时候，只要修改 `$brand-color` 的值，就可以没有遗漏和错误地修改全局的颜色。

CSS 3 开始，已经支持了自定义属性的概念（2017），但是与 Sass 的变量略有不同。使用 `--` 前缀的自定义属性名，配合使用 `var()` 函数，总算是弥补了 CSS 没有变量的困扰。只是从标准到普及落地，比 Sass 晚了近 10 年[^1]。


### 嵌套展开

CSS 的选择器，可以使用节点在 Dom 树的路径来定位样式作用域，于是，我们写出了这样的代码：

```css
#header ul li .first {
  padding-left: 0;
}
#header ul li .second {
  padding-left: 20px;
}
```

不难看出来，这冗余了。Sass 的另一个便利，就是提供了嵌套式的写法。

```scss
#header {
  .first {
    padding-left: 0;
  }
  .second {
    padding-left: 20px;
  }
}
```

可以看到，这种语法结构便利，为编写代码节省了大量的时间。

CSS 3 的最新规范，也已经支持了嵌套特性。可以说，就是将 Sass 的特性官方化了，也就是 2023 年才开始普及[^2]，现在覆盖率也就 90% 左右[^3]。

### 模块化管理

可以将 CSS 文件，按照功能模块，拆成更小的文件，例如 `_reset.sass` 文件。然后使用的时候，只要写上：

```scss
@import 'reset'
```

就可以将模块引入进来。就好像一般的编程语言一样。

CSS 3 的最新规范也支持了这个特性，在 2010 年左右普及，比 Sass 晚 4 年。

### 混入 Mixins

这个特性一般就是指整段整段去复用 CSS 代码，比如：

```scss
@mixin border-radius($radius) {
  -webkit-border-radius: $radius;
     -moz-border-radius: $radius;
      -ms-border-radius: $radius;
          border-radius: $radius;
}      
/* Adding our border-radius mixin */
.container {
  @include border-radius(5px);
}
```

上面的代码，写过的都不会陌生，为了解决浏览器兼容性问题，很多时候不得不写大量的浏览器专有前缀，一个是写起来枯燥不说，还很浪费时间，而有了 mixins，再结合上变量，就可以将这种体力活，封装起来，使用的时候，不但简洁，语义也是清晰明了。

这个特性是 CSS 3 规范中也仍然没有的特性。

### 扩展

如果一个已经定义好的样式，你只想修改一点点，那么就可以用这个特性。这个特性的关键字是 `extend`，我觉得可能不方便叫做“继承”，因为 CSS 作为层叠样式表，本来就有继承的特性，指的是样式的继承，如果一个 Dom 节点是另一个节点的子节点，那么天然就会继承父节点的样式。

而扩展，只是对样式定义的微调，所以就称为是扩展。例如：

```scss
.alert {
  border: 1px solid #ddd;
  padding: 1em;
  color: #333;
}
.success {
  @extend .alert;
  border-color: green;
}
.warning {
  @extend .alert;
  border-color: yellow;
}
.danger {
  @extend .alert;
  border-color: red;
}
```

这也是 CSS 3 里还没有的特性。也是提高效率的利器。

### 四则运算

比如，撰写样式的时候，有时候我们需要去定义一个相对的值，比如比 Header 部分高 10px，那么最好的写法，就是用 Header 的高度加上 10px，因为我们并不知道 Header 的高度是多少，尤其是在响应式如此普遍的情况下。

```scss
$base-size: 1em; // ~ 16px
h1 {
  font-size: $base-size + 5em; // 6em
}
h2 {
  font-size: $base-size + 3em; // 4em
}
h3 {
  font-size: $base-size + 2em; // 3em
}
h4 {
  font-size: $base-size; // 1em
}
h5 {
  font-size: $base-size - .2em; // .8em
}
h6 {
  font-size: $base-size - .5em; // .5em
}
```

好在，CSS 3 现在也支持了类似的功能，就是 `calc()` 方法。配合自定义属性，表达能力也十分强大。不过也比 Sass 晚了 6 年以上。

### 插值

Sass 允许在选择器上也使用变量：

```scss
#{headings()} {
  font-family: $raleway;
}
```

会得到：

```css
h1, h2, h3, h4, h5, h6 {
  font-family: "Raleway", sans-serif;
}
```

这个效果其实和编程语言里的宏非常类似，在编译的时候，就实现了宏的展开。

### 条件和循环

Sass 既然是要模拟编程语言，当然也少不了最重要的条件语句和循环语句：

```scss
$padding: 40px;
.box {
  @if($padding <= 20px) {
    padding: $padding;
  } @else {
    padding: $padding / 2; // 20px
  }
}
```

以及循环语句：

```scss
@each $heading, $size in (h1: 3em, h2: 2em, h3: 1.5em, h4: 1em) {
  #{$heading} {
    font-size: $size;
  }
}
```

编译出来是：

```css
h1 {
  font-size: 3em;
}
h2 {
  font-size: 2em;
}
h3 {
  font-size: 1.5em;
}
h4 {
  font-size: 1em;
}
```

## 启示

其实，看到这里，就能明白，Sass 是一个划时代的发明，可能是 CSS 工具链里最成功的预处理器。在将近 20 年前，就已经预见了现在 CSS 3 的多种重要特性，可见其作者的眼光是非常超前的。从很多特性被引入了 CSS 3 中，就可以肯定这一点。

直到今天，我们也不能说 Sass 就已经过时了，没有必要了，它仍然是强大的预处理器，且始终要记得，它是 CSS **预处理器**，发生作用的时间，终究比 CSS 代码提前了一个环节，即便 CSS 3 已经如此强大，但是配合 Sass 只能是如虎添翼，绝非多此一举。

本文撰写，参考了很多的资料。其中引用最多的是《深入了解 Sass 以及你为什么应该使用》[^4]。大量的例子来自此文。

身为一个后端程序员，我虽然听说过 Sass，但是从没有认真去学习过，直到今天才去了解，通过对 Sass 的粗略了解，深刻感受到它背后设计者的强大洞察力。同时，也顺便学习了很多 CSS 知识。

我只能感慨，我看了几十篇，看懂的不到二分之一，能写出来的不到十分之一，学无止境吧。

#### 引用链接

[^1]: https://www.smashingmagazine.com/2017/04/start-using-css-custom-properties/
[^2]: https://caniuse.com/?search=css%20nesting
[^3]: https://www.cnblogs.com/coco1s/p/17692866.html
[^4]: https://medium.com/the-web-crunch-publication/a-deeper-look-at-sass-and-why-you-should-be-using-it-e7ec48dcec4c