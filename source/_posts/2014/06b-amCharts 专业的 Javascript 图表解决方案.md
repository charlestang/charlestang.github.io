---
title: amCharts 专业的 Javascript 图表解决方案
tags: []
id: '627'
categories:
  - [工作相关, javascript]
date: 2014-06-02 02:38:15
permalink: amcharts-professional-js-charts-solution/
---

amCharts 是一款高级图表库，致力于 Web 之上的数据可视化支持。它支持的图表包括柱状图、条状图、线图、蜡烛图、饼图、雷达、极坐标图、散点图，甚至连燃烧图、金字塔图，都有支持。amCharts 库是一款完全独立的类库，不依赖任何其他第三方类库，就可以在网站上运行。该类库支持两个版本，商业授权版本和免费版本（在图上显示 amCharts 的商标和链接）。

![amCharts 支持的图表类型列表](https://www.evernote.com/shard/s44/sh/2cdb51c9-6bc5-468b-8957-135eec13b7e8/806a0aebc89de88794fd06a103eab528/deep/0/JavaScript-Charts-and-Maps-Demos---amCharts.png "amCharts 支持的图表类型列表")

amCharts 的使用相对比较简便，初学时候，主要搞清楚类库中一些抽象的概念，那就可以非常快速的上手。在 amCharts 体系中，Chart 是一个大概念，所有种类的图表，都叫 Chart，无非是各种类型的，剩下所有的东西，都在 Chart 的内部，它就是一个终极的容器。所以，要绘制一幅图表的话，首先，就要构造 Chart 对象。

Chart 所表达的数据，是通过一个叫做 dataProvider 的属性传递给 Chart 的，作为整个图表的数据源。有了 Chart 以后，就要在其上进行绘图，每一个图，都是一个 Graph 对象，一个 Chart 能容纳的 Graph 不止一个，所以很多时候，我们可以把多种类型的图，整合在一个 Chart 里面，拼出非常专业的图表。

![](https://www.evernote.com/shard/s44/sh/d03563ae-383d-41ed-8379-7e6342096075/1f73778cc575e398b21b57050c3ce786/deep/0/Stacked-Column-Chart-demo---amCharts.png)

有了图以后，还要有坐标，叫 Axis，在不同的 Chart 中，Axis 的属性略有不同，以上图 SerialChart 为例，缺省是有横纵两个坐标的，纵向的叫 ValueAxis，横向的叫 CategoryAxis，坐标因为是单独的对象，所以，在 Chart 上，也可以包含多组。所以我们需要多个纵轴的时候，就可以往 Chart 里添加多个 ValueAxis 对象，每个纵轴有各自的属性，比如起止，刻度大小，等等皆可自定义。

最后，还有一个的东西，也往往可以充分体现出图的专业性，那就是 Legend，中文叫图例，图例是比较规范的图所必备的要素。也是一个单独的对象，也可以在 Chart 里容纳不止一个。位置也可以随意制定，排列也可以随意指定。提供了最大的灵活性。

除了提供最基本的规范要素外，amCharts 还提供了交互特性，做出来的图表，不是完全静止的，如果鼠标划过，还可以显示一些信息，呈现信息的容器，叫 Balloon，气球，可以在里面显示当前指针指向的数据点的数据明细。除此之外，图表都可以动态动画的形式被绘制出来，尽显高大上。