---
title: Docker 常用操作的备忘录
tags:
  - docker
  - usage
id: '1147'
categories:
  - 工作相关
date: 2022-09-27 12:21:34
permalink: docker-memo/
---

![docker](../images/2022/09/dockerlabs.jpeg)

Docker 一旦设置好了环境，日常就只要使用简单命令就可以运行和停止。

于是，我每次用的时候，都想不起来一些关键性的命令到底怎么用，特此记录。

<!--more-->

## 镜像管理

从公有仓库拉取镜像：

```shell
docker pull redis:7.0.5-alpine3.16 --platform linux/amd64
```

查看本地的镜像：

```shell
docker images
```

删除一个本地镜像：

```shell
docker image rm <REPOSITORY>:<TAG>
```

## 容器管理

查看本地的所有容器：

```shell
docker container ls --all
```

给本地镜像打上一个 tag：

```shell
docker tag redis:7.0.5-alpine3.16 registry.selfhost.com/redis:7.0.5-alpine3.16
```

将镜像推送到私有仓库：

```shell
docker push registry.selfhost.com/redis:7.0.5-alpine3.16
```

连接一个正在运行的 container：

```shell
docker exec -it <CONTAINER-ID> /bin/sh
```

⚠️ 注意：使用 Apple Silicon 的 MacBook Pro (M1/2) 时候，`docker` 命令，默认拉取的镜像，构建的镜像，都是 `linux/arm64/v8` 的，但是，服务器开发的运行环境往往是 `linux/amd64` 的，注意交叉编译的问题。

## Dockerfile

### ADD 指令和 COPY 指令有什么异同？

ADD 指令和 COPY 指令有一些重叠，都是将一个文件从源路径复制到目的路径。不过 ADD 指令会有更多的内涵。

如果源路径是一个网址的话，ADD 指令会下载文件，如果源路径是一个压缩包的话，ADD 指令会解压缩。

[最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)里，建议尽量使用 COPY 指令而不是 ADD 指令，因为 COPY 指令有更明确的功能。

一般建议，在解压缩的场景使用 ADD 指令，其他场景都是用 COPY 指令。

### ENTRYPOINT 和 CMD 有什么异同？

今天我在看 Docker Hub 的一个镜像的代码，发现 Dockerfile 里同时指定了 ENTRYPOINT 和 CMD 两个指令，我没有细细研读过 Docker 的手册，不过看代码，以及看字面意思，就觉得这两个仿佛重复了。

放狗一搜，才知道，这两个指令的用途真的是一样的。如果在 Dockerfile 两个都不指定，则 docker run 默认不能自动运行镜像，必须指定一个命令。两者只指定一个，docker run 就可以不指定命令自动运行。不过仍然有细微的差别。

首先，ENTRYPOINT 的执行在 CMD 执行的前面。第二，CMD 命令，更容易被“覆盖”，docker run 如果后面带上命令的话，会覆盖 CMD；不过 ENTRYPOINT 指令的内容也可以覆盖，却是用参数 --entrypoint 来进行覆盖。第三，如果两个命令都存在的话，容器启动后，会用将两个命令的内容拼成一个，再执行。

这种设计会给容器的启动带来一些灵活性。

### 在 Alpine 中，如何定位问题

Alpine 是一个极简的操作系统，各种 Linux 发行版常见的命令，里面都是缺乏的，我试过了，如果不特意去安装的话，里面 vi 倒是有，其他什么都没有，比如 curl，ss，ip 等等命令，几乎都没有。

`apk add iputils` 可以安装 ip 和 ss 命令，用于查看 ip 地址，侦听端口等，便于开发时候调试用。


## docker-compose.yml

docker-compose 主要用于容器编排，我们在生产环境，主要使用 K8S 或者类似的实现来完成容器编排。不过在本地环境下，也就是我们自己的开发机上，如果想实现容器编排，使用 docker-compose 是比较简单的一种方式。

### 常见的使用场景

 - 搭建开发环境
 - 自动化搭建测试环境
 - 单主机部署

### command 指令

这个指令根据我理解，是可以覆盖 Dockerfile 中指定的 CMD 内容的，不过也只能出现一次。


## 常用镜像

### PHP

最近，我在恢复练习我 PHP 的开发能力，这次我搭建环境采用 Docker 实现。

在本地启动一个 PHP 环境，最简单的办法是采用 [PHP 官方提供的镜像](https://hub.docker.com/_/php)，官方镜像制作精良，小巧精悍，强于自己胡乱构建一个。

官方镜像包含了一些[特殊的命令](https://stackoverflow.com/questions/44603941/how-to-enable-pdo-mysql-in-the-php-docker-image)：

- docker-php-source
- docker-php-ext-install
- docker-php-ext-enable
- docker-php-ext-configure

#### docker-php-source

创建 PHP 源代码目录，主要是为了一些必须编译扩展的场景，需要依赖 PHP 的源代码。

```shell
docker-php-source extract | delete
```

这个命令提供两个子指令，顾名思义，就是解压缩和删除。

#### docker-php-ext-install

安装一些官方注册过的扩展，比如我这次要调试一个 PHP 应用，默认的 php-apache 镜像中，竟然没有 pdo_mysql 扩展，这其实就是一个官方维护的扩展，在 PHP 的源码里面，通过编译参数开启的。

可以使用：

```shell
docker-php-ext-install mysql pdo_mysql
```

实现安装。

#### docker-php-ext-configure

需要编译安装的情况，这个指令用来完成编译配置。

下面是一个例子：

```dockerfile
FROM php:7.1-fpm
RUN apt-get update \
    # 相关依赖必须手动安装
    && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libmcrypt-dev \
    libpng-dev \
    # 安装扩展
    && docker-php-ext-install -j$(nproc) iconv mcrypt \
    # 如果安装的扩展需要自定义配置时
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) gd
```
#### docker-php-ext-enable

如果有已经安装好的扩展，可以使用这个命令进行激活。

#### docker-php-ext-install

安装编译好的扩展。

## 参考

[Dockerfile: ENTRYPOINT 和 CMD 的区别](https://zhuanlan.zhihu.com/p/30555962) [英文版](https://www.ctl.io/developers/blog/post/dockerfile-entrypoint-vs-cmd/)

[Dockerfile 最佳实践](https://yeasy.gitbook.io/docker_practice/appendix/best_practices) [英文版](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

[Docker PHP安装扩展步骤详解](https://www.cnblogs.com/yinguohai/p/11329273.html)
