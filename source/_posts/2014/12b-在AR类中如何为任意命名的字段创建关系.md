---
title: 在AR类中如何为任意命名的字段创建关系
tags: []
id: '658'
categories:
  - [工作相关, Yii]
date: 2014-12-23 23:08:24
permalink: how-to-set-arbitry-key-name-in-ar/
---

故事是这样的，在我的业务模型里，有些东西是常态并且固定化的，比如User，这是一个网站的用户，有一张用户表与其对应。但是有些东西，却不是那么常态，比如我们的网站要经常搞活动，搞活动的时候，临时开发一个功能，加一个表来存储活动数据，日后，活动下线了，这个表也就没有用了，可能会被删除。活动频次非常高，所以不同的开发都会快速地进行开发，于是出现了命名不一致的情况，比如大家都是要关联User（活动跟用户有关，非常自然），在表A中，代表用户的字段叫user_id，表示User的主键，但是在表B里面，因为习惯使然，代表用户的字段叫uid，然后问题就产生了，当表A和表B需要联表查询时候，怎么设置这个relations呢？
<!-- more -->
在我碰到的场景里，表A和User是一对一的关系，表B和User是多对一的关系，所以，表A和表B的关系是has many，但是表A的外键不是表B的主键，在Yii框架的CActiveRecord里，要怎么设置表A的model呢？

```php

FK，下面的代码片段
 //是在A的model中，设置relations，表达A has many B的关联
 public function relations() {
 return [
 'user' => [self::BELONGS_TO, 'User', 'user_id'],
 'B' => [self::HAS_MANY, 'BModel', ['uid' => 'user_id']],
 ];
 }

```

问题完美解决，其实上次我也解决过一次，结果没过几天，就忘记了，所以特意来写篇文章记录下。

更多问题即时探讨，请加群：
「Yii框架工程师交流群」[![Yii框架工程师交流群](http://pub.idqqimg.com/wpa/images/group.png "Yii框架工程师交流群")](http://shang.qq.com/wpa/qunwpa?idkey=46ef0e8406816995957cd8d138f378ee233708d79066a5cab3d2803efae44d81)

加群请注明使用年限，使用Yii框架经验1年以下的免加，

鼓励潜水，鼓励探讨问题，问任何问题之前，自己请先给出一个答案，营造良好的讨论环境。

![Yii框架交流群二维码](http://sexywp.com/wp-content/uploads/2014/12/1419348551706.png)