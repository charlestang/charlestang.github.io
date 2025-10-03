---
title: Google用于提高网站质量的工具：Page Speed工具集
tags:
  - add-ons
  - chrome
  - development
  - google
  - tools
  - web
id: '428'
categories:
  - - 技术
    - 前端
permalink: page-speed-family/
date: 2011-05-02 09:17:01
---

应该就是离现在不太远的时候，Google推出了用于提高网页质量的工具集，Page Speed。我最早听说是在若干月前的PHP Classes的news letter上。最近才有时间来仔细看看这个东西。

Page Speed现在的形态是一个工具集，目前提供了客户端和服务器端的两种组件。服务器端提供了Apache服务器的模块mod_pagespeed，该模块可以自动优化网页和资源文件。客户端的工具是一个插件，分别提供了firefox、Chrome的版本，其功能更加类似于Yahoo推出的YSlow，也是真对一个页面进行诊断，给出相应的优化建议，Yahoo提出的东西在业界被称为是14条军规，从Page Speed插件给出的建议来看，基本也没有逃出这14条军规的范畴。除此之外，Google还推出了一个网页版本的Page Speed，只要键入网址，就可以自动分析页面的问题给出建议。

对于没有使用Apache作为Server的，Page Speed还放出了C++ SDK，支持第三方开发。