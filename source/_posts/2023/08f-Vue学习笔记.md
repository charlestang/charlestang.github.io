---
title: 写给程序员的真正 0 基础 Vue 入门
tags:
  - Vue
categories:
  - - 工作相关
date: 2023-08-13 20:57:00
permalink: 2023/vue-notes/
---
学习 Vue 真是十分“困难”的一个过程，作为一个十年以上的老程序员，我这么说，肯定很多人觉得不公平。不过这就是我的真实体验。

网上确实是有很多很多的教程，以及，Vue 确实简单易学，我想说的是，如果你自己完全独立自学，到能做出一个真正完整的应用，中间似乎有一些难以跨越的坎。即便对我这个工作十年以上的老程序员来说都很难。

本文尽量不记录那些普遍能找到的文档视图交给你的东西，比如怎么写这个代码，怎么写那个代码等等，你几乎无法找到怎么实现一个具体东西的代码。我尽量写一些，各种入门文章中都没写的东西。

<!--more-->

## 基础中的基础

这一节治疗一下完美主义者的选择困难症。

我本来是一个 PHP 程序员，一直以来都在做 Web 开发，有比较扎实的编程基础，以前也做过业余前端，不过我了解的都是很古旧的东西，比如 jQuery，比如 BootStrap，没有深入学习过前端工程化的东西，对于 Node 只是听说过，知道是一个高性能的 JS 运行环境。中间放下了跟前端有关的东西很多年。

总结一下就是，有编程基础，了解 Web 的基本原理，了解 HTML，CSS 基础，几乎不了解 Node，前端工程化等等，完全不了解现代的前端框架，比如 react，Vue 等等。

### 包管理器

就好象在 PHP 里用 composer，在 Go 里用 Go Module 一样，在前端范畴里，也有包管理器。有很多，npm/cnpm/pnpm，yarn，等等我只是列举，并不了解。我选择了 npm，Node 安装好后，就自带了这个包管理器。

如果觉得这是一个制约因素，以后可以再专门学习包管理器的课题。坚定自己的想法，盯着一个用就行了。

### Vue2 还是 Vue3

如果你搜中文世界的文档，你会看到巨量的 Vue2 的文档，教程等等。因为企业界使用这个版本实现了大量的应用，未必都来得及切换到新版。

不过学技术就是这样，学新不学旧，毫不犹豫就要决定，选择学习 Vue3。如果你非要学习一下 Vue2，也不是不行，也是为了更好学习 Vue3，才去学习 Vue2，因为有些时候学习 Vue2 有助于更好的理解。

### Javascript 还是 TypeScript

其实，Javascript 的分支，远远不止一个 TypeScript，比如还有什么 ES6，一上来，纠结这些就会弄得自己头昏脑胀，应该快速决定一个即可，因为从长远来说，肯定是都要学习的，只是一个顺序问题。浏览器能原生执行的东西，当然就是 Javascript，但是如果想构建大型项目，并希望编译器给到更多提示，那还是类型严格的 TypeScript 更好，有利于组织巨大的项目。

因为我以前就学习过 Javascript，虽然忘记得差不多了，但是多少知道一点，对我没有新鲜感了，我就选择了学习 TypeScript，算是一条 hard way。但是咨询了资深的前端朋友，选 Javascript 结果没有任何不同，而且更少麻烦，因为不用处理 ts 到 js 的转换问题。怕麻烦的请选择 Javascript 入门，未来再学 TypeScript 也行。


### IDE：Visual Studio Code

就使用 VS Code 作为开发 Vue 应用的开发环境即可，官方文档也这么说，需要安装的插件列表：
 * Volar - Vue Language Features 是 Vue 的语言支持扩展，根据脚手架项目的 Readme 文件内容，使用 Take Over Mode 可以提高性能；
 * Stylelint
 * WindiCSS IntelliSense
 * Prettier - Code formatter 将 Vue 文件，ts 文件等的 formatter 都指向该插件，并且，在 Vue 文件类型里，配置 `editor.formatOnSave`，如不这么配，我自己遇到 save 时候的格式化和 format 的时候格式化竟然是冲突的；
 * Iconify IntelliSense
 * ESLint
 * Auto Close Tag
 * Auto Rename Tag
## Hello World！

通过阅读[官方快速上手](https://cn.vuejs.org/guide/quick-start.html)，运行起一个项目的结构，真是不能再简单了，我只能称赞，Vue 的外围辅助设施和工具链，真是完善！简简单单就直接搭建好了框架，而且能够顺利运行。

然而，就像大多数人学习技术止步于 HelloWorld 一样，我也止步于此了，从这个环节，我看了很多的教程，视频也不少，都是教 Vue 的原理了，比如插值语法，双向绑定，比如单文件组件，选项式和组合式API，看了不少了。还使用[互动式教程](https://cn.vuejs.org/tutorial/)，体验了整套的 Vue 之旅，过程十分愉快！推荐！

然后，我就不知道该怎么办了。

如果你在一个团队里，应该已经有一个 Leader 或者另一个厉害的同事，搭好了一个架子，然后，给你分配一个小需求，你就可以从一个大项目的局部，开始编写代码了。你可以一边从修 bug 这样的小事入手，一边渐渐消化知识，经过一段日子你就可以上手掌握。

如果你像我一个人，而且，你是一个懂得其他技术的开发，你想脱离现有的技术栈和团队，独立学会这个东西，并已经有了一个心目中的项目，想要实现它，然后你发现这太难了，突然变得很迷茫。

## Electron

我们都知道 Vue 其实很适合做 SPA，也就是单页面应用，这其实也意味着，它很适合做桌面应用。Electron 是一个使用 Web 技术制作桌面应用的框架，解决了 Web 技术在桌面的运行环境问题。

如果你不是只想做个网站的话，可以稍微看一下 Electron 的官方入门文档，将一个 Web 应用包装成一个桌面应用，使用 Electron 的话会非常简单。

[这篇文档](https://learnvue.co/articles/vue-and-electron-desktop-apps)介绍了如何手动吧 Vite + Vue3 生成的脚手架和 Electron 结合起来，我照着操作发现很简单。到这一步，我们实现了把前一章的 HelloWorld 转化成了一个桌面应用的办法。

1. 安装 electron，`npm install --save-dev electron`；
2. 修改`vite.config.ts`，将`base`属性修改为`dist`文件夹，作为 electron 启动的根文件夹；
3. 修改`package.json`，增加 `main` 字段，设定为 `main.js`；
4. 从 electron 官网的 Quick Start，抄一个 `main.js` 过来，注意 `index.html` 的路径；
5. 再抄一个 `preload.js` 过来；
6. 如果使用 eslint，注意在 config 文件里 ignore 掉上述两个 js，不然会报错，因为上面两个 js 不是在 web 环境运行的，引用 node 的模块；
7. 在 `package.json` 的 `scripts` 中增加 electron 启动命令；

在尝试 Electron 的时候，我发现 Electron 默认加载 index.html 后，就会停在这里，但是 Web 加载完 index.html 后，会自动访问一下根目录。 原因，是使用
```shell
npm create vue@latest
```
创建的基于 vite 的应用，默认是在 web 环境运行，router 的配置文件里，用的是 `createWebHistory`，但是运行在 electron 环境里的 App，需要使用 `createWebHashHistory`。

如果你只想做一个 Web 网站，那么，就没有必要关注本节提到的内容，因为它只是一个壳子。它提供了一个桌面 App 的脚手架和开始的地方。

## UI 组件

Vue 有很强大的单文件组件的代码复用方式，我们可以把页面上用到的东西，一个一个封装成组件。然后把组件一个个组合成最终的应用。组件出现在不同的页面上，可以复用。

但是我们实际在企业级开发的过程中，一般不会刀耕火种地从纯 HTML 和 CSS 开始，去构建一个最基础的组件，那样的话，简直太累了，本来着手实现一个网站/App 就很难了，还要从 0 开始，就更劝退人了。

多数程序员，都没有什么视觉和交互的才能，你心里的伟大想法，如果自己去构建基础组件，实现出来的东西一定会让自己都觉得鄙视。

所以我们需要找一套现成的 UI 组件来成为我们开始的基础，我们真正要实现的组件，是那些包含了业务规则和特点的业务组件，而不是一个基本的按钮，列表，对话框这类东西。

于是，你就不得不了解一下 Element Plus 这套 UI 组件，这是饿了么公司出品的一套前端 UI 组件。可以跟 Vue 完美地结合。不过这必然不是唯一的一套，只是我们中国人在开发网站的时候喜欢用这套，在网上能搜到海量的文档和信息，所以，可以作为每个人入手的一个基础。

阅读[基础文档](https://element-plus.org/zh-CN/guide/installation.html)，可以学会在项目中引入整套 UI 组件。
```shell
npm install element-plus --save
```
这里有必要仔细看一看 Element Plus 的[指南](https://element-plus.org/zh-CN/guide/design)，很短，却介绍了至关重要的内容，比如如何按需加载框架组件这样的话题。

按需导入功能：

```shell
npm install -D unplugin-vue-components unplugin-auto-import
```

然后，还要修改 `vite.config.ts`，增加相应的配置，[参考这里](https://element-plus.org/zh-CN/guide/quickstart.html#%E6%8C%89%E9%9C%80%E5%AF%BC%E5%85%A5)。
## Vue-Router

现在，你已经通过 Vite 或者 Vue-Cli（已经淘汰了似乎）搭建了一个项目的脚手架，就是上面的 Hello World 已经跑起来了，可以开始做一个 App 了，在这个脚手架上，你去实现一些文档里的简单例子，应该已经毫无阻碍了，但是想要写一个 App，却还不知道如何开始。

第一个需要了解的东西，就是一个 Vue-Router，这是一个重要的官方组件。对于单页面 App 来说，这个组件正是页面内容能够切换的原理。

页面的主要区域，是怎么在不刷新页面的情况下，就实现更新的？本质上，页面的主要区域，就是一个 Vue-Router 里的一个组件叫 RouterView，这个组件根据指令切换自己的内容。指令又是如何发送的呢？通过 RouterLink 组件。

这个组件有比上述深入得多的内涵，需要把比较基础的部分都过一遍，不必追求完全看懂，知道有这么回事，就可以继续推进了。

## 页面布局

现在你要开始真正编写你的 App 了，第一步，你需要引入的组件是页面布局，至少你需要把页面划分成两个部分，一个是导航（Nav），另一个是主要区域（Main Content）。

-- 未完待续 --




