---
title: Vue 项目脚手架结构介绍
permalink: 2024/the-structure-of-vue-scaffold/
categories:
  - - 技术
    - 前端
tags:
  - vue
  - learning
  - usage
  - notes
date: 2024-02-22 10:58:29
updated: 2025-10-03 02:18:40
---

昨天，撰写了一篇文章，介绍[如何 0 基础入门 Vue](https://blog.charlestang.org/2024/howto-learn-vue-from-zero/)，算是讲清楚了学习 Vue 的路线图，今天，继续来介绍一些具体的东西。

<!--more-->

## 一、开发工具

开发 Vue 的项目，我推荐使用 VS Code，有非常多的插件支持基于 Vue 的开发，感觉社区很庞大，提供的完美的支持。

如果你仔细观察，你会发现在生成的脚手架项目里，会有一个 `.vscode` 的文件夹，里面有个文件叫 `extensions.json` 里面包含了项目脚手架推荐开发者安装的插件：

```json
{
  "recommendations": [
    "Vue.volar",
    "Vue.vscode-typescript-vue-plugin",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

除了上面的，我还有一些推荐的插件，可以帮助你快速打造一个良好的开发环境：

- Auto Close Tag 插入一个组件的 tag，就会自动插入关闭的 tag；
- Auto Rename Tag 修改一个 tag 的名字，就会自动修改配对的那个 tag；
- DotENV 项目使用的环境配置文件，提供了配置文件的语法高亮；
- ESLint 将 eslint 的结果集成到编辑器，可以随时划红线的那种；
- GitHub Copilot Chat 无敌，当你不会写的时候，直接问，能得到答案，收费 10 美元，但是值得，或者像我一样成为开源作者。[HexoPress](https://github.com/charlestang/HexoPress)，请 star 谢谢。
- Iconify IntelliSense 将用到的 Icon 在代码里画出来；
- Material Icon Theme 给 VS Code 的目录树显示文件图标，很好看；
- Prettier，保存的时候代码自动格式化，润物细无声；
- Stylelint，CSS 代码的专业 Lint；
- TypeScript Vue Plugin (Volar)，对 TypeScript 的支持；
- Vue Language Features (Volar)，对 Vue 扩展名的文件，提供良好的支持；
- VSCode Neovim，如果你喜欢用 vim 的话，不能错过这个插件，是我用过最像 vim 的环境了，需要一个真正的 neovim 才能正常工作；
- GitLens，主要是对 Git 的功能的一些支持。

上面列举的单子，也包括了配置文件里的几个。

## 二、版本控制

开启一个项目，第一件事情需要使用版本控制，git。将自己的每个修改都记录下来。在 IDE 里还能展示删除和变更的代码。

项目脚手架已经自动创建了 `.gitignore` 文件，自动忽略一些临时文件以及缓存文件。

## 三、Vue 脚手架

![脚手架](../../images/2024/02/scaffold.png)

上面的图，就是使用 `npm create vue@latest` 命令生成的脚手架，我们来看看这个脚手架的目录结构：

```text
charles@TCMBPM1➜  my-first-vue-app tree --gitignore .
.
├── README.md
├── env.d.ts
├── index.html
├── package.json
├── public
│   └── favicon.ico
├── src
│   ├── App.vue
│   ├── assets
│   ├── components
│   │   ├── HelloWorld.vue
│   │   ├── TheWelcome.vue
│   │   ├── WelcomeItem.vue
│   │   ├── __tests__
│   │   └── icons
│   ├── main.ts
│   ├── router
│   │   └── index.ts
│   ├── stores
│   │   └── counter.ts
│   └── views
│       ├── AboutView.vue
│       └── HomeView.vue
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
├── tsconfig.vitest.json
├── vite.config.ts
├── vitest.config.ts
└── yarn.lock

10 directories, 30 files
```

我们可以看到主要的代码在 `/src` 目录里面。入口文件是 `index.html` 文件，里面会载入 `main.ts` 文件，一个 Vue 的 App 就是从主页，加载脚本后开始运行的。根据我们脚手架的各种选择，这个项目已经安装了 Vue Router，Pinia 状态管理，并示范性的提供了一个状态，就是 `counter.ts`。

从截图里，我们可以看到 `main.ts` 的代码，主要就是创建一个 `App` 组件的实例，然后加载到 `#app` 这个 Dom 节点上，整个程序就算是 run 起来了。

```xml
<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>
```

这个是 `App.vue` 的内容，我省去了 style 部分。这是一个 Vue 里的经典 SFC，单文件组件。这里用到了 Vue Router 的两个组件，也即 `RouterLink` 和 `RouterView`，通过点选两个 Link，可将 `RouterView` 的内容，切换成 Home 组件，或者是 About 组件。这也就是 Vue Router 的原理了。

然后，再逐个去看 Home 和 About 的内容，这两个是两个特殊的组件，称为视图，提供了页面的布局。里面的部分内容又被封装成了更小的独立组件，比如 TheWelcome，HellowWorld。这里展示了 Vue App 的组织形式。也就是鼓励开发者，将自己的功能，按照功能，或者按照页面区域，拆解成小的组件，然后组合成一个大的界面称为 View，供 Router 系统去调用和切换。

小的可以复用的独立功能组件，叫做 Component，大的覆盖整个屏幕的界面组件叫 View。多个组件共享状态，使用 Pinia 组件，在项目里命名为 Store。通过脚手架的学习，可以将在《深度指南》中学习的知识都串起来，组织成一个项目。

## 总结

本文介绍了使用 Vue 脚手架构建的项目框架的结构和各个部分的原理。
