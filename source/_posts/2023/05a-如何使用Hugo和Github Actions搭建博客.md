---
title: 如何使用Hugo和Github Actions搭建博客
tags:
  - GitHub
  - Hugo
id: '1234'
categories:
  - [工作相关, 心得体会]
date: 2023-05-26 10:42:46
permalink: howto-build-blog-with-hugo-github-actions/
---

没想到，到了 2023 年的今天，想要找一个能长久免费托管自己个人博客的平台，仍然是一件难事。就在前不久，行业的一位前辈左耳朵耗子逝去，我去他的博客缅怀，发现他的博客托管在 Cloudflare 云计算平台，平台提示，他的博客因为没有续费已经下线。

我不免想到，如果有一天是我，那么我的博客，承载了我在这个世界上公开留下的文字，还能在互联网上存在多久呢？此前我的博客托管在腾讯云服务器上，还比较稳定，较少出现故障等，但是服务器需要人续费维护。后来搬迁到阿里云服务器，比较垃圾，经常会出现故障，还不能自动恢复。而且流量耗光，或者服务器租期到了，我留下的这些内容都会直接下线消失，不复存在。

我想，我需要找一个尽可能长时间免费托管，稳健运行的平台，来备份我的所有博客内容。这样，即使我在相当长一段时间不去维护，不续费，我留下的内容继续存在。所以，我主要的需求，就是一个尽可能免费，稳定运行的平台，托管了博客内容，如果不去维护，也不会出问题。此外，还要满足，撰写方便，发布方便，对开发环境依赖低等等特点。

<!--more-->

Github 是我比较熟悉的平台，也已经稳健存在了多年，对个人用户免费。还有一个原因，就是该平台在开发人员中，有比较好的信用。尊重创作和开源，对作者的创作内容没有太多侵犯性的条款。最后一个点，就是我所掌握的技术能力，可以胜任在这个平台进行操作。而 Github Actions 提供的自动化能力，虽然门槛很高，但是在没有人运维的情况下，业已生成的静态化站点，也不会受到生成功能变更的影响。

可能不是最优的选择，但是值得一试，如果事实证明可行，我也不想再去调研更多的方案了。毕竟人都是懒惰的。下面介绍，如何利用 Hugo 和 Github Actions 来搭建一个博客。

## 1. Hugo[](http://localhost:1313/post/howto-host-a-static-blog-site-with-hugo-and-github-actions/#1-hugo)

Hugo 是一个 Go 语言实现的静态页面生成器，同类产品很多，还有 Jekyll、Hexo 等。选此款有几个原因，一个是在 Github 上的 Star 数量比较多，社区活跃，年头也很长了，比较成熟稳定。另外，学习 Go 语言也一直以来是我的一个计划。当然，这类生成器模式的博客，原理都大同小异，选哪个其实也都无所谓。其实单就个人喜好来说，我见过的几款 Hexo 的皮肤，更符合我的口味一点，而 Hugo 的皮肤往往都不如 Hexo 好看，原因可能是，Hexo 是前端程序员这个群体的制作的产品。

此类生成器，大多是采用某种结构化或者半结构化语言，比如 Markdown，撰写博客的内容，然后用生成器，将其转化为 HTML 静态页面，根据 theme 主题，组织成一个博客网站，然后发布到托管服务器上，供整个互联网查看。

## 2. Github Actions[](http://localhost:1313/post/howto-host-a-static-blog-site-with-hugo-and-github-actions/#2-github-actions)

Github Actions 是 Github 提供的一种自动化工具，可以在 Github 上，通过配置文件，实现一些自动化的功能。比如，当你的代码提交到 Github 仓库时，可以自动触发一些操作，比如自动编译，自动测试，自动部署等等。这里，我们就是利用 Github Actions 的这个特性，来实现自动化编译和部署的功能。

这个功能属于 CI/CD 这个技术范畴内。最大的好处是自动化。可以在平台提供的服务中，完成对代码的编译和发布工作。而因为有了 Github Pages 和 Github Actions 这些功能，用户已经很广泛地采用了它们，作为自己的内容托管平台。这也反过来刺激 Github 对此类用法有了一些预设的模版提供支持，后面会提到。

## 3. Github Pages[](http://localhost:1313/post/howto-host-a-static-blog-site-with-hugo-and-github-actions/#3-github-pages)

Github Pages 是 Github 提供的一个静态页面托管服务。用户可以在 Github 上创建一个仓库，然后将自己的静态页面发布到这个仓库，就可以通过 `https://<username>.github.io/<repository>` 这个地址访问到自己的静态页面了。这个功能，也是 Github 为了方便用户，提供的一个服务。如果你创建的版本库名字是 `<username>.github.io`，那么你的静态页面就可以通过 `https://<username>.github.io` 这个地址访问到了。不需要再提供路径了。

## 4. 实现的步骤[](http://localhost:1313/post/howto-host-a-static-blog-site-with-hugo-and-github-actions/#4-%E5%AE%9E%E7%8E%B0%E7%9A%84%E6%AD%A5%E9%AA%A4)

这个我其实不想展开来写，因为 Hugo 的官方文档写得更好，还能保持持续更新，请访问：[这里](https://gohugo.io/hosting-and-deployment/hosting-on-github/)。

大体上的步骤是，先创建一个名为 `<username>.github.io` 的版本库，然后再本地安装 Hugo，然后利用 `hugo` 命令创建一个新的站点，名字就用 `<username>.github.io`，配置好皮肤和各种属性后，将整个项目推送到 Github 同名项目上。

在项目设置里，启用 Github Pages 和 Github Actions，会自动判断出来你在使用 Hugo，甚至可以给出推荐的配置文件 Workflow，`hugo.yml`，几乎做到了不写一行代码，就能配置成功的地步。体验十分流程。

配置完毕后，你就发现，你每次向版本库推送内容的时候，就会自动生成整个网站并推送给 Github Pages，然后你就可以通过 `https://<username>.github.io` 这个地址访问到你的博客了。

## 5. 结语[](http://localhost:1313/post/howto-host-a-static-blog-site-with-hugo-and-github-actions/#5-%E7%BB%93%E8%AF%AD)

至此，就完成了纯静态的博客解决方案的搭建，可以开始专注于文章的编写了。可能还免不了要学习一些 Markdown 相关的内容，可以更好胜任文章撰写的任务。

## 附录

[Hugo 官方部署指导文档](https://gohugo.io/hosting-and-deployment/hosting-on-github/)

[Hugo 新手指导文档](https://gohugo.io/getting-started/quick-start/)

[V2EX 网友推荐的 Hugo 主题](https://www.v2ex.com/t/828677)