---
title: 如何使用 Hexo 和 Github Actions 搭建个人博客
tags:
  - Hexo
  - Github
categories:
  - 日　　记
id: '1239'
date: 2023-06-05 17:02:08
permalink: how-to-use-hexo-and-github-actions-to-build-a-personal-blog/
---



前两天试用了 Hugo 作为个人博客系统来使用，安装部署的体验不错，不过，当我将全部系统搭建完毕后，我想找一个美观大方，符合我自己这种老派审美的主题时，我犯难了，因为 Hugo 的主题实在是太难找了。虽然主题看起来也比较多，不过，符合我审美的主题，少之又少。

我看过官方目录，竟然不能按照热门程度、更新频度等关键评估指标进行排序，就算是想知道每个皮肤的全部特性，也显得万分困难。我得去知乎帖子，V2EX帖子等等网友推荐列表里寻找主题，而找到的主题多数良莠不齐，比起 WordPress 世界强大完善的主题和插件生态，真是令人失望。

<!-- more -->

另外也不知道是错觉还是什么，我总觉得，Hugo 配套的最好的主题，也都显得稀松平常，甚至跟一些网友怀疑的一样，我也觉得是不是搞后台 Go 语言开发的这帮人，做网页终究还是不大行。于是，我萌生了尝试一下 Hexo 的想法，Hexo 同样也是一个静态网站生成器，区别在于其使用 nodeJS 开发，生态里也多数都是前端程序员。预览了一些博客，发现确实更加美观，功能也齐全，这点要平均优于 Hugo 的各种主题。

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

按照上面命令顺序执行，基本就可以顺利在本地启动一个 Hexo 的博客，通过 http://localhost:4000 默认地址访问，就可以看到一个只有一篇 Hello World 文章的博客，默认的主题叫 `landscape` 看起来还挺好看，整洁大方，美观舒适，瞬间感觉这东西完爆 Hugo 啊……

## 构建、部署自动化

能够在本地启动，还不足够，记得上篇文章，咱们的需求是，能够完全脱离本地环境运行，在本地环境编辑、编译，只是一个可选项，如果没有本地环境，就算直接在 Github 版本库，也要能直接发布博客文章，这是一个核心的需求点，所以第二步，咱们就来实现这个。

这个任务本质上是 CI/CD 这个范畴的一个任务，无非就是，第一步，准备运行环境，第二步，构建所有静态页面，第三步，部署到指定位置。在使用 Hugo 平台的时候，将 hugo 生成的站点文件推送到 GitHub 后，GitHub Actions 频道会自动推荐一个 workflow 给我，是其他大神或者组织业已写好的配置文件。而当我把 Hexo 生成的站点目录推送到 GitHub 后，发现没有对应的 Actions 推荐。后来，我研究了一下，可能 Hugo 的那个 workflow 是官方研发团队编写的，经过认证，所以会进入 Github 的自动推荐。

Hexo 其实也有很多大神编写好的 workflow，但是因为都是个人做的，所以没被系统推荐。大家可以去 Github 上的 Marketplace，然后导航菜单中，Types 选定 Actions，直接搜索 hexo 关键字，就能找出很多各种人发布的，将 hexo 站点构建部署的现成的工作流。简直太方便了，给我打开了一扇新的大门。

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

我自己也来 share 一个，这个是我根据 Hugo 的那个官方发布的工作流改的，改成了适合于 Hexo 的。我找了一个现成的 Hexo 的工作流，很短小精悍，确实可用，不过我觉得它写得不好，没有注释，未来不好扩展和维护，反正我也需要学习一下。所以我就把大神写的 workflow 按照 Hugo 发布的那个，逐行逐行改过去，没想到我只写了一遍，就完全正确运行了，让我十分得意。

## 内容迁移

说实话，Hexo 的入门门槛并不高，你从了解到这个东西，到把它部署起来，速度是很快的。就我上面的这些步骤，到能在 GitHub Pages 上自动发布，半天内足够了，甚至可以基本搞清原理。不过，一般来说，你不是首次假设博客的话，都面临一个原来博客搬家的问题。比如我从 2008 年起，使用 WordPress 博客，我想搬家的话，需要把所有的文章搬迁到 Hexo 上。这个过程是不那么友好的。

### 文章

根据文档，Hexo 有一个 WordPress 博客迁移的工具插件，使用：

```bash
npm install hexo-migrator-wordpress
```

即可安装成功，然后，在 WordPress 博客选择导出功能，将全部内容导出成一个 XML 文件，然后，使用：
  
```bash
hexo migrate wordpress <source> --save
```

就可以将博客所有文章导入到 hexo，当然，故事不会那么圆满。我就碰到相当多的坑，在网上，你也轻易可以搜到各种关于坑的讲述，以及解决办法。比如，主要有几个问题：第一，比如我安装的一些插件，Taxopress 这种处理 Tags 的插件，会在日常写文章的时候，生成一些日志，会储存在 posts 表里，这些日志的内容和文章一样，但是 post_type 是 taxopress 而不是 post，可是无论是 WordPress 自己的导出工具，还是 hexo 的迁移工具，都不能正确过滤掉这个类型。导致你导入后发现，同一篇文章被导入了多次，夸张的有连续导入 5 遍的情况。

后来，我不得不将数据库备份导入一个临时安装的 WordPress，然后从数据库里硬删除 post_type 为 taxopress，link，menu 等等，甚至还有 custom_style 类型的记录。然后再执行导出，得到的 xml 里才混入了比较少的杂质，方便导入。

### 图片

第二个问题是，WordPress 中的图片，是不会被自动导入的，首先你必须手动从服务器上现在图片文件夹到本地。然后，你必须修复每篇文章中，对图片的引用。不然，所有的文章里引用的图片都会用绝对网址链接到你原来的博客。而不会用相对路径链接到本地服务器。为了做这件事情，我专门编写了一个工具。放在本博客的根目录下。首先把图片全部下载，安排好放置的目录，然后用脚本将所有文章的引用，都改为从本地引用。

另一个问题是，WordPress 的文章里有时候插入了一些表格，在我的这次转换中，此类文章，表格在转换完，都破碎了。页面几乎都无法查看了。暂时，我还没找到特别好的方法。

### 分类

第三个问题是，WordPress 和 Hexo 对博客分类的使用和假设不同，比如在 Hexo 里，你不能像 WordPress 那样去设定分类，因为它默认分类只有一层，如果你想使用嵌套的分类，必须使用特殊的语法去设定，这样一来，你使用工具批量转换文章的时候，自动工具的分类设置很多都是错误的。

因为在 Hexo 父分类，子分类的表达方式是不一样的，而迁移工具基本不能正确处理分类的问题。我 400 多篇文章，迁移后，大概 150 篇文章的分类是错的。

## 模版定制

其实，博客皮肤模版，是一个设立一个博客最大的问题。大部分用户都会非常纠结，一是希望自己的博客尽量美观，二是希望自己的博客尽可能功能齐全，在前两者的基础上，往往还希望能有个性和特色。而这些东西往往在大量的皮肤上都是不可兼得的。因为，博客的皮肤，大部分是都是爱好者个人制作的，第一个满足的也都是自己个人的使用需求，虽然出于好心也会发布到公网上，但是很少会做得非常完善。另外用户在不明白原作者思路的情况下，也很难用得很好。

就这一点来看，Hexo，Hugo 这种类型的平台，拍马屁也追不上 WordPress，WordPress 作为世界上最好的博客平台，有着完善的生态系统，庞大的用户群体，在博客主题方面，除了官方的目录，还有很多平台在贩卖收费版皮肤，可以说，选择之多如过江之鲫，而质量之高也足堪使用，毕竟你还能选择付费皮肤让作者提供特殊支持。但是 Hexo 和 Hugo 都要差很多了。

我选定的皮肤是一款比较著名的皮肤，叫 Next，经调查，发布后维护的年头相当长了，各方面都非常完善，竟然也衍生出了自己的插件，十分丰富，我亲测觉得质量也比较过硬。所以我就选了这款了，事实上，我看过很多中文的个人博客，都用的这款皮肤，只不过从不同程度上定制了。

具体的设定参数非常多，大家可以自己看看文档，跟着做就能完成，还比较简单，就不想多费笔墨了。



## 日常管理

如果，你是一个以写作为主，而不是以折腾博客本身为主的玩家，那么你一定会遇到一个问题就是内容管理问题。比如我的博客，刚才说了有 400 多篇文章，从 WordPress 导入后，都放在 source/_posts 文件夹下平铺着，默认用了每篇文章的 post_slug 作为文件名，我那种崩溃，不知道你们能不能想象到。日常，如果一个文件夹有 400 多个文件，你一定会觉得无从管理了。如果所有的文件名又是英文单词拼接成的 slug，更加头晕了。因为时间日期信息又写在文件内部，排序也好，筛选也好，都很难做到。

对比一下 WordPress，采用数据库进行管理，可以进行简单的搜索，而已如果你懂一点点技术也可以轻易用 SQL 进行批量操作。你会感觉到一个从天到地的落差感。至少不要傻乎乎将所有文章都放到一个单个文件夹比较好吧。

我设定一个规则，文件命名采用文章标题的中文，然后将原来的 post_slug 设定为每篇文章的网址，用 permalink 这个 front matter 字段来设定。然后，在配置文件里指定 permalink 的格式。每篇文章用这篇文章的月份 + 26进制后缀（小写字母）来做前缀，放在以年为名称的文件夹里。这样按照我每年输出十几到几十篇文章的频度，完全够用了。每月写文章超过 26 篇，我这个编号体系就会爆掉。不过幸好我没那么高产。

这样，我一个文件夹里，最多就二三十篇，当然 2008 年我最积极，写了 100 多篇，也没什么，反正不会再去修改历史上的文档了。为了完成这个重命名工作，我又写了一个 Python 脚本，也提交到了本站的 repo 里了。

如果没有一点编码能力的非行内人，你会发现这种系统真的非常不友好，几乎等于完全不可用的一个系统了。

## 写作

全部收拾停当后，我可以安心写作了，然后我发现我遇到了难题。

因为在这个博客系统里，所有的内容，不是数据化的，也不是结构化线性存储的。而你在写作的时候，你的文章也是脱离的系统孤立存在的，比如在 WordPress 中写作博客，分类信息，标签信息，你都可以进行下拉选择，或者输入一个字符，就会有大量的提示和建议出来。但是在 Hexo 博客里，不会有任何提示，甚至你写作了一点点，多加了个空格，都会导致分类信息和标签信息无法正确匹配，被识别为全新的分类或者标签。

这样一来，就要求你每次写作的时候，对自己的全部分类体系都有相当完整和精确的记忆，这就给人脑带来了巨大的心智负担。这点是让我最为痛苦的。不知道大家都是怎么解决的？我想到的当然是最后有个客户端，能在内存中把所有的东西都加载进去，然后写作的时候，可以很好的提供提示功能。而不是像现在，找一篇历史写过的文章，进去复制黏贴。

而经过搜索，比较推荐的客户端软件都已经停更至少 3 年了。这一点我非常遗憾。我想，如果有一个好的客户端，我会更加喜欢这个博客系统的。