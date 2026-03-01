---
title: 使用 Claude Code 给 HexoPress 增加了一个 Web 模式
permalink: ''
tags: []
date: 2026-02-18 23:05:31
updated: 2026-02-26 09:37:21
---
设计之处，我就是想给自己做一个 HexoPress 的客户端软件，不过，有了几十个 Star 后，我有人提出要 Web 模式，原理上不难做，但是真的好麻烦。直到，我跟 AI 说了这个想法。

<!--more-->

## Electron 原理
Electron 原理
Electron 原理

现在的 HexoPress，原理是在 Main 进程里，我写了两个 Agent，一个专门操作 Hexo 博客的对象，通过加载命令行的 Hexo 对象来实现，叫 HexoAgent，另一个是 **专门** 操作磁盘的文件系统，叫 `FsAgent`，还有一个 _Fastify_ 的 Agent，专门通过内网给渲染进程，也就是 Renderer 提供磁盘图片文件的 Http 协议的渲染。

然后，Main 进程会把这三个 Agent 提供的能力，都用唯一的字符串，注册成了“具名”的 Handler。然后，通过 Electron 的 contextBridge 对象，将 Handler 的唯一名称，暴露成全局对象 site 上的接口，实则通过 ipcRenderer 的进程 invoke 指令和 Main 进程的 ipcMain 进行通信来实现 Electron 前后台的联动。

如果想改成 Web 版，又要怎么做呢？

## 改成 Web 模式的原理


其实，一般的 Electron App 多数是反过来的，先实现 Web 版本，然后再给用户提供 App 版本。但是我这里，恰恰是反的。

我很庆幸，我写 Electron App 最初的时候，就严格恪守 Electron 的最佳开发规范，前后端完全隔绝，用很麻烦的 ipc 通信的方式来实现，现在改造就变得极其简单了。

首先，我需要启动一个 Web Server，这是肯定的，用 Node 就可以简单实现。我在里面，也用单例包含了 HexoAgent 和 FsAgent，这回不用包含 HttpServer 了，因为它本身就是一个 Web Server，就是要解决一个静态文件路由的问题。

Electron 模式给前端提供服务，是通过 IPC 消息的，现在必须通过 HTTP 协议了，所以，得给两个 Agent 包装一层 RESTful 的 API。

在 Browser 那一边，也不能通过 contextBridge 将 site 上的全局方法转发给 ipcRenderer 进程了，而是应该给 site 的全局方法增加一套方法实现，通过调用 HTTP API 来实现和后端的通信，这么改，就可以实现支持 Web 版了。

## 工作量

主要工作量：
- 增加一个
- 再增加一个
- 哈哈哈

1. hah
2. jksjjgdskg
3. lsjdg

```js
console.log("hello, world!");
```



![](images/2023/10/electron-process-model.png)

