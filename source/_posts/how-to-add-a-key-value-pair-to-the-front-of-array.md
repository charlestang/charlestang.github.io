---
title: 【How to】【PHP】怎么把一个Key-Value加入到数组的最前面？
tags: []
id: '628'
categories:
  - - something-about-daily-work
    - PHP
date: 2014-06-06 02:44:45
---

我自己想了想，貌似只有很傻的办法呢：

1. 创建一个新的空数组，插好要的数据，然后把原来的数组接在后面，用foreach可以，但是弱爆了，不如用＋。
 

```php

 1, 'b' => 2);
$new = array('c' => 3) + $original;

```

2. 先将原数组 array_reverse 一下，然后用 array_push，然后再 array_reverse，不错，不如第一个效率高。

你们想想看啊？