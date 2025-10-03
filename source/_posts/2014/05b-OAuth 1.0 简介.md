---
title: OAuth 1.0 简介
tags:
  - oauth
id: '619'
categories:
  - - 技术
    - 后端
permalink: oauth-1-intro/
date: 2014-05-14 20:42:38
---

[![OAuth1.0Core](http://blog.charlestang.org/wp-content/uploads/2014/05/OAuth1.0Core.png)](http://blog.charlestang.org/wp-content/uploads/2014/05/OAuth1.0Core.png)

现在已经是OAuth2.0的时代了，整个中国互联网圈子，基本都在使用OAuth2.0了，但是我们可以看到，Twitter，这个曾经引领 了互联网开放平台的先驱，依然固执得坚持着使用OAuth1.0，而且现如今都在使用OAuth2.0的这些中国互联网平台们，也都经历过 OAuth1.0的历史阶段。了解历史才能展望未来，就让我们来看一下什么是OAuth1.0吧~
<!-- more -->
本文的题图，是OAuth1.0的完整流程图。因为是展望历史，我就不打算详细地展开了。只是简要介绍一下所有的要件，想要了解详情的同学，可以参考协议规范文档。

## 角色

OAuth1.0协议中，一共定义了三种关键角色：

*   Service Provider：（服务提供商）允许通过OAuth访问的网络服务、平台、应用等，比如腾讯一般都是扮演这种角色的；
*   User：（用户）在Service Provider那里拥有帐号的人，称为用户，比如QQ用户一般都扮演这个角色；
*   Consumer：（接入者）通过OAuth访问User在Service Provider处存储的受保护的隐私数据的网络服务、应用等；

## 协议要件

OAuth1.0协议中，一共出现了下面这六大协议要件，当然，这是我自己归纳的，未必准确，您姑且一看好了：

1.  Consumer Key：接入者在服务提供商处的唯一标识符，一个字符串；
2.  Consumer Secret：与Consumer Key关联的密码；
3.  Request Token：接入者用于取得用户授权的一个载体，由Service Provider颁发，然后请求用户的授权；
4.  Access Token：接入者访问存储于Service Provider的隐私信息的凭证，可以用经过用户授权的Request Token交换；
5.  Token Secret：与Token关联的一个密码，Request Token和Access Token都有各自与之关联的密码；
6.  Signature：所有授权流程中的关键步骤，都要求签名，签名使用双方约定的算法，可以被验证，这是安全性的来源，因为OAuth1.0是不依赖TLS/SSL的；

## 请求的网址

OAuth 1.0中，Service Provider至少提供三个URL，供接入者来完成授权流程：

*   Request Token URL：发起授权流程，请求颁发Request Token的URL；
*   User Authorization URL：请求用户授权，引导用户登录Service Provider并授权的URL；
*   Access Token URL：使用用户授权后的Request Token交换Access Token的URL；

## 授权流程

用户登录接入者的服务，并发起OAuth授权流程：

1.  接入者向服务提供商申请Request Token；
2.  接入者引导用户到服务提供商处授权请求；
3.  用户授权；
4.  服务提供商将用户重定向回接入者的网站，并带回授权过的Request Token；
5.  接入者使用Request Token向服务提供商交换Access Token；
6.  接入者通过Access Token访问用户在服务提供商处存储的受保护的资源；

### 　步骤1：请求Request Token

请求参数：

*   oauth_consumer_key 接入者标识符
*   oauth_signature_method 签名方法
*   oauth_signature 签名值
*   oauth_timestamp 时间戳，控制时效和顺序
*   oauth_nonce 随机值，唯一值，防止重放攻击
*   oauth_version 必须填1.0
*   其他参数 服务提供商要求的别的一些参数，协议没有规定

请求回包：（HTTP Body）

*   oauth_token 未经授权的Request Token
*   oauth_token_secret 与Request Token相匹配的密码
*   其他参数 其他一些协议没有规定的参数

### 　步骤2：请求用户授权

接入者将用户重定向到服务提供商的User Authorization URL上，带上如下参数：

*   oauth_token
*   oauth_callback:
*   其他参数

### 　步骤3：用户授权

1.  服务提供商应该检查用户的身份，比如要求用户提供用户名和密码；
2.  服务提供商应该说明接下来要发生的事情，比如到底授权什么隐私数据，给具体哪一位接入者；
3.  用户必须主动授权，可以只授权一部分数据，服务提供商有义务保护好没有授权的部分不让接入者访问到；

### 　步骤4：带回授权过后的Request Token

服务提供商通过浏览器的重定向，将用户重定向到步骤2中提供的callback url上。在GET参数中增加oauth_token参数，该参数能显示用户是否授权。

### 　步骤５：获取Access Token

请求参数：

*   oauth_consumer_key
*   oauth_token 经过授权的Request Token
*   oauth_signature_method
*   oauth_signature
*   oauth_timestamp
*   oauth_nonce
*   oauth_version

请求回包：

*   oauth_token 可以用于访问用户数据的Access Token
*   oauth_token_secret 与Access Token匹配的密码
*   其他

### 　步骤6：访问受保护资源

经历了上述五个步骤后，就可以开始调用各种Service Provider提供的API了，调用的时候，除了业务参数外，还要提供如下的参数。

请求参数：

*   oauth_consumer_key
*   oauth_token 步骤5中取回来的Access Token
*   oauth_signature_method
*   oauth_signature
*   oauth_timestamp
*   oauth_nonce
*   oauth_version
*   其他参数

## OAuth 1.0的安全问题

以上介绍的是OAuth 1.0第一个广泛使用的版本，但是这个版本在2009年被爆了漏洞。标准的OAuth授权流程：

[![oauth-flow-normal](http://blog.charlestang.org/wp-content/uploads/2014/05/oauth-flow-normal.png)](http://blog.charlestang.org/wp-content/uploads/2014/05/oauth-flow-normal.png)

攻击者首先登录到接入者的网站中，然后发起OAuth授权流程，这时候，接入者的网站就会去服务提供商处请求Request Token，这个Request Token是未经授权的。到这个环节，这里面并没有任何作假的成分。

然后，这时候接入者应该将攻击者重定向到服务提供商的网站进行授权了，但是这个步骤被攻击者截断了。这时候，攻击者将这个URL（并不难获 得），用某种方法，诱使受害者点击（这也很简单，比如，对受害者说，邀请你体验一下将自己在某服务商处的照片或者别的什么，拿到这里来完成什么什么功 能），这时候，受害者就会点击链接。

受害者，会去到服务提供商的网站上，然后要求他登录，这是没问题的，也会看到说，会授权接入者网站的权限，这也是真的。受害者唯一不知道的是， 一旦授权，攻击者将会借由接入者网站获得Access Token来访问他自己的信息。于是，攻击者利用接入者网站提供的功能，完全访问了受害者授权的在服务提供商处存储的隐私资源。

首先大家要注意的是，在整个过程中，受害者的密码是没有泄漏的，Access Token也没有泄漏，callback也没有被篡改，唯一出问题的就是，攻击者透过接入者网站，访问了受害者的隐私资源。

攻击者攻击时候的流程：

[![oauth-flow-exploit](http://blog.charlestang.org/wp-content/uploads/2014/05/oauth-flow-exploit.png)](http://blog.charlestang.org/wp-content/uploads/2014/05/oauth-flow-exploit.png)

产生这种结果的原因，在于上述提到的几个步骤中，步骤1、2和5三个步骤，是割裂的，没有一个方法帮助接入者或者服务提供商来识别说，这三个步 骤，是同一 个用户触发的，从而给了攻击者可乘之机。这里面还有一个问题，就是步骤2中，协议没有要求签名，所以，在这个步骤中，callback是有可能被篡改的 （在OAuth 2.0中，全面摒弃了签名，导致每个参数都是可以被篡改的，可以增加参数或者减少参数，从而多了更多的可乘之机）。

在上面的图中，值得指出一点，攻击者篡改了Authorization步骤中的callback，导致受害者被重定向到了不知道什么地方去了， 然而，就算这里增加了对callback的校验，攻击者仍然可以实施攻击，只不过，攻击变成了赛跑，其结果完全取决于对于真实callback的访问，谁 的速度比较快，因为重定向是浏览器执行的，所以速度很难超过攻击者，攻击者在这里的问题，就是不知道受害者到底何时完成授权动作，不过这个只要多试几次就 行了，总是可以押对一次的。

## OAuth 1.0a的改进

经过这次安全漏洞事件，OAuth协议发布了修正的版本，包括很多小的错误更正，就是后来的广为使用的OAuth 1.0 Core Revision A，一般称为OAuth 1.0a，也是Twitter至今仍在使用的版本。

这个版本主要做了一些修改：

### 　1. 请求Request Token的时候，需要传递oauth_callback参数；

请求参数：

*   oauth_consumer_key 接入者标识符
*   oauth_signature_method 签名方法
*   oauth_signature 签名值
*   oauth_timestamp 时间戳，控制时效和顺序
*   oauth_nonce 随机值，唯一值，防止重放攻击
*   oauth_version 必须填1.0
*   oauth_callback 必须是一个完整的URL，用于授权完毕后的跳转，如果没有的话，值必须填写为oob（大小写敏感）
*   其他参数 服务提供商要求的别的一些参数，协议没有规定

请求回包：（HTTP Body）

*   oauth_token 未经授权的Request Token
*   oauth_token_secret 与Request Token相匹配的密码
*   oauth_callback_confirmed 服务提供商必须提供这个参数，并且返回True表示已经收到并确认了oauth_callback参数
*   其他参数 其他一些协议没有规定的参数

### 　２. 用户授权完毕的时候，除了带回授权过的Request Token，还增加了验证码

这个步骤原来只有重复了一下oauth_token带回了授权过后的Request Token，现在又加了一个参数oauth_verifier

### 　3. 使用Request Token交换Access Token的时候，要求验证oauth_verifier

## 总结

经过修改后的OAuth 1.0a，主要是在未经签名的授权流程中去除了callback，而是加到了申请Request Token的过程中，这样攻击者一来没法预测callback的值，二来，没法篡改，因为需要签名，第二个变革是在授权的Request Token返回的时候，增加了一个oauth_verifier参数，并且在交换Access Token的时候，进行验证，确保了授权的用户和交换Access Token的用户是同一个人。（注意，因为callback是不可以预测，而且不可以篡改的，所以，攻击者无法从callback上获取到 oauth_verifier，而这个oauh_verifier又是不可以预测的，所以，交换Access Token的时候，向上文叙述的攻击方法，就无法实现了）

经过修补的OAuth 1.0协议，已经成为一个比较完善而且安全的协议了。

## 参考文献：

*   OAuth 1.0 Core:  [http://oauth.net/core/1.0/](http://oauth.net/core/1.0/)
*   OAuth 1.0 Core Revision A:  [http://oauth.net/core/1.0a/](http://oauth.net/core/1.0a/)
*   OAuth Security Advisory: 2009.1:  [http://oauth.net/advisories/2009-1/](http://oauth.net/advisories/2009-1/)
*   Explaining the OAuth Session Fixation Attack:  [http://hueniverse.com/2009/04/23/explaining-the-oauth-session-fixation-attack/](http://hueniverse.com/2009/04/23/explaining-the-oauth-session-fixation-attack/)