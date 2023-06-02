---
title: 如何使用 Docker 部署一个 WordPress
date: 2023-06-05 09:56:22
tags: 
  - Docker
  - WordPress
categories:
  - WordPress
permalink: how-to-deploy-wordpress-with-docker/
---

很多年前开始，我在 Mac 上调试 Web 应用，就是使用一个 App，叫 MAMP Pro，这是一个德国软件，相当于 Windows 上的 xampp，是 Apache + PHP + MySQL 套装。用起来很方便，主要在一台机器上，可以启动很多个 Web 应用，比较节省资源，当然，这不是什么优点，真正的优点是开箱即用，非常方便。

不过现在，我公司深度采用云计算和 Docker，k8s 等基础设施，在本地使用 AMP 套件，其整体部署和服务器环境相差就比较远了。而且最近开发 Flutter 远多于 PHP，还有一个因素是我刚换了 m1 的 Mac，而 MAMP 还是 x86 架构的，干脆还是尽量用 Docker 吧。

<!--more-->

## 拉取镜像

```shell
docker pull mysql:latest
docker pull wordpress:latest
```

WordPress 镜像里应该是自带 Web 服务器的，所以，依赖只有一个 MySQL 了。

## 编排服务

当然，你可以先启动 MySQL，然后再启动 WordPress，手动操作也没什么。不过，启动数据库，你要指定端口，root 密码，而启动 WordPress，你要指定的就多了，数据库相关的配置 4 个，还有一些随机 Key，数据库表前缀等参数，就比较麻烦，还是直接用配置文件比较方便。具体可以参看镜像官网。

下面的编排文件也是从镜像官网得到的：

```yaml
version: '3.1'

services:

  wordpress:
    image: wordpress
    restart: always
    ports:
      - 8080:80
    environment:
      WORDPRESS_DB_HOST: db               # 注意这里，host 填写的名字是下面一个服务的名字
      WORDPRESS_DB_USER: exampleuser
      WORDPRESS_DB_PASSWORD: examplepass
      WORDPRESS_DB_NAME: exampledb
    volumes:
      - wordpress:/var/www/html

  db:
    image: mysql:latest
    restart: always
    environment:
      MYSQL_DATABASE: exampledb
      MYSQL_USER: exampleuser
      MYSQL_PASSWORD: examplepass
      MYSQL_RANDOM_ROOT_PASSWORD: '1'
    volumes:
      - db:/var/lib/mysql

volumes:
  wordpress:
  db:

```

你可以随便创建一个空文件夹，然后，将上述的文件拷贝到一个名为 docker-compose.yml 文件里，然后在这个目录下，执行 docker compose up，神奇的事情发生了，全部启动成功了，不得不感叹时代的进步。

## 导入现存

如果你有一个已经存在的 WordPress 博客，你可以执行 mysqldump，下载一个已经存在的数据库。然后导入到上面启动的环境中：
    
```shell
docker cp ~/Downloads/wp-db-dump.sql 1fa12d5802fb:/root/
```

将命令里的 ID 换成你的 container id，就可以将 sql 文件导入到 container 内部；然后执行：

```shell
docker exec -it 1fa12d5802fb /bin/sh
```

登录到 container 的 shell，然后登录 mysql 客户端执行：

```sql
select concat('drop table ', table_name, ';') as 'droptables' 
from information_schema.tables 
where table_schema = 'exampledb';
```

可以生成一系列 drop tables 语句，然后，执行导入：

```shell
mysql -uexampleuser -pexamplepass exampledb < /root/wp-db-dump.sql
```

就可以将你已经存在的 WordPress 数据库导入到数据库里。不过，如果想要导入的数据库可以正常加载的话，你需要把 wp_options 表里的两个值改掉，siteurl 和 home 两个选项的值，要配成你当前需要调试的域名和端口号上，并且使用 Chrome 的无痕浏览模式才行，不然，都会导致你没法访问导入既有数据库博客。

如果你访问自己的博客，发现白屏的话，建议你先尝试登录后台，http://localhost:8080/wp-admin/ 这个网址，因为你线上导入的博客，配置的主题和插件都不存在，直接访问首页的话，会报错，极可能不能正常展示，但是登录后台后，你会发现很多插件的错误提示，主题也更换成默认的。站点就恢复正常了。

这时候，你可能会发现，只有首页是可以访问的，其他所有页面都访问不了。可能是因为你线上的博客配置了 rewrite 规则，但是在上面的说明中，我并没有展示怎么去配置 rewrite 规则，所以，会出现这个现象。

## 总结

总体来说，使用 Docker 启动一个 WordPress 环境是简单的，3202 年的今天，一切都变得如此丝滑。上面的整个记录，还是缺乏了很多细节的，比如，怎么配置和调试 rewrite 规则，怎么配置和调试持久化 Volume，等等，都是需要查询大量文档和调试工作。本文并不是一个教程，只是做这个事情的主干剧情，大概需要干点什么，给基本明白的人一个提示和备忘，希望对您有帮助。