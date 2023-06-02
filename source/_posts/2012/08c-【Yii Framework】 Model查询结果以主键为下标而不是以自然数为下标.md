---
title: 【Yii Framework】 Model查询结果以主键为下标而不是以自然数为下标
tags: []
id: '498'
categories:
  - [工作相关, PHP]
  - [工作相关, Yii]
  - [小窍门]
date: 2012-08-12 23:32:59
permalink: yii-query-result-custom-indexed-array/
---

使用Yii框架编程的时候，我们会很自然的使用Model来查询我们的DB，并进行相应的操作，有些时候，我们因为性能隐患，而不会使用复杂的数据库关系如多对多关系，遇到此类情况，我们一般会在内存中分批查询数据，用程序遍历，主键关联组装数组，操作。
<!-- more -->
在项目的实践过程中，我至少两次看到了类似如下的代码：

```php

findAll(array('condition'=>'age > 18'));
//将数组转换为用自增id（主键）作为下标的数组
$user_array = array();
foreach ($users as $u) {
 $user_array[$u->id] = $u;
}
……
……

```

如果阅读此文的读者你，也不止一次看到了此种代码，那么说明你的团队里，大家也忽略了Yii框架提供的一种便利。上面的这段代码，意图比较明显，就是先查询出了18岁以上的用户的数组，但是这个数组是自然数下标的，通过一次遍历，将此数组转换成了使用自增id作为下标的数组，这么做的目的，也比较自然，可能是某个多对多关系，需要遍历过程中匹配。

Yii框架使用PDO作为底层数据库操作的接口，其实PDO就有一个功能，使用指定的Unique Column作为下标索引查询结果集的数组。具体的函数是PDOStatement::fetchAll，第一个参数是fetch_style，可以指定PDO::FETCH_COLUMN  PDO::FETCH_GROUP（位与结果）来实现以特定column的值作为结果集索引。Yii框架的DB层，没有忠实将此功能开放出来，但是实现了类似的方法，因为Yii框架DB层，是通过一次遍历来组装结果集的，所以，遍历的时候，就可以顺便把这个事情做了。

```php

populateRecord($attributes,$callAfterFind))!==null)
{
if($index===null)
$records[]=$record;
else
$records[$record->$index]=$record;
}
}
return $records;
}

```

上面引用的函数是CActiveRecord中的函数，该函数用来准备每次查询的结果集，可以看到第三个参数是$index，正是替换了结果数组的索引下标。那么如何来传递这个参数呢，因为上面的函数，不是我们最终调用的接口，只是一个内部使用的接口。我们注意到，每个查询接口，都提供了一个参数，叫$condition，这个参数可以是单纯的条件，也可以是一个DBCriteria的配置数组，也可以是DBCriteria本身，我们可以利用这个参数来传递，设置DBCriteria的index属性，来定制最终的结果集。前文列举的写法，可以简化成如下：

```php

findAll(array('condition'=>'age > 18', 'index'=> 'id'));
……
……

```