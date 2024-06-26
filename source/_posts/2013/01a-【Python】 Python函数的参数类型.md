---
title: 【Python】 Python函数的参数类型
tags:
  - PHP
  - python
  - usage
id: '535'
categories:
  - - 工作相关
permalink: python-arguments-type/
date: 2013-01-28 20:46:37
updated: 2024-05-07 21:03:03
---
我是一个 Python 入门级别用户，虽然我一天到晚黑 Python，但是到了用的时候，又不得不用，这真的很悲哀。我讨厌 Python 就因为一个原因，就是其垃圾一样的文档。

这次我被一个绊脚石绊住两次，是因为有点搞不明白 Python 函数的参数。Python 语言的函数参数，到底是用值传递，还是引用传递？其实要思考这个东西，都是从 C++ 带来的一些习惯，虽然我不是一个 C++ 的程序员，但是也是通过学习 C++ 来学习编程的，不可避免地就要带有 C++ 的习惯。在那个语言里，是需要搞清楚这些东西的，编程语言并没有向程序员隐藏这些细节。以至于到了使用动态语言的时候也很容易陷在这种细节里面。

<!-- more -->

在网上搜到了一个人的文章，《[Python 的函数参数传递：传值？引用？](http://blog.csdn.net/winterttr/article/details/2590741)》，文章的排版非常糟糕，让人以为是抄袭来的，当然真相如何我也搞不清楚，看起来像原创的。先不论这个。文章的内容是很好的，帮我搞明白了这个事情，之前一次搞混，我貌似也是用这篇文章搞明白的。

在 Python 这个语言里面，函数的参数是没有修饰符的，所以，其传递参数只有一种形势，就是传值。这篇文章的意义，就在于，它提出了把变量和对象分开看的观点。其实，就是把指针和数据分开看。在 Python 里面，所有的变量都是 C 里面的指针，所以，变量（指针）没有类型，这很好理解，也很好记忆，指针么，都是内存地址而已，长度都一样，类型也都一样，同样这也解释了为什么 Python 明明是强类型语言，但是却不需要变量的类型声明，因为是指针嘛。

然后文章的另一个好处是，抛出了可更改对象和不可更改对象的区别，解释了为什么有些情况下，在函数内部修改形参变量的值会改变实参的值，而有些情况下不会。因为如果变量指向的是不可修改对象，则改变其值时，只是改变了形参的指向，而没有改变实参变量的指向；另一方面，则会直接改变实参的值。

对比一下 PHP 的做法，PHP 显得相当的混乱。如果变量指向的是对象，那么其呈现出和 Python 一致的行为。函数参数传递得相当于一个对象的指针，如果你去修改这个对象，则对象真的会被修改。但是直觉上，一个数组，在 PHP 里面，本质是 Hashtable，却是按照值传递的，也就是不管数组多复杂，如果不加&符号，传递的时候，都会拷贝一遍，这种场景下，其行为又跟 C++ 很像。以前，至少是一致的，要拷贝，都拷贝，现在，这种一致性也被打破了。所以，在使用时候，就不得不区分说，当前这个变量到底指向一个什么类型呢？我是否希望其被拷贝呢？而且，允许使用&符号，把一切都搞混了。整型也变得可以随意通过函数修改其值了。

这种做法，给 PHP 提供了无以伦比的灵活性。同时，又让 PHP 成为一门汇聚了最多垃圾代码的语言。你在 PHP 的世界里，会看到各种编程范型，各种思维模式混杂的代码。尤其是经常看到 C++ 风格的 PHP 和 Java 风格的 PHP，甚至还有 Ruby 风格的 PHP，真是让人崩溃。
