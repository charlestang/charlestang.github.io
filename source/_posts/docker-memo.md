---
title: Docker 常用操作的备忘录
tags:
  - docker
  - usage
id: '1147'
categories:
  - - 工作相关
date: 2022-09-27 12:21:34
---

从公有仓库拉取镜像：

```null
docker pull redis:7.0.5-alpine3.16 --platform linux/amd64
```

查看本地的镜像：

```null
docker images
```

删除一个本地镜像：

```null
docker image rm <REPOSITORY>:<TAG>
```

查看本地的所有容器：

```null
docker container ls --all
```

给本地镜像打上一个 tag：

```null
docker tag redis:7.0.5-alpine3.16 registry.selfhost.com/redis:7.0.5-alpine3.16
```

将镜像推送到私有仓库：

```null
docker push registry.selfhost.com/redis:7.0.5-alpine3.16
```

连接一个正在运行的 container：

```null
docker exec -it <CONTAINER-ID> /bin/sh
```

⚠️ 注意：使用 Apple Silicon 的 MacBook Pro (M1/2) 时候，`docker` 命令，默认拉取的镜像，构建的镜像，都是 `linux/arm64/v8` 的，但是，服务器开发的运行环境往往是 `linux/amd64` 的，注意交叉编译的问题。

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

## 参考

[Dockerfile: ENTRYPOINT 和 CMD 的区别](https://zhuanlan.zhihu.com/p/30555962) [英文版](https://www.ctl.io/developers/blog/post/dockerfile-entrypoint-vs-cmd/)

[Dockerfile 最佳实践](https://yeasy.gitbook.io/docker_practice/appendix/best_practices) [英文版](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)