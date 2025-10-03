---
title: 【nginx】 配置 gzip 模块
tags:
  - configuration
  - nginx
  - usage
id: '789'
categories:
  - - 技术
    - 前端
permalink: nginx-config-gzip-module/
date: 2017-10-26 01:16:01
---

在使用 nginx 的时候，配置 gzip 模块，可以让服务器的伺服更加高效，对于文本类型的数据，传输量可以压缩一半左右。

官方建议我们创建一个叫 conf.d 的文件夹，使用 include 语句，将 gzip 的配置文件插入到 http 区段。
<!-- more -->
```conf
# 打开gzip 功能
gzip on;

# 针对老旧的微软浏览器关闭gzip 功能
gzip_disable "msie6";

# 设定需要被压缩的资源类型
gzip_types text/css text/xml text/plain
           application/javascript application/json
           application/atom+xml application/rss+xml;

# 启动压缩的最小资源体积，压缩是占用资源的，太小的资源就不压缩了
gzip_min_length 1000;

# 对于代理的请求，代理服务器没有缓存的，不许存储的，过期的，需要身份验证的
# 这些都被视为是纯动态的请求，应该被压缩
gzip_proxied no-cache no-store private expired auth;
```

gzip 模块，有好几个指令，特意重温了一下，记录下来跟大家分享。`gzip_disable` 是为了兼容老旧的浏览器的，现如今应该没什么用了，但是如果考虑到广泛伺服的公众服务，可以配置上这个，文档中描述，这个指令接受的是一个 pattern，而 “msie6” 是一个内置 pattern，会被自动翻译成对应于微软老旧浏览器的 pattern，但是比直接写目标 pattern 的效率高一点。

gzip_type 指定了要压缩的资源类型，默认的情况下，只有 text/html 会被压缩。值得注意的是，在配置这个指令的时候，不需要再次写入 “text/html” 这个值，因为这个 MIME 类型，是必然会被压缩的，如果你写上了，语法检查，会报一个 warning。这里，我还遇到了其他几个知识点，比如 “text/javascript” 和 “application/x-javascript” 这两个 MIME 类型到底要不要放进去呢？我特意检查了一个官方默认的配置文件 mime.types ，里面是没有前述的两个 MIME 的。SO 查了一下，“text/javascript” 是不规范的写法，已经弃用了（deprecated），而 “application/x-application” 是一种实验期的写法，x- 代表实验（experimental），一直坚持用到标准落地，而现如今，其实标准已经落地了，正确的写法就是一个 “application/javascript”。

gzip_min_length 是一个启动模块的阈值，根据 Content-Length 来判定。虽然压缩可以大幅度节省流量，但是显然，这个操作会浪费 CPU，所以，如果文件太小，启动一次压缩，就不合算了。默认这个指令是 20 字节，官网推荐的是设置为 1000。

最后一个指令，是针对代理的，默认情况下，nginx 不会对代理的内容进行压缩。但是官网认为，针对代理的内容也是应该压缩的。但是要小心应对。我贴的几个选项也是官网推荐的用法。