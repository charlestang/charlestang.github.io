---
title: 关于Push Mail的种种
tags: []
id: '350'
categories:
  - - 历史归档
permalink: what-is-push-mail/
date: 2009-06-26 17:59:39
updated: 2025-05-08 02:17:53
---

Push Mail应用，是黑莓手机赖以成名的绝技，非常遗憾的一件事情是，在中国，这项业务是收费服务，而且价格不菲。但是，随着中国移动通信行业的发展，Push Mail的概念日渐火热，其门槛不断降低，再非昔日的高不可攀，最近一段日子，我不禁对这项应用倍感兴趣。

上一篇介绍E63的使用体验的文章中，我已经提到了这个东西。但是，事实上，我对其的了解是非常有限，我只是根据心目中的想象，将我现在享受到的服务，认为是Push Mail。而实际上，通过在互联网反复搜索，我还是没有实现对这项服务的深入了解。感觉国内做这个的有好几家公司，包括著名的尚邮，另外就是一些移动运营商和知名度较低的公司，但是我觉得这些公司里，不乏玩弄概念，欺瞒客户的现象。
<!-- more -->
### 什么是Push Mail？

Post Office Protocol（邮局协议），就是我们常说的POP3，是互联网上广为使用的邮件投递协议。接收邮件时，用户通过客户端，登录邮件服务器，从服务器上检索新邮件，并下载到客户端查看，而发送邮件之时，却是客户端将邮件直接发送到了目标服务器（也即直接发送到了收件人地址所在的邮件服务器）。以上所描述的方式，就是传统的邮件处理方式，也即与Push Mail相对的Polling Mail。

Push Mail真正与Polling Mail不同的，就是在发送邮件之时，邮件不是到达了目标地址所在的服务器就停止的，而是再进一步地被送到了收件人的客户端之中。听起来，这种处理方式的好处是不言而喻的，最重要的优点，就在于实时性非常的高。

既然这种方式是如此的优秀，为什么没有被广为采用呢？事实上，这是一个历史原因。我们都知道，现在互联网的主要使用的协议还是IPv4，这种协议使得IP地址的数量非常有限，并不能满足给接入网络的每个终端一个地址的需求，现在的方案，是大量的桌面终端用户，接入互联网时，动态地分配其一个IP地址，数量较小的服务器，被分配了固定的IP地址。这种方式，暂时性解决了IP地址不够用的问题，但是同时，也使得每个终端无法享有独一无二的IP地址。回到我们的问题上，这样一来，邮件服务器就无法知道，到底要把邮件投递到哪个地址，于是，只能够放在服务器的存储中，等待客户端主动连接上来查看邮件。

说个题外话，随着互联网的发展，同一时间接入互联网的终端和服务器数量日益增加，IPv4这种动态分配的方式，也开始变得捉襟见肘，IP地址成了日益稀缺的资源，于是乎，IPv6应运而生，这种新的IP协议号称可以给地球上的每一粒沙子都非配一个IP地址，可见其地址数量是何等地庞大，等到IPv6全面使用之时，每个个体（我特意没说是人，被人类管理的动物也包含其中）在出生之时，像得到身份证号码一样得到一个IP地址应该是非常正常的事情。届时，Polling Mail这种方式，也该理所应当地退出历史舞台了吧。

### 通过手机实现Push Mail

我们都知道，每一台接入通信网络的手机，都有一个唯一的手机号码，这就使得将邮件直接投递到手机上，成为了可能。事实上，很多文章上也提到了，我们所熟知的彩信，其本质就是一种Push Mail，只不过发信人地址和收信人地址都是手机号码，而非邮件地址。当然，可能的事情办起来也并非如此容易，无线通信网络和互联网是两种不同的网络，要从互联网，将邮件穿透网络发送到无线通信网络中，必然无法避开通信运营商这一关。所以，在手机上实现的Push Mail，必须有无线通信运营商的支持。

中国在这个领域起步较晚，所以，刚开始，这样的业务必然资费高昂，但是资费的下降，眼看着就是必然趋势。

### 我用过的几种手机接收邮件的方案

我用过的使用手机接收邮件的方案非常有限。现在我就放在一起来说说：

**手机浏览器**——手机通过GPRS上网，从Web页面直接收取。这种方式，就和普通的上网收邮件是一码事。想起来了去收一下，你需要承担的费用只是流量费。当然，这个全然没有实时性可言了，就是你自己想起来，收一下而已。属于彻底的Polling Mail方式。

**Gmail客户端**——这是智能手机上的一个应用程序，目前在绝大多数智能手机平台上可用。该程序运行于系统后台，每隔固定的时间，就通过GPRS网络访问Gmail服务器，从服务器上下载新邮件。使用Gmail客户端，你需要负担的费用也只有流量费，当然这个程序一直运行在系统的后台，会使手机的电量迅速地被消耗，这也是你所必须承担的，经常给手机充电。通过这个客户端，基本实现了实施查收邮件，你可以把检索服务器的时间间隔设置成3分钟，甚至更短，几乎就是实时，当然检查服务器越频繁，流量消耗越多，电量消耗也越多。这种方式还是属于Polling Mail。

**尚邮客户端**——尚邮是我在使用了黑莓后才听说的，不知道为什么，尚邮一直吹嘘自己是Push Mail，不过根据我的理解（见上面），至少其免费版本，绝对不是Push Mail。尚邮的免费版本，和Gmail客户端的性质并没有区别。几乎一模一样。甚至根本赶不上Gmail。使用尚邮免费版本，你需要承担的代价和使用Gmail客户端完全相同。区别就是Gmail从来没吹嘘自己是Push Mail，而这个牛皮，尚邮吹了。其原理，从外表上看，也是Polling Mail，如果退出了尚邮客户端，你就无法收到邮件了。所以，你根本无法知道，开着尚邮客户端，邮件到底是被Push过来的，还是客户端自己去刷新出来的（根据Push的原理，尚邮完全没有和手机号码关联，可以推断，邮件肯定不是Push过来的）。当然，尚邮也推出了很多价格不菲的收费服务，也一概说自己是Push Mail，我没有用过，不敢妄加评论他们到底是不是真正的Push Mail，从情感上，我还是相信尚邮没有这么无耻的。

**139邮箱**——139邮箱是中国移动推出的一项业务，我所在的浙江移动，有这项业务，其他地区不详。139邮箱绝大部分功能和普通电子邮箱一样，区别可能就是这款邮箱带有Push Mail业务。我使用的免费版本，带有邮件到达提醒。在邮件到达的第一时间，发送一条手机短信给用户，告知邮件到达。发送的格式有多种版本。有只发送邮件标题的，发送70字标准短信的，发送350字短信的，和发送彩信的几种方式，如果使用彩信的话，基本上就把邮件完整地发送到手机上了。这种方式，不需要在手机后台开任何程序，不会浪费电，而你真的会在邮件到达的第一时间看到邮件的内容。根据我的理解，这个就是Push Mail了。因为是直接抵达客户端的，而不是你主动去收取的。这个邮箱还带有两个收费服务，叫做Push Mail5元版和20元版，区别是邮箱容量和附件大小。不过收费服务也需要安装客户端软件，我没有用过，不过在网上看到有人用，说是就算不启动客户端软件，还是可以收到邮件。真要是这样，那么邮件也是被Push过来的了。

要是这样的话，就真的意味着在中国，用上Push Mail业务，只要支付每月少于20元的平民价格了，而非黑莓的那个300+的天价。

好，今天就写到这里了，我自己理解的内容，和我自己试用过的方案都在上面了，欢迎纠正我的错误和给我推荐更好的方案。