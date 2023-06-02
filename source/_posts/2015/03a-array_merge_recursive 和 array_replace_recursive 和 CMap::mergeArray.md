---
title: array_merge_recursive 和 array_replace_recursive 和 CMap::mergeArray
tags:
  - PHP
  - usage
id: '668'
categories:
  - [工作相关, PHP]
date: 2015-03-04 01:21:42
permalink: array-merge-recursive-和-array-replace-recursive-和-cmapmergearray/
---

学习使用PHP怎么也有7年的时间了，竟然也没有注意到有个函数是array_replace_recursive，之前只知道array_merge_recursive，而且，这两个函数的返回结果，都非常地出人意料，不怎么符合直觉，而使用了Yii框架若干年，竟然也不知道有个CMap::mergeArray()方法，这个方法，如果跟前面两个函数混同起来看，竟然也显得有点离奇。

 

```php

 [
 'apple',
 'orange'
 ],
 'nested' => [
 'A' => 'xx',
 'B' => 'yy'
 ],
 'single' => 1,
];
$b = [
 'fruite' => [
 'penapple',
 ],
 'nested' => [
 'A' => 'zz',
 ],
 'single' => [
 'string'
 ],
];
echo "array_merge_recursive: ", PHP_EOL;
var_export(array_merge_recursive($a, $b));
echo PHP_EOL, "array_replace_recursive: ", PHP_EOL;
var_export(array_replace_recursive($a, $b));
echo PHP_EOL, "CMap::mergeArray: ", PHP_EOL;
var_export(CMap::mergeArray($a, $b));

```

然后，我们来看一下这个用例输出的结果，相当神奇哦~

```php

array_merge_recursive: 
array (
  'fruite' => 
  array (
    0 => 'apple',
    1 => 'orange',
    2 => 'penapple',
  ),
  'nested' => 
  array (
    'A' => 
    array (
      0 => 'xx',
      1 => 'zz',
    ),
    'B' => 'yy',
  ),
  'single' =>                //注意这个东西的处理，简直莫名其妙！
  array (
    0 => 1,
    1 => 'string',
  ),
)
array_replace_recursive: 
array (
  'fruite' => 
  array (
    0 => 'penapple',
    1 => 'orange',
  ),
  'nested' => 
  array (
    'A' => 'zz',
    'B' => 'yy',
  ),
  'single' => 
  array (
    0 => 'string',
  ),
)
CMap::mergeArray: 
array (
  'fruite' =>   //这里选择了array_merge_recursive的行为
  array (
    0 => 'apple',
    1 => 'orange',
    2 => 'penapple',
  ),
  'nested' => 
  array (
    'A' => 'zz',
    'B' => 'yy',
  ),
  'single' =>   //这里却选择了array_replace_recursive的行为
  array (
    0 => 'string',
  ),
)

```

实在是没有心力去把所有的用例想完整，只能随便写几个，从中可以看出来，这些函数的处理规则，不是简单可以说清楚的。

1.  对于包含了字符串键的数组，是逐个键去做merge或者replace的
2.  merge：对于键的值都是纯数组的情况，单纯合并
3.  merge：对于键的值都是非数组的情况，创建数组添加两者作为元素
4.  merge：对于键的值一边是数组，另一边是非数组，结果就匪夷所思了，将数组降维后，按上一条规则处理
5.  相比之下，replace的行为更具被一致性，就是纯替换
6.  CMap::mergeArray 则跟两者的行为都有所不同，我也是跪了

当然，问题绝不止这么几个，只是我懒得想全所有用例而已。