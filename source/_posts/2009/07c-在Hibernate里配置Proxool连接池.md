---
title: 在Hibernate里配置Proxool连接池
tags:
  - java
  - programming
id: '352'
categories:
  - 工作相关
date: 2009-07-14 15:22:37
permalink: configure-connection-pool-with-hibernate/
---

在网上搜出了很多给Hibernate配置连接池的文章，不过基本上都是同一篇文章，介绍了3种连接池的配置方法，我先试验了c3p0，感觉不出有什么快的，只是觉得在并发测试中，减少了出错的概率。那篇帖子最底下，说道社区普遍认为c3p0不够优秀，大家更倾向使用proxool，于是乎，我决定也试试，当然，我自己完全是没任何经验的，纯粹是为了试试。

去proxool下载了最新版本，0.9.1（我用的Hibernate是3.2.5版本，实际上0.9.1配置好后，跑步起来，最后还是用了0.8.3，后面会说的），按照网上普遍能搜到的帖子里的那个方法配置。
<!-- more -->
在hibernate.cfg.xml中加入:

```xml
<property name="hibernate.proxool.pool_alias">pool1</property>
<property name="hibernate.proxool.xml">proxoolconf.xml</property>
<property name="hibernate.connection.provider_class">org.hibernate.connection.ProxoolConnectionProvider</property>
```

然后，再在classpath下面放一个proxoolconf.xml的配置文件，里面的内容为：

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- the proxool configuration can be embedded within your own application's.
Anything outside the "proxool" tag is ignored. -->
<something-else-entirely>
    <proxool>
        <alias>pool1</alias>
<!--proxool只能管理由自己产生的连接-->
        <driver-url>jdbc:mysql://localhost:3306/struts?useUnicode=true&characterEncoding=GBK</driver-url>
        <driver-class>org.gjt.mm.mysql.Driver</driver-class>
        <driver-properties>
            <property name="user" value="root"/>
            <property name="password" value="8888"/>
        </driver-properties>
<!-- proxool自动侦察各个连接状态的时间间隔(毫秒),侦察到空闲的连接就马上回收,超时的销毁-->
        <house-keeping-sleep-time>90000</house-keeping-sleep-time>
<!-- 指因未有空闲连接可以分配而在队列中等候的最大请求数,超过这个请求数的用户连接就不会被接受-->
        <maximum-new-connections>20</maximum-new-connections>
<!-- 最少保持的空闲连接数-->
        <prototype-count>5</prototype-count>
<!-- 允许最大连接数,超过了这个连接，再有请求时，就排在队列中等候，最大的等待请求数由maximum-new-connections决定-->
        <maximum-connection-count>100</maximum-connection-count>
<!-- 最小连接数-->
        <minimum-connection-count>10</minimum-connection-count>
    </proxool>
</something-else-entirely> 
```

如果人品好，到这里应该就没有别的事情要做了，就是把proxool-0.9.1.jar放到你的classpath中就OK了，可惜事情偏偏不会那么顺利。

这样子搞，会出现一个错误：

org.hibernate.HibernateException: Proxool Provider unable to load JAXP configurator file: proxool.xml
  
org.logicalcobwebs.proxool.ProxoolException: Parsing failed.

于互联网上疯狂搜索，找了很多的说法，过滤了无数信息，终于发现一个哥们儿说的招儿有效：

**将proxoolconf.xml里面的中文删除即可。**汗死！~~~

以为到这里消停了吧，一启动服务器，又出错了：

java.lang.ClassNotFoundException: org.logicalcobwebs.cglib.proxy.Callback

然后我在proxool的代码里找了半天，竟然没有这个类，到网上搜索依赖的jar包，发现这个类在proxool-0.8.3.jar中才包含，于是乎只好再换过去。

看来，最新的东西是不能用的啊……另外，我以一个实例说明了，使用Java开发项目是多么的麻烦，选用Hibernate作为持久层，你还要考虑配备什么连接池，然后连接池有好多种，每种的性能，使用方法不一样，选定一种后，你还面临着版本兼容问题。这么小一个地方，就出了这么多麻烦，网上甚至看到一个哥们儿，写着，调试了5天了，还没有找到出错原因……唉……