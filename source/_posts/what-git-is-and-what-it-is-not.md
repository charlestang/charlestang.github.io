---
title: 【Git】Git是什么？Git不是什么？
tags:
  - git
  - usage
id: '671'
categories:
  - - 工作相关
  - - something-about-daily-work
    - 心得体会
date: 2015-04-14 01:21:30
---

Git是目前世界上最为炙手可热的版本控制系统。它是如此的流行和重要，以至于全世界程序员的工作和生活，都可能因之而改变。

Git是一个版本控制系统，帮助程序员管理自己的源代码的版本变化，保证它们不会丢失。它只是开发工作中的一个工具。但是，一个“工具”，为什么可以重要到足以改变这个“工作”本身？我们可以以政治经济学范畴的概念，来理解一下这个问题，Git就相当于是生产工具，生产工具的发展，可以进一步解放生产力，从而推动了社会的进步。Git不是历史上第一个版本控制工具，显然也不会是最后一个，为什么到了Git出现的时候，就产生了近乎变革般的变化？
<!-- more -->
Git是一个“分布式”版本控制系统，在这一段，我们更强调它的分布式特性。整个系统中，每一个节点，都拥有整个版本库的拷贝，每个节点，都具备全部的信息，整体上是去中心化的。每一个加入到系统的节点，通过克隆其中某个节点的内容，成为一个独立的版本库，并在此基础上可以自行发展，甚至重新以自我为中心，传播和扩散。整个系统的设计，极大地鼓励了拷贝和分化。带给人的感觉，就好像原子弹爆炸的链式反应一样，一个项目，通过使用Git开源，就有可能擦出其他人的火花，一个火花可以擦出更多火花，最后形成代码实现的爆炸式增长。

Git另一些带来变革的原因，我想，首先是社区，从来没有一个开源社区，像GitHub一样，提供了如此良好的氛围，不光是氛围，还有方法，约定，礼貌。这个社区鼓励开源，如果开源，将得到社区运营者免费的代码托管服务。这个社区鼓励创造，为每个项目提供了最显眼的fork功能，以及pull request功能，前者是复制、是索取，后者是改进、是回馈。

除此以外，还有什么？莫非是其创造者Linus个人的精神领袖气质么？这只是个玩笑~

Git不是GitHub，虽然它们密不可分，但是不要将它们混为一谈，很多不明所以的初学者，学习Git的所有知识，可能都来自GitHub，所以，自然而然就把它们混淆了，虽然，这种混淆也不影响大局，但是，搞清楚它们，仍然是有好处的。

Git不是SVN，虽然都是版本控制系统，Git和SVN有着最为本质的不同，前者是分布式的，而后者是集中式的，Git的学习成本，就个人体验来看，远远超过SVN，所以，一时半会儿搞不清楚，绝对是正常的事情，也没必要急躁，切忌的是，不要用SVN去理解Git，那就时常会大错特错。

Git不仅仅是工具，还包括与Git密切相关的方法论，或者说工作流程，它们有很多形式和种类，每一种都有特定的场景，或者适用于特定的团队管理，或者特定项目的开发，甚至，也非常鼓励每个团队发展自己的工作流。

Git不会阻止任何形式的误用和滥用，所以，在这个时候，我们就更强调契约精神和理解其原理的钻研精神。虽然，就这一点来看，是我个人及其讨厌的，但是，如果想让它在团队工作中发挥更大的作用，大家不得不去适应这一点。

最后，你可以批评它，讨厌它，但是我建议，在此之前，你应先学会它。