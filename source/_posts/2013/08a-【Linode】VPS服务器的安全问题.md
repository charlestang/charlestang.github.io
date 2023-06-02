---
title: 【Linode】VPS服务器的安全问题
tags: []
id: '586'
categories:
  - [工作相关, 心得体会]
date: 2013-08-14 23:21:57
permalink: linode-vps-security/
---

因为放在VPS上的博客一直Nginx 502和500，我去看了一下access.log，不看不要紧，一看下一跳。我的博客是个没多少访问量的博客，竟然每秒也能产生数十条的log，而最糟糕的是，这些log，都指向了同一个文件，xmlrpc.php。

这个xmlrpc.php，其实是WordPress博客提供的一种API接口，如果你使用Live Writer或者MarsEdit这类软件，这个xmlrpc.php就是必不可少的一个东西了。其实就是使用xml文件描述的，远程方法调用。频繁地访问这个API，非奸即盗啊！试密码，或者发垃圾评论，或者发垃圾文章，太糟糕了。虽然这么久了，没有被攻破，但是看着总归不爽。

一般方法是将访问的IP都找出来，然后全部iptables禁用掉。如果你不用客户端，直接把xmlrpc禁用掉好了，省得让贼惦记着。

```shell

grep "POST /xmlrpc.php" access.log*  awk '{print $1}'  sort  uniq -c  sort -nr

```

上述命令，用倒序列出所有攻击得IP和攻击次数，对于攻击最多的，直接iptables就好。

然后，以前ishow也谈过的，ssh试密码的问题，可以对auth.log搜索一下“Failed password”这个关键词。我看了，我自己的，是没有的。又看了管理的两台朋友的服务器，都有10万这个量级的攻击次数。我大体想了想，可能因为我一开始习惯性更换了sshd的端口，导致攻击者找不到目标了的关系。所以这个问题，我建议直接更换sshd的端口，很方便。