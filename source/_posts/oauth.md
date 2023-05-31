---
title: Oauth
tags:
  - oauth
  - open source
id: '483'
categories:
  - - 工作相关
  - - something-about-daily-work
    - 心得体会
date: 2012-05-24 00:10:14
---

## 什么是OAuth？

简单来说，OAuth就是一种协议。这种协议的作用是，授权第三方使用你在某服务商处储存的私人数据，但是并不需要告诉第三方你的密码。OAuth并不是一个新发明的协议，而是已有的各种解决方案的一个去芜存菁，融合了当时所有解决方案（Google AuthSub, AOL OpenAuth, Yahoo BBAuth, Upcoming API, Flickr API, Amazon Web Services API, 等等）的优点。OAuth协议的研发始于2006年11月，2007年10月3日，OAuth Core 1.0最终草案发布，其1.0版本发布于2007年12月，并迅速成为业界标准，2008年6月修复了一个安全漏洞，发布了OAuth 1.0 Revision A（OAuth 1.0a），2010年4月，OAuth 1.0作为RFC5849发布。

## OAuth与互联网开放

OAuth协议虽说不是一个通过认证的国际标准协议，但是它是事实上的互联网公认的标准。现今，开放已经成为了互联网的主流，而OAuth在其中扮演了不可或缺的角色，可以说OAuth是互联网开放的基石。各种平台服务商，都通过OAuth协议，部分开放了自己的用户数据，使得新兴的互联网服务，可以更加方便地访问到用户在各种网络服务中存储地私人数据，从而更加便利而且快捷地提供更为优质、有针对性地服务。这种用户数据的开放，是建立在安全和授权的基础上的，也即，只有用户亲自授权，其存储于某互联网服务的数据才可以被第三方调用，这种授权可以精确指定，比如用户只希望授权访问自己地照片，但是不可以查看自己照片底下的评论，此外，用户在授权第三方访问自己的私有数据时，不需要告知其自己的密码是什么，这也就保护了用户的密码不备泄漏和篡改。

在以上机制的保障下，任何网络服务，都可以使用OAuth协议，开放用户数据的访问，也可以请求用户访问其位于其他网络服务，如大型平台服务，社区服务提供的数据。在安全保障下的开放与共享，促进了互联网的进一步繁荣。

## 各种知名网络平台、服务提供商采用的OAuth协议

服务商

OAuth版本

文档

Google

OAuth 2.0

[文档](https://developers.google.com/accounts/docs/OAuth2)

Facebook

OAuth 2.0

[文档](http://developers.facebook.com/docs/authentication/)

Twitter

OAuth 1.0a

[文档](https://dev.twitter.com/docs/auth/implementing-sign-twitter)

新浪微博

OAuth 2.0

[文档](http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E)

腾讯微博

OAuth 1.0a

[文档](http://open.t.qq.com/resource.php?i=1,2)

豆瓣

OAuth 1.0a

[文档](http://www.douban.com/service/apidoc/auth)