---
title: 【Yii】CCache接口中add和set的不同语义
tags: []
id: '580'
categories:
  - [工作相关, PHP]
date: 2013-07-20 18:33:46
permalink: the-difference-of-the-add-and-set-in-cache-interface/
---

昨天晚上，我打算自己实现一个使用Redis作为对象存储的模型，并且提供一个类似CActiveRecord的接口，做事情之前，我非常小心的搜索了一遍，基本确定没有人已经实现过我的理念，所以放心大胆开始写了。在开始真正的对象存储模型编写之前，我还是忍不住自己创造轮子，就是用CCache接口封装Redis，开始我没搞懂addValue和setValue有什么区别，就按照我一般使用的经验去实现了，然后今天早上，我在别人的项目YiiRedis里看到了一个RedisCache的实现，发现跟我写得很不一样，主要是一上来没看懂，就觉得人家写错了，还跑twitter上骂了一句，哈哈，太傻逼了。
<!-- more -->
不过关于addValue和setValue，这个问题始终萦绕我的心中最后还是翻回来，重新研究这两个方法的区别在哪里，一看，惊出一身冷汗，原来这两个接口有这么丰富的语义，我都直接错过了。

> set: Stores a value identified by a key into cache. If the cache already contains such a key, the existing value and expiration time will be replaced with the new ones.
> 
> add: Stores a value identified by a key into cache if the cache does not contain this key. Nothing will be done if the cache already contains the key.

原来如此，set的时候，同key的value和expries是要更新的；而在add的时候，key如果已经存在，则直接什么都不做！！！我晕死，我自己的实现可以说根本完全都不对。因为我日常工作中，只用过set的功能，既没有用到add，也对add的语义一无所知，这真是太危险了。

不过上面的描述中，没有说，如果key不存在，set到底怎么表现，是set失败，还是说给创建回来。于是我这回仔细看了下CMemCache的实现和memcache本身的文档，我发现这个跟我本身的理解是一致，如果本身key不存在的话，会被创建出来。

值得一提的是，我又一个发现了以前不知道的东西，就是set接口的expire参数的新含义，根据memcache的原生接口来看，这个时间既可以是绝对时间，也可以是相对时间，如果是相对时间，则时间单位是秒，总数不能超过1个月。然后我在memcache的源代码里找到了依据：

```c

#define REALTIME_MAXDELTA 60*60*24*30
/*
 * given time value that's either unix time or delta from current unix time, return
 * unix time. Use the fact that delta can't exceed one month (and real time value can't
 * be that low).
 */
static rel_time_t realtime(const time_t exptime) {
    /* no. of seconds in 30 days - largest possible delta exptime */

    if (exptime == 0) return 0; /* 0 means never expire */

    if (exptime > REALTIME_MAXDELTA) {
        /* if item expiration is at/before the server started, give it an
           expiration time of 1 second after the server started.
           (because 0 means don't expire).  without this, we'd
           underflow and wrap around to some large value way in the
           future, effectively making items expiring in the past
           really expiring never */
        if (exptime <= process_started)
            return (rel_time_t)1;
        return (rel_time_t)(exptime - process_started);
    } else {
        return (rel_time_t)(exptime + current_time);
    }
}

```

在memcache中，是使用相对时间管理的，current_time是相对时间，服务器启动后，经过的时间。而process_started这个是绝对时间，就是服务器启动的时间点。所以最后无论是给出相对时间还是绝对时间，都会换算成memcache服务进程启动后的时间。

而到底用哪个，分界点，就是30天，小于30天的，就认为传入的是相对时间，大于30天的，认为是绝对时间，但是如果传了个大于30天的相对时间会发生什么？看代码，过期时间会被设置到服务进程启动后1秒，就是说，马上会失效。结局很严重。

要不是我仔细研究文档，还有源代码，我不可能发现这一点，但是在使用框架的时候，我们怎么从来没有这个问题呢，一来30天真的很长，很少有失效期那么长的数据，二来，框架替我们handle了这一切：

```php

0)
$expire+=time();
else
$expire=0;

return $this->useMemcached ? $this->_cache->set($key,$value,$expire) : $this->_cache->set($key,$value,0,$expire);
}

```

以上是Yii框架的CMemcache的实现，这里在调用memcache的时候，只用绝对时间，这样就没有30天的限制。从而不会发生致命的错误，封装了原有memcache接口的复杂度，实现了高度的接口一致性。