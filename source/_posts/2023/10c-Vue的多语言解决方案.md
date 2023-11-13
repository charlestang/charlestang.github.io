---
title: Vue 的多语言解决方案
tags:
  - Vue
  - i18n
categories:
  - - 工作相关
  - - 工作相关
    - Vue
  - - 工作相关
    - 心得体会
permalink: 2023/vue-i18n-solution/
date: 2023-10-30 15:03:00
---
如果你实现的网站或者 App 的潜在用户不是面向单一地区的，那么你需要考虑到整个系统的多语言解决方案。

常见的多语言解决方案是，使用翻译文件，根据当前系统所在的 locale 信息，加载对应的翻译文件，实现切换界面的语言。

<!--more-->

## Vue i18n

使用 Vue 3 开发应用的时候，我们采用 [Vue i18n 库](https://kazupon.github.io/vue-i18n/)提供解决方案。

这个库的使用方法非常简单。

### 安装

```shell
npm install vue-i18n --save
```
然后，在 Vue 3 的 `main.ts` 中，实例化一个 `I18n` 对象，然后调用 `use`，就可以实现该功能的加载。

```ts
import { createI18n } from 'vue-i18n'
// ... initialized options
const i18n = createI18n(options)
// ... some other init

app.use(i18n)
app.mount('#app')
```

通过上面的代码，可以启用加载语言文件的功能，里面有个关键的 `options` 后面再细说。先接着介绍，怎么在页面上使用翻译字符串。

### 字符串显示

在页面文件中，比如一个叫 `DashboardView.vue` 中，怎么让一个字符串展示成翻译字符串呢？

```vue
<template>
  <p>{{ t('dashboard.hello') }}, world!</p>
</template>
<script lang="ts" setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n
</script>
```

在上面的代码例子中，`dashboard.hello` 是一个翻译字符串的 `key`。通过从类库导入的 `t` 函数，就可以将这个字符串从语言文件中载入到系统。

### options

接下来说一下这个 `options`，语言翻译字符串是怎么载入进去的呢？

就是通过 `options.messages` 这个配置键。

```ts
{
  locale: 'zh-CN', //当前使用的语言类型；
  fallbackLocale: 'en', //加载失败或者找不到靠语言文件，降级的语言类型；
  messages: {
    'en': {
      dashboard: {
        hello: 'Hello'
      }
    },
    'zh-CN': {
      dashboard: {
        hello: '你好'
      }
    }
  }
  //许多其他的选项参数
}
```
从这个配置对象的结构来看，不同语言的字符串就是这个配置对象的一个 `key` 而已，以具体的语言标识符作为 `messages` 键的索引，值则是用名称空间（如：`dashboard`）组织的翻译字符串的 key-value 对。

### 项目实践

在具体项目里，我们可能会每个语言单独放置一个语言文件，比如，在目录 `src/locales` 目录下，放置 `en.ts`，`zh-CN.ts` 等等文件，每个文件代表一种语言，在系统具体启动的时候，我们根据当前系统环境的语言标识，加载对应的翻译文件，以下是一个代码例子：

```ts
import type { App } from 'vue'
import { createI18n } from 'vue-i18n'

export const setupI18n = async (app: App) => {
  //..
  const currentLocale = 'zh-CN' //假设从某系统环境读到当前使用的语言是这个
  const messages = await import(`../../locales/${currentLocale}.yml`)
  
  const options = {
    legacy: false,
    locale: currentLocale,
    fallbackLocale: 'en',
    messages: {
  	  [currentLocale]: messages.default
    },
    sync: true,
    silentFallbackWarn: true
  }
  const i18n = createI18n(options)
  app.use(i18n)
}

// main.ts
//……
setupI18n(app)
//……
```
从上面的代码上，我们看到，系统启动时候，先从环境变量中读取到当前的语言环境标识，然后加载对应的语言文件，初始化 `I18n` 对象，接下来整个应用的界面就可以加载对应的语言包了。

### 日期时间、数字、货币

结合 moment 和 vue-i18n，直接用 i18n 我是一点用不明白的。

## 解决方案

前面讲完了多语言在 Vue 里怎么实现，下面来说说开发时候的解决方案。其实就是要解决，作为一个开发，到底怎么才能更好去维护这个这个多语言的文件。我在网上搜了很多的文章和博客，都没有很好的介绍这个问题。

我在这里分享一个我研究后采用的方案，当然我现在也不知道这么做可能有什么弊端，只是觉得至少在开发阶段，还是很爽的。

### 语言包文件

回顾一下 `options` 那一节，我们看到 `messages` 这个设置的内容是用语言标识做 `key` 的 Plain Object，所以，自然而然，我们可以把一个语言文件命名为 `en.ts` 作为语言文件：
```ts
// en.ts 的内容
export default {
  dashboard: {
    hello: 'Hello'
  }
}
```
在引用的时候，只要 `const content = import('en.ts')` 就可以通过模块的方式，取得这个语言文件的内容。不过，这个方式有个弊端。后面会说。这里只是介绍了如何将不同的语言，拆分成翻译语言包文件。

### IDE 插件

拆分语言包文件，方便我们分离管理，甚至分工合作。但是在编码环境中，要想有比较好的体验，就是使用 IDE 插件。我开发 Vue 是在 VSCode 里面，当成我的主要开发环境。所以有一个插件就不得不说—— i18n Ally，一款非常强大的插件。

这个插件可以将组件代码里的多语言字符串，按照指定的语言翻译出来，这样看起来就舒服多了。

你不会看到代码里的真实情况（一个字符串的`key`），而是将编辑器里，渲染成那个`key`代表的真实字符串。这就非常方便了。

另外，还可以渲染一个面板，可以展示当前语言文件有没有什么正在用的字符串，以及引用的无效的字符串，还可以提醒硬编码的字符串。

另外，如果不同语言版本提供的语言包文件没有全部翻译的话，还能展示每个语言翻译的百分比。

最后，最爽的一个功能，就是如果你凭空写一个 `key`，也即没有任何版本的语言文件，你可以用右键直接在编辑器面板上实现字符串的创建，这就很方便了。完全不用频繁打开语言包文件了。不过，这里就不得不满足一个前提。

### 使用纯文本的配置

在[语言包文件](#语言包文件) 这个章节，我们提到过，用 ts 文件以对象的形式来保存语言包文件，有一个弊端，就出现在这里。如果我想用 i18n Ally 的辅助编辑语言文件的功能，那么要求，被编辑的语言包文件不能是 `js` 或者 `ts` 格式。原因是编程语言动态性太强，无法实现编辑[issue #365](https://github.com/lokalise/i18n-ally/issues/365)。

这个问题，也是很多介绍 i18n Ally 和国际化问题的文章，都没有提到过的一点。如果你想在这个地方，用 IDE 得到更好的体验，你就要用 yaml 或者 json 文件来作为语言包文件，这样 IDE 可以通过插件来实现编辑和维护，更好的提高效率。

于是，很自然，我决定用 YAML 作为语言包文件的格式，无非是使用的时候，要将 YAML 文件转换成一个 JS Plain Object，只是我没想到，这个转换竟然也不是表面上那么显然。

### 怎么引用一个 Yaml 文件？

我一开始很天真地用 `fs` 去读 Yaml 文件，然后立刻发现，在 Web 环境里，这就很扯，根本不能访问文件系统，那么到底怎么将一个 Yaml 文件像 import 一样引入到代码里呢？

这里就要用到构建工具。这是我咨询了一个专家得到的答复。比如我们在代码里写代码：`import X from 'y'` 这样的代码能直接工作，根本上还是因为有一个构建系统，将这些代码都很好的组织起来，所以，这么简单一句 import 语句，并没有访问文件系统，而是在构建时候，就已经重新组织起来成为一个文件了。

得益于这种特性，我方可以将源代码放在不同的目录里，分类管理复杂度，让整个项目能更轻松地维护。

那么，显然，只要构建工具，能把一个 Yaml 文件加载进来，当场一个 JS Plain Object，我们的目的就达成了，我们可以直接：`import Obj from 'config.yml'` 通过这样的语句，就直接得到了代表 Yaml 文件内容的 JS Plain Objcet，那就完美了。

想明白这层道理，发现这并没什么难的。

可以使用一个 [vite-plugin-yaml](https://github.com/Modyfi/vite-plugin-yaml) 插件，这是 Vite 的插件，如果你用的是别的构建工具，那么我认为原理应该是一样的。
```shell
npm install -D @modyfi/vite-plugin-yaml
```
安装插件到项目的 `dev-dependencies` 里面，然后打开`vite.config.ts`：
```ts
// vite.config.js / vite.config.ts
import ViteYaml from '@modyfi/vite-plugin-yaml';

export default {
  plugins: [
    ViteYaml(), // you may configure the plugin by passing in an object with the options listed below
  ],
};
```
注册这个插件，如果你像我一样使用 ts，那么还有注册类型：
```json
// tsconfig.json
{
  "compilerOptions": {
    ...
    "types": [
      ...
      "@modyfi/vite-plugin-yaml/modules"
      ],
  }
}
```
告诉 ts 的编译器，yml 和 yaml 这两个文件扩展名的类型。至此，就可以像使用普通代码一样，使用 yml 文件了。
```ts
import YamlContent from './your.yaml'
```
这样就直接将 yml 文件读取成了 JS Plain Object，有了这个设定后，你就可以通过 i18n Ally 轻松愉快地修改语言文件了。

### 使用 JSON 格式

除了 Yaml 文件，还可以用 JSON 格式的语言包文件，相比起 Yaml 来说，可能更加方便一点，可能省去了安装 Vite 插件的过程。我猜是因为 js 和 ts 都对 json 格式兼容更好。

不过，我个人不是很喜欢 json 文件，太多双引号了，导致阅读 json 文件让人很不愉快。

不过考虑到其方便的特性，也很推荐大家使用 json 作为语言包文件，而不是很多例子里给出的 js 或者 ts 文件。

### 配置 i18n Ally

注意，在项目里，一定要用导入 `vue-i18n` 这个包，否则只安装 i18n Ally 插件是不起作用的。如下，是一些推荐的配置项：
```json
{
  "i18n-ally.localesPaths": ["src/locales"],
  "i18n-ally.keystyle": "nested",
  "i18n-ally.indent": 2,
  "i18n-ally.tabStyle": "space",
  "i18n-ally.sortKeys": true,
  "i18n-ally.namespace": true,
  "i18n-ally.enabledParsers": ["yaml"],
  "i18n-ally.sourceLanguage": "en",
  "i18n-ally.displayLanguage": "zh-CN",
  "i18n-ally.ignoredLocales": [],
}
```
这些配置可以加入全局的配置里，不过更常见的是加入到单个项目的`.vscode` 文件夹里，作为项目范围的配置。因为每个项目的多语言环境和设置都不一样，在单个项目里更合理一点。需要注意的是 `.vscode` 文件夹必须跟 `package.json` 文件同级目录，不然不起作用。

## 总结

本文介绍了一个很基础的技术话题，国际化。在 Vue 项目中使用 vue-i18n 库，也是一个很基础的事情，搭配 i18n Ally 插件和 VSCode 可以提供很好的开发体验。这里的技巧是用 json 或者 yaml 格式作为语言包文件的格式，而不是使用 js 或者 ts。