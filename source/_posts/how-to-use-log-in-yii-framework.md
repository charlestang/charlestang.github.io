---
title: Yii框架的Log系统的分析
tags:
  - framework
  - source code
  - yii
id: '418'
categories:
  - - something-about-daily-work
    - Yii
    - 心得体会
  - - 工作相关
date: 2011-03-31 01:00:21
---

昨天阅读了Yii框架中log部分的源代码，框架提供了灵活、强大的log功能，如果不是非常特殊的需求，框架中自带的类就已经能够满足一般的应用的需求了。实现log功能的源代码被存放在 framework/logging 目录下，这个目录下的代码都包含在包system.logging中。本文简要介绍一下我昨天阅读代码的所得。
<!-- more -->
[![yii-logging-class-graph-jpg](http://sexywp.com/wp-content/uploads/2011/03/class-graph.jpg)](http://sexywp.com/wp-content/uploads/2011/03/class-graph.jpg)

首先，来看一下这个图，这是Charles昨夜工作的结晶，研究了logging目录下一共九个文件中的类的关系。YiiBase，Yii，CWebApplication不属于logging目录，但是为了说明这些类如何发生作用，也放在了这种图里。我的初衷，是要画一张标准的UML图的，无奈于本科的知识都还给老师了，所以这个图只能算是个四不像，大家凑合看一下，后面我会给自己补补课，后续的文章画得图会趋于规范的。

言归正传，左下角的类CLogger，是在开发过程中，打log时候，真正调用的类，这个类作为所有应用最最基础的组件，被包含在了YiiBase中，任何时候，在代码中调用Yii::getLogger()函数，会得到一个CLogger类的实例，这里用的是一个单件模式（Singleton）。打印log，只要调用其log()方法即可，这个方法有三个参数，第一个是log的内容，第二个是级别（warning，debug，fatal等），第三个category，可以叫类别，也可以视作是一种标识符，可以用于log的过滤。

```php
Yii::getLogger()->log("here is a debug info.", 'debug', 'app.siteController');

```

上面的代码片段给出了一个打印log的范例，任何时候想打log，只要这样写就好。从上面的代码片段中，我们看到，log系统的调用接口是极其简单的。接下来分析一下大家非常关心的，log到底会被怎么处理的问题。

在框架中这个log系统里，负责打log，和负责记录log的是两个对象，他们被很好的解耦合了。CLogger扮演了一个专门生产log的角色，其任务就是将用户使用log()函数记录的log放到一个数组里，可以认为是一个内存buffer，长度可配置。在buffer满了的时候，会激发flush（如果配置了autoFlush）的话，flush就是冲掉的意思，如果内存buffer满了，则清空之，继续接受log信息。在清空log buffer之前，这个类对象会触发一个事件，就是onFlush事件，后续其他的类hook到这个onFlush事件上，就可以在log信息被清空之前，有所动作了。

```php
public function log($message,$level='info',$category='application')
{//$this->_logs就是一个数组，也即存放log信息的内存缓冲，默认10000行
    $this->_logs[]=array($message,$level,$category,microtime(true));
    $this->_logCount++;
    if($this->autoFlush>0 && $this->_logCount>=$this->autoFlush)
        $this->flush(); //缓冲满了后，会调用flush
}

public function flush()
{
    $this->onFlush(new CEvent($this)); //激发onFlush事件
    $this->_logs=array(); //清空缓冲
    $this->_logCount=0;
}

```

这是一个生产者与消费者的故事，以上讲述的是生产者的故事。接下来，讲消费者的故事。CLogger已经在内存中生产了log，那么接下来就要来收集，分析，处理这些log，该记录的记录，该抛弃的抛弃，该报警的报警。当然，你可以不给系统提供消费者，那些log产生了，然后消失了，基本不会带来什么负载和泄露，轻轻松松。

log的生产者是系统中必然存在的，但是log的消费者不是，是通过配置文件配置到系统中的，打开位于/protected/config/main.php的配置文件，在components段，我们可以看到关于log组件的配置，如下所示：

```php
'log'=>array(
    'class'=>'CLogRouter',
    'routes'=>array(
        array(
            'class'=>'CFileLogRoute',
            'levels'=>'error, warning',
        ),
        // uncomment the following to show log messages on web pages
        /*
        array(
           'class'=>'CWebLogRoute',
        ),
        */
    ),
),

```

负责采集处理log的真正对象，是一组以Route结尾的类，在上面类图中，位于右上角的那5个类。它们各有个的功能，发邮件的，写文件的，写Db的等等。前面也提了，对于一堆log，可能各自要使用不同的方法处理，比如debug信息抛弃，info信息记录在文件，而fatal信息发邮件给管理员，一个系统中很可能有这样那样的需求。所以，被以组件形式装进应用中的，并不是Route，而是类图中叫CLogRouter的对象。

对log的各种处理方法，都继承自一个叫CLogRoute的抽象类，提供了统一的调用接口，CLogRouter就是这些route的管理者，它主要负责的就是在onFlush事件发生的时候，把CLogger生产的log都接过来，然后，逐一地交付给自己旗下的Route们，分别处理。从上面的配置信息里，我们可以看到，LogRouter管理多少个Route也是通过配置文件配置的，也即route是router所依赖的组件。在具体开发过程中，你可以只配置一个，也可以配置一群。这种行为特征，真的有点像路由，怪不得叫router和route，我猜就这么个解释。

```php
public function collectLogs($event)
{
    $logger=Yii::getLogger();
    foreach($this->_routes as $route)
    {//Router向每个route分发log，请求处理
        if($route->enabled)
            $route->collectLogs($logger,false);
    }
}

public function processLogs($event)
{
    $logger=Yii::getLogger();
    foreach($this->_routes as $route)
    {//Router向每个route分发log，请求处理
        if($route->enabled)
            $route->collectLogs($logger,true);
    }
}

```

在操作实践中，我们完全可以自己继承CLogRoute，实现collectLogs方法，可以开发譬如名为NetLogRoute的类，将log从网络端口上以UDP包或者通过TCP连接形式发送到网络上专门的log服务器中，也可以开发名为MobileLogRoute的类，用来给管理员发送手机报警短信。

上面一直没有介绍到的Filter，其作用其实可以顾名思义，就是在log处理的时候，过滤用的，可以根据前文提到的category参数来过滤，也可以根据log等级类过滤，等等等等。Filter也是通过参数配置的形式被插入到route中的，完全可以创建自己特有的filter通过配置来替换默认filter，可以说，将灵活性发挥到了极致。不过，灵活还是有牺牲的，比如我就觉得，如果一个router下面挂上N个route之后，每个route都采用特定的filter，则会造成同一批log（10000条）被过滤的N遍。所以，比较好的模式，可能还是一个router，下面一个route，然后可以选择用或者不用filter，挂多个虽然理论可行，但是从实际代码来看，可能有一定性能损耗。

好了，终于啰嗦完了，最后问个问题，整个logging系统的这种结构，到底是哪一种设计模式呢？欢迎交流哈～