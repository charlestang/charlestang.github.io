---
title: HTML语言中checkbox的行为
tags:
  - advanced topics
  - html
id: '271'
categories:
  - - 工作相关
date: 2008-12-09 23:46:50
---

为了从用户处取得一个yes or no的答案，一般在html表单中，使用checkbox，中文叫做复选框。
<!-- more -->
复选框的写法：

```html



```

表单（form）的method属性一般设定成post，action属性设定为发送数据的目标。

当按下提交按钮后，发送到目标的数据是checkbox的value属性值。发送的条件是checked属性值为checked。如，在上面的代码例子中，如果按下提交按钮，目标会收到$_POST['check1']='yes'。

**checkbox比较奇怪的一点是，如果checked属性值不为"checked"的时候，就什么都不发送了。就像该项不存在一样的。**

这种不对称性其实是很让人不爽的，就是不符合一般的思维条件，体现到代码上，需要额外的一次判断。隐约记得以前看到过的这个问题的处理方法是添加一个同名的hidden域，放置checkbox没有被选中时候的值。

对于上面的例子，写法如下：

```html




```

这样，如果用户选中了check1复选框，发送给目标的值是yes，如果没有选中，目标收到的是no。注意一下这两个表单域放置的顺序，经过实验，我发现，如果同名的话，发送的数据以最后一个为准。