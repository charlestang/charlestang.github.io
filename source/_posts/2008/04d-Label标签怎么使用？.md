---
title: Label标签怎么使用？
tags:
  - dotNet
  - programming
id: '76'
categories:
  - 工作相关
date: 2008-04-26 16:50:41
permalink: a-problem-with-label/
---

我在写一个类似电视墙一样的软件，就是视频监控管理软件。  
  
在每一个小电视的顶上，我需要显示一条消息，告诉用户当前的状态，比如"no video""recording"等等。我使用了Label控件。结果出现的效果真的让我觉得很"震撼"。当我一屏展示36个画面的时候，首先每个"小电视"是一个个顺序出来的，在应该显示消息的那个位置，显示的是一块黑方块，然后等所有的"小电视"呈现完毕了，那些label才逐一出现在那些黑方块上。  
  
也许是我的编程的水准太低下了，我用的1.8G双核，2G内存，都是这么糟糕的效果，放到客户机器上，真的是给我一种要"毁灭"的感觉。不禁恨自己的水平太臭了，但是我总要学的啊，原谅我一次吧。  
  
我后来想了另一个办法，就是把我要显示的消息都截屏成了图片，然后用一个panel来载入图片的办法显示消息。这样子，虽然"小电视"还是一个个出现，但至少一个"小电视"是完整的，不会像使用label的时候的那个烂样子。  
  
唉，我真的为自己感到"很抱歉"了。想来我是误会了Label的正确用法了，别的地方我也有做得不好的地方。我现在对程序的效率感到很头痛，不知道这些控件在屏幕上的出现是不是也可以使用双缓冲？希望有牛人看到的话给我点指点。  
  
最后发个牢骚，现在市面上的技术书籍都太浮躁了，都是教怎么"ABC"的，没有教"DEF"的，让我觉得非常恶心，想找一本讲C# Windows Form编程的书，根本就没有好的，中文的没有，英文的也没有，唉……