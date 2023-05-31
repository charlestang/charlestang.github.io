---
title: 在 CendOS 6.5 上编译 PHP 5/PHP 7
tags: []
id: '714'
categories:
  - - something-about-daily-work
    - PHP
  - - 工作相关
date: 2016-01-08 15:08:26
---


<!-- more -->
首先安装一些依赖的软件包：

```bash

yum install libmcrypt.x86_64 libpng.x86_64 libjpeg-turbo.x86_64 \
libxml2.x86_64 readline.x86_64 libxml2-devel.x86_64 openssl.x86_64 \
openssl-devel.x86_64 libcurl-devel.x86_64 libjpeg-turbo-devel.x86_64 \
libwebp-devel.x86_64 libpng-devel.x86_64 freetype-devel.x86_64 \
libmcrypt-devel.x86_64 readline-devel.x86_64 gcc.x86_64 pcre-devel.x86_64

```

然后是正确的配置 PHP7 的编译选项

```bash

./configure -C \
--prefix=/usr/local/php \
--with-readline \
--with-curl \
--with-gd \
--with-iconv \
--with-gettext \
--with-mcrypt \
--with-mysqli \
--with-openssl \
--enable-pcntl \
--enable-soap \
--enable-mbstring \
--with-zlib \
--enable-fpm \
--with-freetype-dir=/usr \
--with-jpeg-dir=/usr \
--with-webp-dir=/usr \
--with-png-dir=/usr

```

最后执行编译指令：

```bash

#使用2个核的意思，看CPU多少决定这个参数
make -j 2
make install

```

编译完了，要单独编译一下 opcache，虽然我觉得这个应该编译进去到 PHP 解释器里面，
但是目前，我只找到了以扩展方式使用的方法。

```bash

cd ext/opcode
/usr/local/php/bin/phpize
./configure --with-php-config=/usr/local/php/bin/php-config
make -j 2 
make install

```

然后编辑配置文件，添加：

```null

zend_extension=opcache.so

```

=====

下面是 PHP 5 的编译脚本：

```bash

#!/bin/bash

yum -yq install  \
libxml2-devel.x86_64 gcc.x86_64 \
openssl-devel.x86_64 libcurl-devel.x86_64 libjpeg-turbo-devel.x86_64 \
libwebp-devel.x86_64 libpng-devel.x86_64 freetype-devel.x86_64 \
libmcrypt-devel.x86_64 readline-devel.x86_64 libtool-ltdl-devel.x86_64

./configure -C \
--prefix=/usr/local/php \
--with-readline \
--with-curl \
--with-gd \
--with-iconv \
--with-gettext \
--with-mcrypt \
--with-mysqli \
--with-pdo-mysql \
--with-openssl \
--enable-pcntl \
--enable-soap \
--enable-mbstring \
--with-zlib \
--enable-fpm \
--with-freetype-dir=/usr \
--with-jpeg-dir=/usr \
--with-png-dir=/usr

```