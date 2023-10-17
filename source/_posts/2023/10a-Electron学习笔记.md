---
title: Electron 学习笔记
date: 2023-10-10 10:36:00
tags:
  - electron
categories: 工作相关
permalink: 2023/electron-notes/
---
最近在学习桌面 App 开发，技术选中了 Electron + Vue3，因为我本身是 Web 开发，虽然是后台开发，但是对 HTML + JS + CSS 的技术栈有所了解，另外对 Web 的原理了解也比较多，算是有一定基础。

通过阅读 Vue 3 的文档，以及实战演练了一些简单代码，已经渐渐可以上手写一点简单的代码。但是我发现，要实现一款客户端应用，不得不掌握一些 Electron 的知识。好在 Electron 是一个很易学的解决方案或者说框架。

## 什么是 Electron？

> Electron是一个使用JavaScript、HTML和CSS技术构建桌面应用程序的框架。通过将 Chromium 和 NodeJS 嵌入其二进制文件中，Electron允许您维护一个JavaScript代码库，并创建跨平台应用程序，可以在Windows、macOS和Linux上运行，无需本地开发经验。

这是来自官方文档的定义。在 Chrome 内核的帮助下，我们可以很好的实现 Web App，而 Node.js 环境则是实现本地（服务器）应用的优秀环境，将两者结合起来，就可以实现做出客户端 App 的方案，十分巧妙，中间通过 Javascript 这个桥梁。不得不惊叹最初作者的敏锐和巧思。

接下来，我会把一些我在学习使用过程中，非常重要的，但是必须时刻记住的概念，笔记下来，供自己以后查阅。更多的细节，还是需要查阅官方文档。只有官方文档才能更保证紧随最新版本的步伐。

## 基础知识

如果想要用好 Electron，对其基本原理要有所了解。
### 进程模型

![](../../images/2023/10/process-model-of-chrome.png)

Electron 因为包含了 Chromium 在其中，自然也集成了 Chrome 的进程模型。一个 Electron 的应用程序，需要两种进程 main 和 renderer，上图是 Chrome 的进程模型，一个主进程负责管理每个窗口，而每个标签页都是一个独立的进程。

而在 Electron 中有一个 main 进程，相当于 Chrome 的管理进程，而 renderer 进程则加载 Web 技术实现的 UI 界面。

### 基本的应用构成

一个 Electron 应用有至少四个文件构成，每个文件都扮演一个关键角色。
 * `main.js` 是整个程序的入口文件，通过 `package.js` 配置指定，主进程加载后，会构造一个 `BrowserWindow` 的实例对象，来作为加载 UI 界面的浏览器窗口。 在 `main.js` 中开放了 Electron 提供的各种系统 API，以及可以在这里操作 Node.js 的各种模块。
 * `index.html` 作为 Electron 的 Web UI 部分的入口文件。
 * `renderer.js` 通过 `index.html` 引入此文件，这就相当于一个普通网站的 js 文件。
 * `preload.js` 因为 Electron 是 Node 和 Chrome 两种架构的整合，但是两种



-- 未完 --
