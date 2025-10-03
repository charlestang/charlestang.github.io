---
title: '为什么用 npm/yarn 时会发生 Error: certificate has expired'
permalink: 2024/why-certificate-error-using-npm/
categories:
  - - 技术
    - 前端
tags:
  - usage
  - develop
date: 2024-02-20 15:50:53
updated: 2024-05-06 14:10:11
---
# 缘起

昨天，我写了一篇文章，介绍[如何使用项目模板，构建一个 Electron 项目的脚手架](/2024/howto-quick-start-a-electron-app/)，我发现我自己在本地无法运行成功，出现了错误。

```text
  ✖ Failed to install modules: ["@electron-forge/plugin-vite@^7.2.0","@typescript-eslint/eslint-plugin@^5.0.0","@typescript-eslint/parser@^5.0.0","eslint@^8.0.1","…
    With output: Command failed with a non-zero return code (1):
    yarn add @electron-forge/plugin-vite@^7.2.0 @typescript-eslint/eslint-plugin@^5.0.0 @typescript-eslint/parser@^5.0.0 eslint@^8.0.1 eslint-plugin-import@^2.25.0…
    yarn add v1.22.21
    info No lockfile found.
    [1/4] Resolving packages...
    info Visit https://yarnpkg.com/en/docs/cli/add for documentation about this command.
    (node:89705) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
    (Use `node --trace-deprecation ...` to show where the warning was created)
    error Error: certificate has expired
    at TLSSocket.onConnectSecure (node:_tls_wrap:1674:34)
    at TLSSocket.emit (node:events:515:28)
    at TLSSocket._finishInit (node:_tls_wrap:1085:8)
    at ssl.onhandshakedone (node:_tls_wrap:871:12)
    (node:89705) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
    (Use `node --trace-deprecation ...` to show where the warning was created)
    error Error: certificate has expired
    at TLSSocket.onConnectSecure (node:_tls_wrap:1674:34)
    at TLSSocket.emit (node:events:515:28)
    at TLSSocket._finishInit (node:_tls_wrap:1085:8)
    at ssl.onhandshakedone (node:_tls_wrap:871:12)
  ⚠ Finalizing dependencies
```

错误内容如上，看着一大段，很吓人的样子，不过可以仔细阅读一下，真正的错误是在第 10 行，`Error: certificate has expired`，如果你去网上搜，遇到这个错误怎么办？

<!--more-->

# 探究

你会搜到很多文章，告诉你，将 `strict-ssl` 设置成 `false`，就可以解决这个问题。确实没错，这样设置真的可以解决问题。

不过，作为程序员，我们还是要探究一下原因，为什么我只是根据模板创建一个项目，就会遇到这种那种奇怪的错误呢？

昨天写文章太急了，我也没有深究，还是把解决方案写上了。今天我花点时间来研究一下。有不少文章说，是因为挂了代理导致的，你可以使用命令：

```shell
echo $http_proxy
echo $https_proxy
```

检查一下，命令行环境下，是否挂了代理，我发现我是没有挂代理的。那么，什么情况下会出现这个错误呢？

1. **服务器证书过期**：包管理器的服务器证书确实过期了。这种情况下，你需要等待服务器端更新证书。
2. **本地系统时间错误**：如果你的计算机系统时间设置不正确，可能会导致证书验证失败。确保你的系统时间是准确的。
3. **代理或 VPN 问题**：如果你使用了代理或 VPN，可能会影响 SSL 证书的验证。尝试暂时禁用这些服务，看是否能够解决问题。
4. **本地证书问题**：你的本地系统可能存在证书问题，比如缺少最新的根证书或中间证书。

上面，是 AI 给出的答案，我觉得可以逐一排查一下，其中第 3 点，我已经排除了。看了眼时间和手机，第 2 点也可以排除了，而第 4 点，根据 SSL 的原理，我们是用本地根证书来验证站点的 SSL 证书的，我觉得可以最后怀疑这个。

那么就只剩下第 1 点了，可是闻名天下的 npm 服务器怎么可能证书过期呢？

```shell
yarn config list
```

我执行一看：

```text
{
  'version-tag-prefix': 'v',
  'version-git-tag': true,
  'version-commit-hooks': true,
  'version-git-sign': false,
  'version-git-message': 'v%s',
  'init-version': '1.0.0',
  'init-license': 'MIT',
  'save-prefix': '^',
  'bin-links': true,
  'ignore-scripts': false,
  'ignore-optional': false,
  registry: 'https://registry.npm.taobao.org',
  'strict-ssl': true,
  'user-agent': 'yarn/1.22.21 npm/? node/v21.1.0 darwin arm64',
  lastUpdateCheck: 1707273586611
}
```

大家注意第 13 行，`registry: 'https://registry.npm.taobao.org'`，原来，我用的不是 `npm` 官方的 `registry`，怪不得，淘宝提供的镜像过期了，那很有可能。

结果一搜，[实锤了《淘宝 NPM 镜像站切换新域名啦》](https://developer.aliyun.com/article/801527) （2021-11-09）。原来，官方声明，在 2022-05-31 日，我用的 `registry.npm.taobao.org` 早就已经过期了。现在都 2024 年了，难怪。

# 原因

那么为什么，我会用了一个淘宝的源呢？其实，主要因为一些不可说的原因，在我国访问美国那边的各种服务，总是有些一言难尽，在宽带随便 100M 的今天，我们下载一个项目依赖，动辄以小时计算，于是大家网上随便一搜，都会有文章告诉你把 `registry` 改成 XXXX，于是我就改了。

相信你今天去搜，还是会看到大把文章告诉你，改成那个过期的域名呢。人家官方早就不为过期子域名维护证书了，只是没有取消解析而已。结果，反倒诞生了 `strict-ssl` 设置为 `false` 这种解决方案，就好像非要在一颗歪脖树上吊死一样的执拗。

# 解决

```shell
yarn config set 'strict-ssl' true
yarn config set registry "https://registry.npmmirror.com"
```

就可以轻松解决问题了，还没有降低项目的安全性。当然，用官方源，在系统全局挂代理提高网速，也是可以的，官方源地址是 ：`https://registry.npmjs.org/`。

其实，我还想强调一点，将 `strict-ssl` 设置成 `false`，真正的含义是，当连接一个 SSL 协议的网站时，不去检验服务器提供的证书的真假，也即，服务器的域名与证书可能不符，或者根本没有证书，或者是不合格 CA 颁发的，这些可能得欺诈，我们都直接忽略。

这是将我们项目的安全，完全建立在没有黑客会来攻击的基础上，是在凭运气确保项目安全，**是非常不负责任的行为**。养成这种习惯，让项目长期置于这种危险中，是很没有职业素养的做法。

# 总结

在项目里遇到了问题，快速搜索解决方案，掉到了坑里，其实无可厚非，只要我们保持自己的好奇心，求甚解，及时归还技术债务，就还是好少年！
