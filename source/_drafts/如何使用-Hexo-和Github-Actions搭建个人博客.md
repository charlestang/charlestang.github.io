---
title: 如何使用 Hexo 和Github Actions搭建个人博客
tags: []
id: '1239'
categories:
  - - 日　　记
---

前两天试用了一个 Hugo 作为个人静态博客生成器，体验很是不错，不过，当我将全部系统搭建完毕后，我想找一个美观大方，符合我自己这种老派审美的主题时，我犯难了，因为 Hugo 的主题实在是太难找了。

我看过官方目录，竟然不能按照热门程度、更新频度等关键评估指标进行排序，就算是想知道每个皮肤的全部特性，也显得万分困难。我得去知乎帖子，V2EX帖子等等各种奇奇怪怪的地方寻找主题，而找到的主题多数良莠不齐，比起 WordPress 世界强大完善的主题和插件生态，真是令人失望。
<!-- more -->
另外也不知道是错觉还是什么，我总觉得，Hugo 配套的最好的主题，也都显得稀松平常，甚至跟一些网友怀疑的一样，我也觉得是不是搞后台 Go 语言开发的这帮人，做网页终究还是不大行。于是，我萌生了尝试一下 Hexo 的想法，Hexo 同样也是一个静态网站生成器，区别在于使用 nodeJS 开发，生态里也多数都是前端程序员。确实预览了一些博客，发现更加美观，功能也齐全，这点要平均优于 Hugo 的各种主题。

## 安装搭建

找了一个[教程](https://zhuanlan.zhihu.com/p/618864711)，按着操作，发现本地安装和启动过程，还是非常流畅的。

```shell
# 安装 node
brew install node
# 更新 npm
npm install -g npm@9.6.7
# 安装 hexo 命令行
npm install hexo-cli -g
# 初始化一个博客站点，blog 可以换成你自己的文件夹名字
hexo init blog
# 启动博客
cd blog
npm install # 安装依赖
hexo server
```

按照上面命令顺序执行，基本就可以顺利在本地启动一个 Hexo 的博客，通过 http://localhost:4000 默认地址访问，就可以看地一个只有一篇 Hello 作为文章的博客，默认的主题叫 `landscape` 看起来还挺好看，整洁大方，美观舒适，瞬间感觉这东西完爆 Hugo 啊……

## 构建、部署自动化

能够在本地启动，还不足够，记得上篇文章，咱们的需求是，能够完全脱离本地环境运行，在本地环境编辑、编译，只是一个可选项，如果没有本地环境，就算直接在 Github 版本库，也要能直接发布博客文章，这是一个核心的需求点，所以第二步，咱们就来实现这个。

这个任务本质上是 CI/CD 这个范畴的一个任务，无非就是，第一步，准备运行环境，第二步，构建所有静态页面，第三步，部署到指定位置。在使用 Hugo 平台的时候，推送完 hugo 生成的站点文件，系统会自动推荐一个 workflow 给我，是其他大神或者组织业已写好的配置文件。而当我把 Hexo 生成的站点文件推送后，发现没有对应的推荐。我后来，研究了一下，可能 Hugo 的那个 workflow 是官方研发团队编写的，经过认证，所以会进入 Github 的自动推荐。

Hexo 其实也有很多大神编写好的 workflow，但是因为都是个人做的，所以反倒无法被系统推荐。大家可以去 Github 上的，Marketplace，然后导航里，Types 选定 Actions，直接搜索 hexo 关键字，就能找出一堆各种人发布的，将 hexo 站点构建部署的现成的工作流。简直太方便了，给我打开了一扇新的大门。

```yaml
# Sample workflow for building and deploying a Hugo site to GitHub Pages
name: Deploy Hexo site to Pages

on:
  # Runs on pushes targeting the default branch
  push:
    branches: ["master"]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest queued.
# However, do NOT cancel in-progress runs as we want to allow these production deployments to complete.
concurrency:
  group: "pages"
  cancel-in-progress: false

# Default to bash
defaults:
  run:
    shell: bash

jobs:
  # Build job
  build:
    runs-on: ubuntu-latest
    #env:
    #  HUGO_VERSION: 0.108.0
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Cache NPM dependencies
        uses: actions/cache@v3
        with: 
          path: node_modules
          key: ${{ runner.os }}-npm-cache
          restore-keys: 
            ${{ runner.os }}-npm-cache

      - name: Install Node.js 16.x
        uses: actions/setup-node@v3
        with:
          node-version: 'latest' 
      - run: npm install
      - run: npm run build
      # https://github.com/marketplace/actions/configure-github-pages
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v3
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v1
        with:
          path: ./public

  # Deployment job
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

我来 share 一个，这个是我根据 Hugo 的那个官方发布的工作流改的，改成了适合于 Hexo 的。我找了一个现成的 Hexo 的工作流，很短小精悍，确实可用，不过我觉得它写得不好，没有注释，未来不好扩展和维护，反正我也需要学习一下。所以我就把大神写的 workflow 按照 Hugo 发布的那个，逐行逐行改过去，没想到我只写了一遍，就完全正确运行了，让我十分得意。

## 内容迁移

## 模版定制