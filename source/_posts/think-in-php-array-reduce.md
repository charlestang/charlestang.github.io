---
title: 【Think in PHP】使用array_reduce降维
tags:
  - PHP
  - usage
id: '502'
categories:
  - - something-about-daily-work
    - PHP
  - - 工作相关
date: 2012-08-19 18:34:53
---

PHP里面最强大的工具，就是数组，它融合了多种数据结构的特点，数组、队列、栈、哈希表等等，而且容器可以兼容各种类型，任意嵌套，简直无所不能。围绕着数组，PHP原生支持了一些列的函数，使得数组在实际编程实践中，可以有更强的表达能力和更高的编程效率。但是这要求我们用PHP的方式去思考，尽量使用PHP原生的函数解决问题，而不是掌握了一个foreach就一招鲜吃遍天。
<!-- more -->
本文谈论的就是一个数组函数，array_reduce，我在文章的标题中，使用了“降维”这个词语，因为我联想到了《三体》里面的维度攻击，能把三维变二维，实现毁灭性打击，array_reduce当然不是攻击用的，但是array_reduce可以帮助我们实现降维，将一维数组“降维”成单一字符串。当然，array_reduce的可以但不仅限于实现这个功能，这取决于运用过程中，程序员对问题的抽象能力。

这里讲一种应用场景：从数据库中按照某种条件，取出一组记录，然后按照某种规则，将某个特定字段，拼接成一个单一字符串。举个简单的例子，比如我们常见的联表查询，如果两张表，位于不同的DB，不同的物理机，甚至是通过开放API拉取回来的数据，那么我们可能没法使用简单的联表查询，只能分步骤查询，先查询一个结果集，将结果集主键拼接成IN语句，再到另一个DB去查询结果集。

```php



这是非常常见的一种写法，思路非常自然、直接，也未见什么冗余，但是我觉得，这不是PHP思考问题的方式。PHP的思考方式，是像这样：




我可能没法证明，第二种写法，比第一种写法要高多少效率，减少多少运行时间，但是我更提倡第二种写法，因为第二种写法，是按照PHP的方式在思考问题，提供了更好的语义，
更强的表达，retrieve_ids函数还可以复用在类似的场景里。很多情况下，函数里大段的foreach遍历，都并非为了表达业务本身，而只是为了取得某种中间结果，
而PHP提供了工具，帮助我们避免这种局面，而让自己的代码更加简洁易读。这并非炫耀什么奇技淫巧，这只是PHP自己的正常的方式而已。
```