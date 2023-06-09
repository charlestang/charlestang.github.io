---
title: SVN为什么比git更好
tags:
  - git
  - svn
  - usage
id: '694'
categories:
  - [工作相关, 心得体会]
date: 2015-08-09 20:17:08
permalink: why-svn-is-better-than-git/
---

首先我表明一个根本的立场，**我个人**更喜欢用git，但是，这仅仅是一个个人偏好。当我们需要将一种技术方案带给整个团队的时候，并不是由我们的个人偏好作为主要决定因素，而应该充分去权衡利弊，选择对团队，对公司更有效率的方案。抛开个人立场，理性评估利弊，可能才是我认可的一个资深程序员，或者一个架构师的本分。

我所在的团队，现在选用的技术方案是git作为全公司的版本控制系统，我们一共有差不多20个程序员，使用五种以上的程序设计语言，研发维护四个左右的项目，属于小型创业公司中，研发规模中等偏上的企业。使用git作为版本控制系统，在我加入公司之前，已经是既成事实了，在我听说这一点的时候，我非常高兴，因为我说过，我喜欢git。

上周五，我们公司新来的工程师，在周会上分享git，有个同事挑战道，为什么git比svn更好？这个问题，如果是问我个人的话，我可能会有很多的理由，但是，就像我一贯的思维模式，说服别人的时候，必须给出足够令人信服的原因，不能使用主观因素去说服别人，那样只能引起争论。

对于，“为什么git比svn更好”这个问题，我真的很想给出一个肯定的答案，但是，我在探寻答案的过程中，遇到了困难。于是，我来尝试一下站在反面的立场来给出一份答卷，然后，我们再反过来辩论，于是就有了本文的题目。
<!-- more -->
## SVN到底有什么优点

**广泛的群众基础**。从我开始使用版本控制系统，我用的就已经是SVN了，所以，想要追溯SVN到底从什么时候开始，不得不求助于维基百科，我发现，SVN首个正式版本，可以追溯到2000年，距今已经十五年历史了。在github成为大热门之前，SVN基本处于一统天下的地位。几乎所有的公司都在使用SVN作为内部的版本控制系统，Google Code更是掀起了开源软件的浪潮，一时间，几乎全世界的程序员，都在使用SVN。

我敢说，我们公司目前招聘的程序员，还没有没用过SVN的。这意味着，如果公司使用SVN的话，他们快速上手的概率，是非常高的。现在中国中小企业和创业企业，程序员招聘的困难程度，我不想多阐述——谁负责，谁头疼——如果使用SVN的话，学习版本控制系统用法这种事情，不会成为你脑海里的一个问题。

**优异的跨平台支持** 。年龄大这种事情，并非总是缺点，在跨平台支持这个角度，就会成为优势。十五年来，SVN几乎积累了所有平台上优秀的客户端软件。Windows平台的TortoiseSVN的成功，简直无需赘述，甚至有程序员认为，TortoiseSVN就是SVN本身，一提到小乌龟，每个码农都会心一笑。而且，SVN本身的命令行客户端，就已经非常简洁好用了。跨平台简直毫无任何可以挑剔的地方。

**简单易用**。我个人认为，SVN的易用性是无与伦比的。我刚入职腾讯的第一年，身边的程序员，是把SVN当成云端文件夹用的。整个部门，只有一个版本库，一个项目文件夹，所有的项目代码仍在trunk里面，需要开新项目，就在trunk里加一个文件夹。就算SVN被误用到这种程度，它依然没有给整个研发过程带来任何大的麻烦，一切都井井有条。你要学会的，就是在小乌龟里点点鼠标而已。

后来，部门逐步扩大，文档增多，为了保护文档不丢失，部门运维自己架设了一个SVN服务器，让所有非程序员成员，都用SVN管理文档，各种需求，设计稿，统统用SVN管理，这个切换过程几乎没花什么时间，就是简单地给一些非技术同事培训了一下，一切都平滑异常。让五、六十号不懂技术的人，一下子用上SVN，足见其简单了吧。

**功能完善稳定**。从过去七年（此时是2015年）的开发经历来看，我还没遇到过什么SVN不能处理的研发管理模型。特指在中国，公司制的研发团队管理场景下。SVN本身建议的研发流程模型，已经足足够够了，trunk用于代码主干，branches用于特性开发，tag用于发布快照，一切都流畅自然。

我所在的团队，经过几年的摸索和磨合，已经形成了非常流畅顺滑的研发流程。有新任务来了，开分支，天天早上第一件事，同步主干变更（sync trunk），任务完成后，分支测试，测试完毕后回归主干（reintegration），完毕后集成测试，测试通过后，打tag，然后用内部自研上线系统，tag全量代码发布，最后分支负责人删除掉用过的分支。尤其配合SVN 1.5以后出现的merge tracking功能特性，连冲突都是很偶然的事件了。

SVN经过15年左右的研发，功能异常完善，而且非常稳定，你熟知的命令和参数，就几乎一直保持着你熟知的那个状态，没有附加学习成本，最难能可贵的是，SVN一直在持续更新，改善效率。

## git 相对SVN来说，有什么缺点？

**高昂的学习成本**。不要睁着眼睛跟我说，git学习很简单啊，“学习很简单”这一个主观感受，也即，你觉得简单，只能代表你一个人的感受，如果整个团队只有你一个人，或者你们团队奉行一种精英文化，不是精英不招聘的话，你们所有人，可能都觉得学习git很简单。但是如果是一家刚刚创业的小公司，或者经营数年的中小企业，考虑其本身能从市场上获取到的人才的程度，你不得不考虑他们的接受能力。固然，公司可以花力气去培训，可是培训的时间和代价，本身就构成了“学习成本”。

**拙劣的跨平台支持**。对于Windows，尤其不友好。但是请注意，Windows仍然是世界上使用最广泛的操作系统，我相信，大多数基层程序员也仍然在Windows环境下工作，那么git那近乎故意的Windows不友好，不知道到底是为了什么。无论GitHub做了什么，各种IDE做了什么，在Windows下使用git，其体验仍然是非常间接，而且不方便的。

**糟糕的抽象，复杂的结构**。要想用好git，用户必须理解几个很特殊的东西，一个是分布式的结构，另一个是git存储版本的原理。这对于没空去理解他的人们来说，很不友好，你几乎不能凭着直觉去使用git，那样几乎都会把事情搞得一团糟。另外，公司里非技术的同事，几乎没法使用git工作，比如我们公司的设计师，试图使用git来管理设计稿，并进行协作，实际体验是很糟糕的，他们连新建版本库都不会。还不用提git其实对二进制文件并不怎么友好。

**你可以把事情搞得很糟糕**。git整个系统，给用户提供了极大的自由度，很多操作，我们知道是危险的，但是系统并没有阻止你操作。比如，你可以把任意分支push到任意分支，比如你可以随意删除本地提交历史里的commit，比如你可以把多人共享的分支给rebase掉，你可以干出很多匪夷所思的坏事托乱全团队的速度，你可以惹麻烦，git本身没有提供任何保护机制。

## 一个不是结论的结论

我完全站在SVN的拥泵角度，来阐述上面那些，我会得出这样的结论，SVN在某些场合，真的比git更合适，而我觉得，这个结论，也相对是公允的。如果公司研发成本低，研发团队小，研发人员经验参差，完全应该考虑直接使用SVN，这可能为你们团队后续发展，节省大量的时间。

当然，还有一个要考虑的因素是研发内容的特点和研发流程的特点，是否高频次协作？是否跨公司，跨地域协作？是否海量研发人员参与的开源系统？而就我的经验看，很少有公司的研发团队能跟这些东西搭边，于是SVN理所当然成为更理智的选择。