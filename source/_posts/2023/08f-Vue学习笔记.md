---
title: 写给程序员的真正 0 基础 Vue 入门
tags:
  - Vue
categories:
  - 工作相关
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
 * i18n Ally - [国际化的解决方案](/2023/vue-i18n-solution/)用到的插件，可以在 VS Code 里提供很好的体验；
## Hello World！

通过阅读[官方快速上手](https://cn.vuejs.org/guide/quick-start.html)，运行起一个项目的结构，真是不能再简单了，我只能称赞，Vue 的外围辅助设施和工具链，真是完善！简简单单就直接搭建好了框架，而且能够顺利运行。

```shell
npm create vue@latest
```

然而，就像大多数人学习技术止步于 HelloWorld 一样，我也止步于此了，从这个环节，我看了很多的教程，视频也不少，都是教 Vue 的原理了，比如插值语法，双向绑定，比如单文件组件，选项式和组合式API，看了不少了。还使用[互动式教程](https://cn.vuejs.org/tutorial/)，体验了整套的 Vue 之旅，过程十分愉快！推荐！

然后，我就不知道该怎么办了。

如果你在一个团队里，应该已经有一个 Leader 或者另一个厉害的同事，搭好了一个架子，然后，给你分配一个小需求，你就可以从一个大项目的局部，开始编写代码了。你可以一边从修 bug 这样的小事入手，一边渐渐消化知识，经过一段日子你就可以上手掌握。

如果你像我一个人，而且，你是一个懂得其他技术的开发，你想脱离现有的技术栈和团队，独立学会这个东西，并已经有了一个心目中的项目，想要实现它，然后你发现这太难了，突然变得很迷茫。

## Electron

我们都知道 Vue 其实很适合做 SPA，也就是单页面应用，这其实也意味着，它很适合做桌面应用。Electron 是一个使用 Web 技术制作桌面应用的框架，解决了 Web 技术在桌面的运行环境问题。

如果你不是只想做个网站的话，可以稍微看一下 Electron 的官方入门文档，将一个 Web 应用包装成一个桌面应用，使用 Electron 的话会非常简单。

[这篇文档](https://learnvue.co/articles/vue-and-electron-desktop-apps)介绍了如何手动吧 Vite + Vue3 生成的脚手架和 Electron 结合起来，我照着操作发现很简单。

1. 将`electron`添加到依赖；`npm install -D electron`
2. 设定构建目录到 `dist`，执行构建 `npm run build`；
3. 生成 `index.html`，这是后面要加载到 `electron` 的应用；
4. [创建](https://www.electronjs.org/docs/latest/tutorial/quick-start) `electron` 需要的几个文件 `main.js`，`preload.js`；

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

终于可以开始制作一个 App 的界面了，先有了界面交互的原型，才能逐步叠加功能上去。虽然，根据广为流传的教程，你已经学会了如何做一个局部区域。但是，做一个网站或者一个 App，第一步恰恰不是从那种细枝末节的地方开始，而是先要搭一个架子。

这个环节，你需要掌握一些基本的 CSS 布局知识，怎么利用 div，以及 margin 之类的属性，搭建一个框架，把页面分成 aside，main，header，footer 之类的区域。然后才能逐个区域去开发。

在 element-plus 组件库里，提供了 Container 这个组件，里面有几个元素，可以用来组织页面的结构。可以直接使用。

除了页面框架的问题，可能还有一个就是 layout，这个翻译成中文也叫布局，在我以前学习 Bootstrap 的时候，这个叫 Grid System，就是网格系统，将一块区域，分成 12 份，然后设定宽高来排布页面上的元素。这也算是页面布局的一部分吧，整个页面的布局也可以用这个。不过这个一般都是相对的，将一个区域进行 12 等分。所以想做一个固定的边栏，可能也需要特定的写法。

深入到布局的原理和细节的话，可能内容很多。这里就不展开了。

## 制作原型

现在终于可以一个区域一个区域的小块实现页面的原型了，当然仍然还只是原型，我建议不要一边做原型一边做功能。

当然，你可能没有想好你的原型做成什么样子，这样的话，我建议你一定要，哪怕是，在纸上把原型画出来。否则，你会一边做一边改变主意，在这个过程中，还会被无穷的细节给牵扯，导致很久都做不出来一个合心意的原型。

如果你在做原型的过程中，再结合功能的实现，那就更糟糕了。不管后续还有多少困难，原型只是一个最终界面的模拟和假数据填充。抛开功能后，耦合并不高。这里可以利用各种 SFC 的优势，对界面进行一些切割，也帮助你在实现的过程中，想好页面各部分数据的耦合方式和模块划分。

这个环节，可能是整个流程里，文档和教程最丰富的部分，一般点开一个视频，开始交怎么使用 Vue 的时候，都是讲怎么去做一个 SFC，往往就很适合这个环节。

## 业务逻辑层

到原型可以基本制作这个步骤后，我也陷入了一些迷茫，卡住了很多天，没有想明白怎么继续下去了。虽然说有些东西，在明眼人看来是很简单，理所应当不言自明的，但是就是可以卡住我很久。

当你制作完页面原型，就应该可以开始实现整个 App 的逻辑了。可以先从一些简单的逻辑入手。

我举个例子，比如一个页面是展示一个列表。这个时候，你就需要调用 API 来拉取列表的数据并在页面上进行渲染。在制作原型的时候，你当然已经准备了一个硬编码的数据结构，实现了这个列表了。现在的一步，就是把这个硬编码的假的数据结构，和后台服务提供的真的 API 去对接联调。将后台服务提供的数据接入进来后，可以进一步微调原型。

而如果实现的是一个客户端 App 的时候，如果是从互联网走 HTTP 协议获取数据，那么就没什么不同，也是连接一个服务器。但是，如果不是，而是从本地文件系统载入数据库或者文件之类的应用，则在这个环节要研究如何从本地操作系统中获取数据了。

在 Electron 中，你需要使用 Node.js 进行开发，与本地操作系统或者数据库进行交互，实现相应的接口，然后通过 preload.js 实现 ipc 调用方法，开放给网页端，供页面 UI 进行调用，也是一个实现 API 和 API 联调的过程。这和开发网络类服务无甚不同。

区别只是，如果你是连接某种网络服务，可能是已经事先有人开发好了 API 或者有后台开发同事和你配合，但是如果你像我一样独立开发 App 则需要你自己学习如何给自己开发后台 API，或者在本地操作系统上给自己开发被 ipc 调用的 API。

捅破了这层窗户纸，很多东西就迎刃而解了。

比如，如果你不知道怎么访问本地数据库和本地文件系统，需要补充一些 Node.js 服务器开发的知识，如果你不知道怎么调用网络服务的 API，需要补充一些 Axios 类进行网络访问的知识，这样，就可以在之前工作的基础上，继续向前前进。

## 一些基础但是困难的事情

有些东西是很基础的，但是一点都不好做。

比如，登录。

这是一个超级基础的话题，但是涉及到很多背景知识，以至于让人觉得举步维艰。登录本质上是一个业务，不能说是一个功能，由很多个方面的问题组成。比如，登录本来就涉及到两个问题，身份验证和授权。

验证回答的问题是，你是谁的问题，而授权则回答的是，你可以做什么的问题。如果涉及到这个问题，可以分别搜索去寻找答案。

如果你的 App 是一个网络服务的客户端，你可能需要考虑登录态校验的问题。因为 Web 建立在 HTTP 协议之上，而此协议是无状态的，则意味着每次客户端访问服务器的时候，都是无状态的，就意味着每一次调用服务器的 API，服务器本质上都不知道调用自己的是谁，需要在应用层尝试去恢复之前的会话。这就涉及到登录态如何持久的问题，这个是 HTTP 协议层没有解决的问题。

一般 BS 架构的软件，都是用浏览器实现 UI，采用 cookie session 等技术方案去解决登录态的持久的问题。

那么到了 CS 架构的软件，面临的问题并没有什么不同。在 Electron 中甚至有一个 Chrome，就更是如此，只是在浏览器里，有天然的 cookie 这样的机制，是浏览器提供的，但是到了 Electron 环境，你需要自己决定怎么做，用什么来持久 cookie，或者用别的什么方案，比如 JWT token 之类，那么怎么持久，怎么恢复登录态，都是问题。

另外一些问题，比如，你的整个业务流有一些前置条件要满足，比如我想实现一个 Hexo blog 的客户端，那么客户端启动的时候，需要加载整个 Hexo blog 的目录，作为一个根目录配置。这种如何拦截整个 App 的逻辑流，在最前面进行检查和插入配置的逻辑，涉及到整个 App 启动流程原理，生命周期等等问题。

虽然很基础，很必要，但是并不容易实现，也不容易学懂，如果卡在这个地方，就会阻挠你学习和实现的热情。需要慎重选择介入这类问题研究的时机，避免学习时候半途而废。







## 后续

本文记录到这里，我自己的开发就踏上正轨了，整个流程，我摸索了差不多 2 - 3 个月，当然，我不是全部精力都投在这里精心去学，还有一个原因是我可能真的老了，就是比较慢，温吞。

一个项目发展到这里，基本很多东西也看出来了，明白了。然而，却不能再往下细说了。因为每个领域都是深水区了。在一篇文章里也不方便继续展开了。

那么到了这个环节，进一步学习和项目实践，该干点什么呢？

为了学习 Vue，我给自己找的一个练手小项目是用 Electron + Vue 3 (TS) + Vite 实现一个 Hexo blog 的桌面客户端软件。不得不说，我是“眼大肚小”了，实现过程中发现自己各种基础知识的缺失：

1. NodeJS 的知识；
2. Vue 的知识；
3. Electron 的基础知识；
4. Vite 的基础知识；
5. Hexo 的原理和 API 等知识；

这还不包含各种用到的工具类库和基础类库，比如，Markdown 的编辑和渲染，比如 warehouse，太多了，我简直数都数不完，一方面感叹世间竟有如此之多的类库，另一方面有觉得现代程序员的幸运，做个东西，可以轻松站在无数巨人的肩膀上。

到本文写完的时候，我已经搭建好了一个能在 Electron 环境运行的 Vue 网站的框架，基本实现了载入我自己的 hexo blog 的所有数据。

再往下，要么可以继续打磨客户端的界面，把 UI 做得更加精致一些。要么可以针对某个具体的 UI 界面，开始编写用户交互部分。要么还可以提前研究一下 Electron 实现的 App 到底怎么去打包成一个可以分发的 App。要么还可以研究一下客户端软件付费的视线方式，毕竟要为以后实现自己的“小而美”产品打下基础。

我不知道多久才能打磨好第一个练手的小作品。如果未来我真做出来了，我会更新在本文的末尾。大家可以从项目的提交历史里，部分感受到项目的实现的过程。算是给像我一样的情况程序员，一些指引和帮助吧。

-- End --