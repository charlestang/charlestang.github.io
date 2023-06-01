---
title: OpenResty学习笔记：使用 Lapis 框架开发 Web 应用
tags:
  - Lua
  - OpenResty
  - web
id: '775'
categories:
  - - 工作相关
  - - something-about-daily-work
    - 心得体会
date: 2017-08-18 04:36:03
---

不知道从哪一届开始，老罗开锤子手机发布会的时候，会当场捐赠一款开源软件，第一次是捐赠给 OpenSSL，第二次是 OpenResty。那次发布会开完，OpenResty 在程序员圈子里火了一把，成为一种热门技术了。其实，OpenResty 在后端程序员世界里，早就享有盛名。当你不得不去面对高并发的场景的时候，你一定会发现 Nginx 的巧妙和强大，然后你会想到用 Nginx 解决问题，然后你一定会发现 OpenResty。
<!-- more -->
三年前就想学 OpenResty，一直被拖延症耽搁了。这期间，OpenResty 发展很快，无论是自身还是社区都进步很快，甚至也有了配套的 [awesome-resty](https://github.com/bungle/awesome-resty) 项目。我下定决心这次好好学学。

因为我是 Web 开发，所以自然最关心的还是 Web 框架。之前就了解过新浪出的 Vanilla，但是我看了一点 Lua 语法，不是很喜欢，更不要提用其实现的 Web 框架了，好在我碰巧点开了 Lapis 的官网，发现还有一种语言叫 MoonScript，简洁优雅，真是 Lua 的绝佳替代。

## 安装 OpenResty

目前最新版本的 OpenResty 是 [v1.11.2.4](http://openresty.org/en/download.html) 发布于 2017/07/31 真是新鲜得发烫。一般，我使用 Debian 作为自己使用的操作系统环境，有比较方便的包管理器和比较稳定的服务器环境。Ubuntu 也是不错的选择。以下，我都会使用 Debian（jessie）。首先安装依赖的软件包，然后编译安装 OpenResty。

```shell
apt-get install libreadline-dev libncurses5-dev libpcre3-dev libssl-dev perl make build-essential curl

wget "https://openresty.org/download/openresty-1.11.2.4.tar.gz"
tar -xf openresty-1.11.2.4.tar.gz
cd openresty-1.11.2.4
./configure -j4
make -j4
sudo make install

```

以上的命令会把 OpenResty 安装到默认目录 `/usr/local/openresty`，也可以用 `./configure --help` 来查询编译选项，改变安装的路径。里面自带了 LuaJIT，在 `/usr/local/openresty/luajit/bin` 下有个 luajit 的二进制。执行 luajit 命令，会进入 Lua 的交互式命令提示符，使用下面的命令可以查询 Lua 的版本 `print(_VERSION)` Lua 的各个版本，语法不完全兼容，后续默认的讲的都是 Lua 的 5.1 版本。

## 安装 LuaRocks

Python 有 pip，PHP 有 Composer，Lua 有 LuaRocks，还真是酷呢。LuaRocks 在 Linux 环境默认只有编译安装的方式，依赖本机的 Lua 环境。虽然 OpenResty 里面带有了 LuaJIT，但是我试了一下，并不能简单代替原生 Lua 环境。所以，还是建议再安装 Lua 环境，避免踩坑和麻烦。

```shell
#一个命令安装 Lua 5.1 环境，以及依赖软件包
apt-get install lua5.1 liblua5.1-dev unzip

wget "https://github.com/luarocks/luarocks/archive/v2.4.2.tar.gz" -O luarocks-v2.4.2.tar.gz
tar xf luarocks-v2.4.2.tar.gz
cd luarocks-2.4.2
./configure
make build
make install

```

到这里，luarocks 就安装完毕了。

## 安装 Lapis

有了 LuaRocks，安装 Lapis 会非常简单，如下单个命令就能完成安装，一共会安装 12 个软件包，一个是 Lapis 自己，以及其依赖。

```shell
root@deb8➜  ~  luarocks install lapis
Installing https://luarocks.org/lapis-1.6.0-1.src.rock
Missing dependencies for lapis 1.6.0-1:
   ansicolors (not installed)
   date (not installed)
   etlua (not installed)
   loadkit (not installed)
   lpeg (not installed)
   lua-cjson (not installed)
   luaossl (not installed)
   luafilesystem (not installed)
   luasocket (not installed)
   mimetypes (not installed)
   pgmoon (not installed)

```

## 实现一个简单的 Demo

为了学习一个 Web 框架，我打算用这个框架开发一款最简单的应用。这里要用到框架的一些基础特性，比如 MVC，ORM，缓存等等。想了想，我要做一个手机号归属地查询的服务。以下是需求的细化：

> 需求：手机号归属地查询
> 功能：
> 1. 一个查询页面，上面一个查询框和一个按钮，输入手机号码，点击查询，显示出手机号归属地和运营商；
> 2. 这个功能需要提供 API 的版本，传入一个手机号，返回一个 JSON 格式的归属地和运营商标识；
> 
> 非公能性需求：
> 1. 因为可能有巨量的查询，应该有比较好的性能，所以考虑把结果缓存起来；

首先，我们来建立一个最简单的项目，先建立一个项目文件夹叫 mobile-search，然后在该目录下，用 lapis 命令创建项目基础文件：

```shell
root@deb8➜  Projects  mkdir mobile-search
root@deb8➜  Projects  cd mobile-search
root@deb8➜  mobile-search  lapis new
wrotenginx.conf
wrotemime.types
wroteapp.moon
wrotemodels.moon

```

这样项目脚手架就做出来了。执行`lapis server`，nginx 就会启动了。然后，我们访问 `http://localhost:8080`，然后，你可能会遇到 Internal Server Error 500。原因是找不到 `app.lua`，Lapis 框架同时支持两种语言，Lua 和 MoonScript，后者是前者的语法的一种美化和简化，相当于 CoffeeScript 之于 JavaScript。在实际执行的时候，MoonScript 需要被编译成 Lua 才能工作。Lapis 默认是使用 MoonScript 作为原生语言的，所以，我们刚生成的是使用 MoonScript 语言的模板，没有执行编译的过程，所以，`app.lua` 还没有编译出来。

同样使用 LuaRocks 我们来安装 MoonScript 的软件包，然后使用编译器编译 MoonScropt：

```shell
root@deb8➜  mobile-search  luarocks install moonscript
Warning: falling back to curl - install luasec to get native HTTPS support
Installing https://luarocks.org/moonscript-0.5.0-1.src.rock
Missing dependencies for moonscript 0.5.0-1:
   alt-getopt >= 0.7 (not installed)

moonscript 0.5.0-1 depends on alt-getopt >= 0.7 (not installed)
Installing https://luarocks.org/alt-getopt-0.8.0-1.src.rock
alt-getopt 0.8.0-1 is now installed in /usr/local (license: MIT/X11)

moonscript 0.5.0-1 is now installed in /usr/local (license: MIT)

#编译当前目录下的所有 `.moon` 文件
moonc .
#监视当前目录下所有 .moon 文件的变化，如果变了，就自动编译
moonc -w .

```

之后再次执行 `lapis server` 你会看到，Welcome to Lapis 1.6.0!，可以开工了。

## 数据库连接

首先，我们来看看我们要做的 Demo 的表结构。我去淘宝上 2 块钱买了一个用于查询手机号码归属地的数据库，用来完成这次的 Demo。以下是这个数据的表结构：

```sql
CREATE TABLE `phonenumber_info` (
  `id` int(11) NOT NULL COMMENT '条目ID',
  `prefix` varchar(6) DEFAULT NULL COMMENT '号码前缀',
  `mobile_type` varchar(50) DEFAULT NULL COMMENT '号码类型',
  `phone_header` varchar(20) NOT NULL DEFAULT '' COMMENT '号码前7位',
  `province` varchar(20) DEFAULT NULL COMMENT '省',
  `city` varchar(20) DEFAULT NULL COMMENT '市',
  `area_code` varchar(30) DEFAULT NULL COMMENT '区号',
  `postcode` varchar(20) DEFAULT NULL COMMENT '邮编',
  PRIMARY KEY (`phone_header`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

手机号码归属地查询的原理不难理解，就是使用手机号码的前 7 位数字（`phone_header`），查询对应的条目，查到后，展示`province` 字段和 `city` 字段的值，也可以显示当地的区号和邮编。

首先，我们来创建一个配置文件，进入到 `mobile-search` 目录，创建一个名为 `config.moon` 的文件：

```lua
-- config.moon
config = require "lapis.config"

config "development", ->
    mysql ->
        host "172.16.57.1"
        user "mobile"
        password "mobile"
        database "mobile"

```

然后，我们可以测试一下，配置文件是否有效。我们打开 `app.moon` 来编辑一下：

```lua
-- app.moon
lapis = require "lapis"

-- 增加如下这行
db = require "lapis.db"

-- 在路由 “/” 里面，执行一条 raw 的查询
class extends lapis.Application
  "/": =>
    res = db.query "select * from phonenumber_info where phone_header like ?", '1851623'
    "Welcome to Lapis #{require "lapis.version"}!"

```

然后，我们访问 `http://localhost:8080` ，又看到了：Welcome to Lapis 1.6.0! 并且，我们在 shell 的 log 里看到：

```shell
2017/08/17 23:55:17 [notice] 5429#0: *6 [lua] [C]:-1: [200] GET / - {  }, client: 127.0.0.1, server: , request: "GET / HTTP/1.1", host: "127.0.0.1:8080"
2017/08/17 23:55:17 [notice] 5429#0: *8 [lua] mysql.lua:104: query(): SQL: select * from phonenumber_info where phone_header like '1851623', client: 127.0.0.1, server: , request: "GET / HTTP/1.1", host: "127.0.0.1:8080"
2017/08/17 23:55:17 [notice] 5429#0: *8 [lua] [C]:-1: [200] GET / - {  }, client: 127.0.0.1, server: , request: "GET / HTTP/1.1", host: "127.0.0.1:8080"

```

这些迹象表明，我们的数据库连接已经通了。我们把代码优化一下：

```lua
class extends lapis.Application
  "/": =>
    res = db.query "select * from phonenumber_info where phone_header like ?", '1851623'
    item = res[1]
    @html ->
        ul ->
            for k,v in pairs item
                li ->
                    p "index: #{k}, value: #{v}"

```

改完，我们刷新页面，发现了乱码，把编码格式改成 utf-8 后，我们看到：

```shell
  Lapis Page
  
    index: province, value: 上海
    index: phone_header, value: 1851623
    index: prefix, value: 185
    index: id, value: 271321
    index: postcode, value: 200000
    index: area_code, value: 021
    index: city, value: 上海
    index: mobile_type, value: 联通185卡


```

其实，到这里，我们的第一个需求，竟然就已经实现了（从本质上看）。剩下的，就是美化的工作了。

## 使用 Model

Lapis 框架是提供 Model 这个抽象形式的。跟一般的 Web 框架区别也是不大的，一个 Model 代表着一张数据库的表，一个实例代表着数据库表里的一行记录。

定义一个 Model 最简单的办法是使用约定。数据库表用下划线分割的小写单词的话，Model 名字用对应的驼峰命名法。

```lua
lapis = require "lapis"
-- Model 的基类
import Model from require "lapis.db.model"

-- 具体的 Model
class PhonenumberInfo extends Model
    @primary_key: "phone_header"

class extends lapis.Application
  -- 规划 URL
  "/mobile-search/:number": =>
    entry = PhonenumberInfo\find string.sub @params.number, 1, 7
    @html ->
        ul ->
            for k,v in pairs entry
                li ->
                    p "index: #{k}, value: #{v}"

```

app.moon 代码经过改写后，变成上面的样子。表名是 `phonenumber_info`，则 Model 名为 `PhonenumberInfo`。参见这个表的建表语句，我们看到这个表的主键不是缺省的 `id` 字段，所以，用 `@primary_key` 指定主键的字段。

Lapis 的 Model 封装了一系列的单行变量的操作方法。insert，select，update，delete等等，也实现了 relation 等 ORM 层常见的功能。

## View 的使用

我们再来看看，视图是怎么使用的，在 Lapis 里面，支持 etlua 的一个模板库。只要开启模板库，就可以使用 render 方法来输出内容。

我们在 `mobile-search` 目录下，创建一个目录叫 views，这也是一种约定。在里面放一个模板文件，叫 `result.etlua`：

```shell

    号码类型：<%= mtype %>
    归属地：<%= province %> <%= city %>


```

写入如上的内容。

然后，我们把 app.moon 改成：

```lua
lapis = require "lapis"
import Model from require "lapis.db.model"

class PhonenumberInfo extends Model
    @primary_key: "phone_header"

class extends lapis.Application
  -- 注意这个地方
  @enable "etlua"

  -- 规划URL
  "/mobile-search/:number": =>
    entry = PhonenumberInfo\find string.sub @params.number, 1, 7
    @mtype =  entry.mobile_type
    @province = entry.province
    @city = entry.city
    -- "result" 是模板的名字
    render: "result"

```

经过上面的方法，我们把复杂的 HTML 给挪到了代码外面做到了逻辑和表现分离。

## 项目代码组织

经过上面的一些改造，基本体验到了 MVC 中的 M 和 V，但是没有 C，就我自己目前学习的知识看，这个框架里是没有C这个抽象的，本质上就是 Application，这个框架的抽象认为，一个网站，就是由一系列的 Request 和 Action 组成的。Request 通过 URL 的 path 映射到 Action，Application 就是用来组织这种映射的地方。那么复杂的业务逻辑怎么组织呢，可以放到 Application 的子类里面，切小后，放到子目录里。

让我们来试试。

创建一个目录叫 applications ，然后，在里面创建一个文件叫 search.moon 用来把逻辑组织在一个单独文件，然后分出去，然后再建个目录叫 models，把刚才的 Model 也挪出去。

```shell
root@deb8➜  mobile-search  tree .
.
├── applications
│   └── search.moon
├── app.moon
├── client_body_temp
├── config.moon
├── fastcgi_temp
├── logs
│   ├── access.log
│   ├── error.log
│   └── nginx.pid
├── mime.types
├── models
│   └── phone.moon
├── models.moon
├── nginx.conf
├── nginx.conf.compiled
├── proxy_temp
├── scgi_temp
├── uwsgi_temp
└── views
    └── result.etlua

```

目录布局就是上面这个样子。

```lua
-- --------------------
-- app.moon 变为
-- --------------------
lapis = require "lapis"

class extends lapis.Application
   @include "applications.search"

   "/": =>
       "Welcome!"


-- --------------------
-- search.moon 里面是
-- --------------------
lapis = require "lapis"

import
    PhonenumberInfo
    from require "models"

class MobileSearch extends lapis.Application
    @enable "etlua"
  -- 规划URL
  "/mobile-search/:number": =>
    entry = PhonenumberInfo\find string.sub @params.number, 1, 7
    @mtype =  entry.mobile_type
    @province = entry.province
    @city = entry.city
    render: "result"

-- --------------------
-- phone.moon 里面是
-- --------------------
import Model from require "lapis.db.model"

class PhonenumberInfo extends Model
    @primary_key: "phone_header"


```

## 压测

还是很好奇这个东西的性能的吧，哈哈哈

```shell
~  ab -n 10000 -c 10 http://172.16.57.128:8080/mobile-search/18516231234
This is ApacheBench, Version 2.3 <$Revision: 1757674 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 172.16.57.128 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        openresty/1.11.2.4
Server Hostname:        172.16.57.128
Server Port:            8080

Document Path:          /mobile-search/18516234722
Document Length:        180 bytes

Concurrency Level:      10
Time taken for tests:   79.270 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      3290000 bytes
HTML transferred:       1800000 bytes
Requests per second:    126.15 [#/sec] (mean)
Time per request:       79.270 [ms] (mean)
Time per request:       7.927 [ms] (mean, across all concurrent requests)
Transfer rate:          40.53 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   1.0      2       5
Processing:    48   78   6.8     77     124
Waiting:       47   77   6.8     76     123
Total:         50   79   6.8     79     124

Percentage of the requests served within a certain time (ms)
  50%     79
  66%     82
  75%     84
  80%     85
  90%     87
  95%     91
  98%     93
  99%     96
 100%    124 (longest request)

```

对比一下同一台机器上的 PHP + Apache 

```php
$mobile = $_GET['phone'];
//持久连接
$link = mysqli_connect("p:127.0.0.1", "root", "root", "mobile");
$ret = mysqli_query($link, "select * from phonenumber_info where phone_header=$mobile limit 1");
$data = $ret->fetch_assoc();
var_dump($data);

```

结果，才跑完2000，我有点舍不得跑了，风扇那个吹啊，改成2并发，100请求：

```shell
ab -n 100 -c 2 "http://local.karl.com/mobile.php?phone=1851623"
This is ApacheBench, Version 2.3 <$Revision: 1757674 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking local.karl.com (be patient).....done


Server Software:        Apache
Server Hostname:        local.karl.com
Server Port:            80

Document Path:          /mobile.php?phone=1851623
Document Length:        315 bytes

Concurrency Level:      2
Time taken for tests:   13.351 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      47100 bytes
HTML transferred:       31500 bytes
Requests per second:    7.49 [#/sec] (mean)
Time per request:       267.013 [ms] (mean)
Time per request:       133.507 [ms] (mean, across all concurrent requests)
Transfer rate:          3.45 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:   258  267   5.9    267     288
Waiting:      258  267   5.9    267     288
Total:        258  267   5.9    267     289

Percentage of the requests served within a certain time (ms)
  50%    267
  66%    268
  75%    269
  80%    270
  90%    275
  95%    279
  98%    289
  99%    289
 100%    289 (longest request)

```

注意，上面压测，完全胡乱玩的，请勿胡乱参考。对 Lapis 的压测是，Debian 8 虚拟机，1核1G，OpenResty 1.11.2.4 + Lapis 1.6.0，压得时候还开着调试模式，而 PHP 呢，是 Debian 的宿主机，iMac，i7 4GHz 4核16G，Apache 2.x + PHP_Module 7.1.6，完全不对等的配置，也未做调优等等。主要是我心里也知道，一个是纯异步通信，一个是同步的，这个根本就没有太大比的必要，PHP真要认真测，应该也没这么烂，主要我写得辛苦，也懒得花时间去努力测试了，诸君谅解。真想参考性能，[请看这个](http://www.techempower.com/benchmarks/#section=intro&hw=ph&test=json)。