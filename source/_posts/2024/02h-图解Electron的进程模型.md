---
title: 图解 Electron 的进程模型
permalink: 2024/image-explain-electron-process-model/
categories:
  - - 工作相关
  - - 工作相关
    - Vue
tags:
  - electron
  - vue
  - usage
date: 2024-02-26 17:58:00
updated: 2024-02-26 18:52:14
---
此前，已经介绍了《如何从 0 开始，创建一个 Electron 的 App》，每个人就有了一个梦开始的地方。如果想实现一个功能丰富的 App，了解一点基础知识，是非常必要的。比如，Electron 的进程模型。

<!--more-->

# 一、简介 Chrome 的进程模型

Chrome 浏览器是多进程的结构，使用一个管理器，来管理多个页面进程，每个页面存在一个沙盒中，如果崩溃了，也不会影响其他的页面。

[插图，Chrome浏览器进程管理模型]

从上图我们看到，每个页面独占一个进程，管理器负责管理所有的页面。这种架构，使得浏览器的稳定性加强，但是资源占用更加庞大，系统架构也更加复杂。

# 二、Eletron 的进程模型

[Eletron的进程模型图]

Electron 的进程模型参考 Chrome，也存在一个管理器进程，即主进程，这是一个系统进程，启动的时候，会首先加载我们项目里的 `main.js` 文件，这个文件的路径，需要在 `package.json` 文件里配置，用 `main` 这个 `key`，告诉 `electron` 启动的时候，去哪个路径找入口文件，显然，入口文件的名字也是可以改的。

```json
{
  "name": "my-electron-app",
  "version": "1.0.0",
  "description": "Hello World!",
  "main": "main.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "Jane Doe",
  "license": "MIT",
  "devDependencies": {
    "electron": "23.1.3"
  }
}
```
上面是一个 `package.json` 的代码范例，注意第 5 行。

这个主进程，暴露给开发者的接口，是一个对象 —— `app`，在上篇系列文章中，我们可以看看 `main.js` 的代码，里面引用的 `app` 对象，就是主进程的句柄。

而 Web 网页，是通过另一个进程加载的，就是 `BrowserWindow`，我们在 `app` 的 `ready` 回调里，创建浏览器窗口对象，并加载我们写好的网站 App，至此完成了一个 Electron 的应用的启动和加载。

```js
const { app, BrowserWindow } = require('electron')

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600
  })

  win.loadFile('index.html')
}

app.whenReady().then(() => {
  createWindow()
})
```

上面是一个 `main.js` 的代码范例，注意 `app` 这个对象，以及倒数第二行，`createWindow()` 的调用时点。`whenReady` 是主进程 `app` 初始化完毕的时点，另外 Electron 还会提供一些其他的事件钩子，比如 `activate` 和 `close` 或者 `window-all-closed` 等等。我们可以给这些钩子注册各自的处理函数，只要确定，这些处理器在被调用时，应该是已经处于可以正确的调用的时候，才不会报错。

不难看出，BrowserWindow 对象的数量，本质上是没有限制的，也就是我们可以用这种方式创建一个多窗口的 App，不过创建一个单窗口的 App，更符合一般简单 App 的习惯。在一个浏览器窗口内，完成所有的功能操作，这本身和 Web 开发里的 SPA 概念很像，也即单页应用。而 Vue 就是非常适合开发单页应用的一种前端框架，所以 Vue 3 和 Electron 可以说是开发桌面 App 的绝配。

# 三、如何在 Eletron App 中使用 Vue 框架

`BrowserWindow` 对象提供一个 API，就是 `laodURL`，在一个窗口创建完毕后，我们可以加载一个 Web App 的首页，其实也就是一个 Vue App 的入口文件，index.html，加载成功后，我们就看到了页面。注意看上面 `main.js` 的第 9 行，这里加载一个 `index.html`，也就是你的 Vue App 的 `index.html`。

在 Eletron App 中，BrowserWindow 也是运行所有 js 代码的地方，因为 index.html 文件里，肯定会用 `<script>` 标签来加载 js，这样就启动了 Vue 的框架代码。Vue 3 的默认的入口文件，也叫 `mian.js` 或者  `main.ts`，如果和 Electron 一起开发的话，我们可以给入口主文件改个名字，叫 `renderer.js` 或者 `renderer.ts`，这样概念就会更清楚，让其他开发者也更能理解你的项目的结构。

在 Electron 中，这个 BrowserWindow 的进程，也叫 `renderer`。其实，从这里不难看出，其实 Vue 实现的 App 的 js 代码，和 main.js 里的 js 代码，本质上运行在两个不同的进程里。这也就是为什么两者的互相调用，需要进行进程中通信的原因。

# 四、衔接者 preload.js

以前的 Electron 的规范不那么严格，我们一般会把 `ipcRenderer` 直接暴露到 Web App 一侧，不过这么做并不安全，如果需要访问主进程的一些资源，还是应该通过 IPC 通信的方式更正规和安全。

方法是通过 `preload.js` 来给 `BrowserWindow` 注入一些预定义的 API，方便从 Web 侧给主进程发送进程间通信。在 `prelaod.js` 里，能够使用的 API 是收到很大的限制的。

什么情况需要进行这种 IPC 通信呢？比如，你作为一个 Web App，你需要访问用户本地的系统资源，比如文件系统，或者其他宿主操作系统的资源，比如剪贴板，系统托盘区，打印机之类的外设。Node.js 的系统进程身份给这种调用提供了方便，但是其开发接口，是通过 API，更像是前后台程序在互相调用。所以前端程序员很适合来开发 Eletron 的 App。

```js
const { contextBridge } = require('electron')

contextBridge.exposeInMainWorld('versions', {
  node: () => process.versions.node,
  chrome: () => process.versions.chrome,
  electron: () => process.versions.electron
  // we can also expose variables, not just functions
})
```

上面是一个 `preload.js` 脚本的范例，里面看起来使用了 `require`，但是这个脚本其实是收到限制的，只有非常有限的 node 模块可以在这里加载，上面使用 `contextBridge` 对象，给浏览器内部的 App，暴露了三个 API，即 `windows.versions.node` 等三个，显示类库版本的接口。实际上我在开发过程中，也是用类似的方法来做到网页和系统的 node 进行通信。实现磁盘文件操作和系统进程服务调用的。

# 总结

本文简介了 Eletron 的各种进程的类型和交互原理，讲清楚了如何将流行的 Web 开发框架嵌入到 Electron 中，并说明了 Web 侧进程和后台 node 如何进行互相调用。更多 Electron + Vue 3 的 App 的操作方法，请参考我的开源项目[HexoPress](https://github.com/charlestang/HexoPress)，这里提到的技术，里面都有用到。大家感兴趣可以看看真实项目是怎么写的，谢谢！如果感到有用，请给我一个免费的👍🏻和小⭐️，谢谢！

