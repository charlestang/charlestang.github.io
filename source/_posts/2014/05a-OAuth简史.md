---
title: OAuth简史
tags:
  - introduction
  - oauth
id: '617'
categories:
  - 工作相关
date: 2014-05-13 21:11:34
permalink: oauth-history/
---

[![OAuth-cartoon](http://sexywp.com/wp-content/uploads/2014/05/OAuth-cartoon-300x267.png)](http://sexywp.com/wp-content/uploads/2014/05/OAuth-cartoon.png)

最早的OAuth诞生于2006年11月，当时，程序猿布莱恩·库克（Blaine Cook）正在实现Twitter的OpenID。与此同时，Ma.gnolia（一个社会化书签服务2005.12.25~2009.1.30）需要一 个解决方案，允许使用OpenID的成员，授权Dashboard Widgets（Mac系统的桌面小挂件）访问它的服务。这样库克、克里斯·梅西纳（Chris Messina）和来自Ma.gnolia的拉里·哈尔夫（Larry Halff）与戴维·雷科尔顿（David Recordon）会面，讨论在Twitter和Ma.gnolia API上使用OpenID进行委托授权。他们的讨论，得出一个结论，没有开放标准完成API访问的委托。
<!-- more -->
2007年4月，成立了OAuth讨论组，这个由实现者组成的小组撰写了一个开放协议的提议草案。来自Google的德维特·克林顿（DeWitt Clinton）获悉OAuth项目后，表示他有兴趣支持这个工作。2007年7月，团队起草了最初的规范。随后，Eran Hammer-Lahav加入团队并协调了许多OAuth的稿件，创建了更为正式的规范。2007年10月3日, OAuth核心1.0最终版草案发布了。这份草案被更新到2007年12月4日，而且得到了广泛的使用。

2008年11月，在明尼阿波利斯举行的互联网工程任务组第73次会议上， 举行了OAuth的BoF（Birds of a Feather）讨论将该协议纳入IETF做进一步的规范化工作。 这个会议参加的人很多，关于正式地授权在IETF设立一个OAuth工作组这一议题得到了广泛的支持。

但是好景不长，该草案提供的方案，存在严重的安全漏洞：[OAuth Security Advisory: 2009.1](http://oauth.net/advisories/2009-1/)，更详细的介绍可以参考：[Explaining the OAuth Session Fixation Attack](http://hueniverse.com/2009/04/explaining-the-oauth-session-fixation-attack/)。紧接着一个修订的版本，就出现了，那就是[OAuth Core 1.0 Revision A](http://oauth.net/core/1.0a/)。这份规范，被更新到2009年6月24日。

2010年4月，OAuth 1.0协议发表为[RFC 5849](http://tools.ietf.org/html/rfc5849)，一个非正式RFC。也就是一个流行最为广泛的版本，Twitter，Facebook，包括后来中国的新浪、腾讯等等，都实现过此版本的OAuth。

OAuth1.0 经过修补发展到了 OAuth 1.0a 版本后，已经没有安全问题了，但是还存在其他的缺点，其中最主要的缺点莫过于两点：

1.  签名逻辑过于复杂，对开发者不够友好；
2.  授权流程太过单一，除了Web应用以外，对桌面、移动应用来说不够友好；

所以，为了弥补这些缺陷，OAuth2.0被开发出来，2012年10月，OAuth2.0 框架发表为 [RFC 6749](http://tools.ietf.org/html/rfc6749) ， Bearer Token的用法发表为 [RFC 6750](http://tools.ietf.org/html/rfc6750)，至此我们目前广泛使用OAuth2.0协议出现了。

**备注**：

Bearer Token：这个词的含义我 查了蛮多，当然也许查得还不够多，我始终没有找到一个比较准确的中译，其意思就是说，其实Access Token有很多品种的，Bearer Token就是其中的一种，也是最简单的一种，另外，也是最简陋的一种，安全性也最差。不过，你仍然可以使用这种Token来校验，估计是为了开发者的便 利，目前各种OAuth实现方，基本都采用了这个Bearer Token。

**参考文献**：

1.  Wikipedia的OAuth词条：http://en.wikipedia.org/wiki/OAuth
2.  OAuth Core 1.0的Specification：http://oauth.net/core/1.0/
3.  OAuth Core 1.0 Revision A：http://oauth.net/core/1.0a/
4.  RFC 6749： http://tools.ietf.org/html/rfc6749
5.  RFC 6750： http://tools.ietf.org/html/rfc6750
6.  The OAuth Bible：https://github.com/Mashape/mashape-oauth/blob/master/FLOWS.md
7.  OAuth那些事儿：http://huoding.com/2010/10/10/8
8.  OAuth的改变：http://huoding.com/2011/11/08/126
9.  OAuth History：http://hueniverse.com/oauth/guide/history/
10.  OAuth 大全：http://hueniverse.com/oauth/