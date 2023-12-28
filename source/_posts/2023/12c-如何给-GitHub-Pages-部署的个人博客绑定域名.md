---
title: 如何给 GitHub Pages 部署的个人博客绑定域名
permalink: 2023/how-to-bind-custom-domain-on-gp/
categories:
  - - 日　　记
tags:
  - GitHub
  - HTTPS
date: 2023-12-28 17:07:30
updated: 2023-12-28 17:29:50
---
今天，我给本博客绑定了自定义域名，其实是一个非常简单的过程。

首先，你需要购买一个域名，如何购买域名这种问题，本文先不介绍。

在你的域名管理的网站，你先要做一个域名指向，使用的是 CNAME 记录。比如，本博客的免费域名是 GitHub 提供的，叫 `charlestang.github.io`。你要做的 CNAME 记录就指向这个地方。比如我选的域名是 blog.charlestang.org，我只要做一个将此域名指向 `charlestang.github.io` 的 CNAME 记录即可。这一步的作用是，让用户访问 blog.charlestang.org 这个域名的时候，实际上跳转到 GitHub Pages 部署的地方。

第二步，就是在 GitHub Pages 所在项目的设置界面 https://github.com/charlestang/charlestang.github.io/settings ，进行配置。打开“Settings”，找到“Pages”标签页，找到“Custom Domain”，填入你要使用的域名，比如本站的域名是“blog.charlestang.org"。

然后点击保存即可。

比较麻烦的是 HTTPS 的部署，因为是 CNAME 直接指向到 GitHub 的，那么接入端的证书配置，显然是在 GitHub 一侧的。不过所幸，这些问题都已经解决了。你要采用一个叫 CAA 的域名验证方案，就可以自动获取到证书并部署了。

GitHub 也是采用 letsencrypt.org 作为免费的域名证书颁发机构的。通过配置域名验证的方案，GitHub 可以自动执行申请域名证书的操作。

CAA 是 Certificate Authority Authorization 的缩写，意思就是证书颁发机构授权。说得很啰嗦，其实操作方式比较简单，相当于也是在 DNS 中配置一条记录信息。而这个记录，既不是我们熟悉的 A 记录，也不是 CNAME 记录，而就是一条 CAA 记录。具体的操作方法，可以参见： https://letsencrypt.org/docs/caa/ 这份文档，甚至，letsencrypt.org 还提供了一个[工具](https://sslmate.com/caa/)来生成 CAA 记录。

最后，我们在 GitHub Pages 项目的 Settings 页面里，可以看到 Enforce HTTPS 复选框旁边就有 GitHub 自动任务的执行结果。等候不多时候，就可以看到 GitHub 已经自动申请了证书并完成了部署，十分流畅。