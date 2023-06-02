---
title: 【Yii 1.x】 中 Console 环境下因为 CLogger 导致的「内存泄漏」问题
tags:
  - usage
  - yii
id: '747'
categories:
  - [工作相关, 心得体会]
  - [工作相关, PHP]
  - [工作相关, Yii]
date: 2016-10-16 21:24:59
permalink: yii-1-x-console-clogger-cause-memory-exceed-limit/
---

今天下午，我在 Yii 框架 1.x 下，写一个数据处理脚本，脚本的功能主要是把一个超过百万行的表中的两个字段，同步到一个新表中。按照一般的想法，我写了如下的代码。
<!-- more -->
```php
protected function syncronize()
{
    $maxId = Yii::app()->db1->createCommand("select max(user_id) from user_lifecycle")->queryScalar();
    if ($maxId == null) {
        $maxId = 0;
    }

    $sql    = "select id user_id, create_at register_at from user where id > :max";
    $limit  = 2000;
    $offset = 0;
    do {
        $users = Yii::app()->db2->createCommand($sql . " limit $offset, $limit")->queryAll(true, ['max' => $maxId]);
        if (!empty($users)) {
            $this->insertIntoUserLifecycle($users);
        }
        $offset += $limit;
    } while (!empty($users));
}
```

因为表的总数据量超过百万，所以，这个代码片段，以 2000 行数据为一个批次，分次将数据插入到新表中。原以为顺利完成任务的，结果在 Console 环境下一执行，发现总是到了 696000 行数据的时候，脚本就自动退出了，而命令行环境基本没有报错，按照我一般的经验，这个脚本自动退出又没有报错的原因，基本就是因为内存使用超限，于是，我加了一些内存统计代码来验证这个事情。

```php
protected function syncronize()
{
    $maxId = Yii::app()->db1->createCommand("select max(user_id) from user_lifecycle")->queryScalar();
    if ($maxId == null) {
        $maxId = 0;
    }

    $sql    = "select id user_id, create_at register_at from user where id > :max";
    $limit  = 2000;
    $offset = 0;
    echo 'offset, memory', PHP_EOL;
    do {
        $users = Yii::app()->db2->createCommand($sql . " limit $offset, $limit")->queryAll(true, ['max' => $maxId]);
        if ($offset % 20000 == 0) {
            echo $offset, ',', memory_get_usage(), PHP_EOL;
        }
        if (!empty($users)) {
            $this->insertIntoUserLifecycle($users);
        }
        $offset += $limit;
    } while (!empty($users));
}
```

执行后，数据结果如下：

```generic
offset,memory
20000 ,2401632
40000 ,5941896
60000 ,9539432
80000 ,13132872
100000,16726312
120000,20327944
140000,23921384
160000,27514824
180000,31108264
200000,34718088
220000,38311528
240000,41904968
260000,45498408
280000,49091848
300000,52685288
320000,56278728
340000,59872168
360000,63498376
380000,67091816
400000,70685256
...

```

可以看到，基本上，每次循环里查询完毕，内存占用线性增加。而且，仅执行了一句框架的代码，我心想，这下坏了，框架里面内存泄漏了，这可是不好解决啊。但是不甘心啊，好想找到内存泄漏的点，所以，我决定深入进去研究，第一步当然是看 log，但是执行过一遍脚本，发现 log里面竟然是空的，我这才想起来，如果程序异常退出，那么是没有来得及打 log的，必须在每个循环里主动 flush，才有可能看到崩溃前的 log。于是，我加了一行代码：

```php
protected function syncronize()
{
    $maxId = Yii::app()->db1->createCommand("select max(user_id) from user_lifecycle")->queryScalar();
    if ($maxId == null) {
        $maxId = 0;
    }

    $sql    = "select id user_id, create_at register_at from user where id > :max";
    $limit  = 2000;
    $offset = 0;
    echo 'offset, memory', PHP_EOL;
    do {
        $users = Yii::app()->db2->createCommand($sql . " limit $offset, $limit")->queryAll(true, ['max' => $maxId]);
        if ($offset % 20000 == 0) {
            echo $offset, ',', memory_get_usage(), PHP_EOL;
            Yii::getLogger()->flush(true);
        }
        if (!empty($users)) {
            $this->insertIntoUserLifecycle($users);
        }
        $offset += $limit;
    } while (!empty($users));
}
```

然后开始执行代码，然后出现了我目瞪口呆的现象：

```generic
offset,memory
20000 ,2402499
40000 ,2402499
60000 ,2402499
80000 ,2402499
100000,2402499
...

```

咦？内存竟然不泄漏了！！！误打误撞下，我恐怕直达了内存泄漏的真相。显然是 logging 包里的代码导致的。又打开看了一下 CLogger.php, CLogRouter.php 和 CLogRoute.php 终于确认无疑了，其实，我对这三个文件的代码，不知道看过多少遍了，只是里面一些小细节背后的深刻内涵，并没有掌握透彻，现在看来，恍然大悟啊。

CLogger 作为 Yii 框架的 logging 系统的入口，为了降低磁盘 IO，使用了一个数组，来缓存每一行 log，默认每 10000 行执行一次 dump 操作。而 dump 的时候，则首先通过 CLogRouter 启动每一个 LogRoute 的 collectLogs 操作，如果 dumpLogs 参数为 true，则执行 processLogs 操作。执行 collectLogs 操作的时候，CLogger 的对象内部的缓存数组会被清零一次。这还不算完，LogRoute 的实现，缺省也各有一个缓冲数组的，这样，每个具体的 LogRoute 实现，可以根据需要调整处理的频率。只有在 dumpLogs 参数为 true 的时候，要求每次 collectLogs 时候，也同时强制 processLogs 这样，才能将挂载到系统里的每一个 LogRoute 的缓冲数组清零。设定 dumpLogs 参数的方法，就是上面第 16 行代码，调用 flush() 方法的时候，里面传 true。

至此，所有疑惑解开，其实 Yii 框架的代码质量还是相当靠谱的。当然，logging 用于命令行环境下，这种坑，官方文档里还是应该说清楚，要不是对整个框架的代码高度熟悉，我也不可能这么快搞清楚来龙去脉的，这对新人来说，必然算不上太友好。仔细回忆了下，最多也就 2 年前，我的同事肯定解决过这个问题，也跟我们都分享过，只是不是自己亲手解决的，印象不深，非要自己独立亲历一次，才能印象深刻，不胜唏嘘。

关于这个问题，基本都讲清楚了，看看 log 记录的内容，发现，我这个是 debug 环境，每次会把执行的 SQL 原本打印，所以，每个循环插入 2000 行数据，log 里会把那个插入 2000 行数据的 SQL 给打出来，也即意味着，这些都在缓冲数组里，怪不得一次 autoFlush 还没有触发，就已经耗光了所有默认的 128M 内存。

以上所有的东西记录下来，希望下次遇到类似的问题，能够快速想到问题的关窍点，不要再浪费太多时间。