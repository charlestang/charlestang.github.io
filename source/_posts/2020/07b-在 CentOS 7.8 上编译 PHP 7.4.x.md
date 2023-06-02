---
title: 在 CentOS 7.8 上编译 PHP 7.4.x
tags:
  - CentOS
  - compile
  - Linux
  - PHP
id: '922'
categories:
  - [工作相关, PHP]
date: 2020-07-03 18:52:35
permalink: compile-php74-on-centos78/
---

昨天，我在一台 CentOS 6.10 上面编译 PHP 7.4.7 和编译前几个版本有很大的区别，PHP 7.4 开始使用了一个叫 pkg-config 的东西，有点先进，但是在老旧的系统上，真是无比痛苦的一个体验。

今天我尝试一下在 CentOS 7.8 上面编译一下，之前没有干过，我就记录一下过程，虽然无聊得很，但是记录下来，可以给以后节省点时间。
<!-- more -->
```shell
yum install -y systemd-devel.x86_64
yum install -y libxml2-devel.x86_64
yum install -y openssl-devel.x86_64
yum install -y sqlite-devel.x86_64
yum install -y libcurl-devel.x86_64
yum install -y libpng12-devel.x86_64
# 注意，看你的系统里是 libpng 后面的数字是几
ln -s /lib64/pkgconfig/libpng12.pc /lib64/pkgconfig/libpng.pc
yum install -y libwebp-devel.x86_64
yum install -y libjpeg-turbo-devel.x86_64
yum install -y freetype-devel.x86_64
yum install -y oniguruma-devel.x86_64
yum install -y readline-devel.x86_64
yum install -y libzip-devel.x86_64

# 手动编译 libzip
yum install -y cmake3
yum install -y bzip2-devel.x86_64
wget https://libzip.org/download/libzip-1.7.1.tar.xz
tar xf libzip-1.7.1.tar.xz
mkdir build
cd build
cmake3 -DENABLE_GNUTLS=OFF ..
make
make test
make install

# 进入 php-7.4.7 目录
PKG_CONFIG_PATH="/usr/local/lib64/pkgconfig" \
./configure -C \
  --prefix=/usr/local/php7 \
  --enable-fpm \
  --with-fpm-systemd \
  --with-openssl \
  --with-zlib \
  --enable-bcmath \
  --with-curl \
  --enable-exif \
  --enable-gd \
  --with-webp \
  --with-jpeg \
  --with-freetype \
  --with-gettext \
  --enable-mbstring \
  --with-mysqli \
  --with-mysql-sock=/var/lib/mysql/mysql.sock \
  --enable-pcntl \
  --with-pdo-mysql \
  --with-readline \
  --enable-soap \
  --enable-sockets \
  --with-zip \
  --enable-mysqlnd

# 开始编译，使用 2 核
make -j2
make test
make install
```

PHP 7.4.7 版本，我编译下来感觉就是，使用了 pkg-config 这个工具来自动识别 lib 库所在的位置，这个工具是很强大的，但是遗憾的是，不够普及，不是每个包都正确带有了自己的 pkgconfig 文件，以 `.pc` 结尾的。

编译中遇到的麻烦，都是这个问题带来的，比如上面的执行记录里，就可以看到，libpng，这个依赖，使用 yum 安装的包，名字竟然叫 libpng12，我做了一个软链，绕过了这个问题。但是不是每次都这么顺利的。

另一个问题就是 libzip，系统里只有 0.10 版本的，但是编译 PHP 7.4+ 需要 0.11 版本，yum 就解决不了这个问题了，只能使用一些私有的源。当然，如果使用私有源，就可以直接安装现成的 PHP 7.4+ 了，没必要编译这么痛苦了，我觉得如果没有什么必要性，还是用网上的私有源安装比较好，还会带有全套的运维脚本，比自己编译方便太多了。

文件拷贝完了，下面还有一个步骤，就是各种配置文件的设置和启动。

```shell
cp php-7.4.7/php.ini-production /usr/local/php7/lib/php.ini
# 上面把生产环境的 php.ini 文件拷贝过去
cd /usr/local/php7
mv etc/php-fpm.conf.default etc/php-fpm.conf
mv etc/php-fpm.d/www.conf.default  etc/php-fpm.d/www.conf
#上面三行，拷贝好 php-fpm 的配置文件
cp php-7.4.7/sapi/fpm/php-fpm.service /usr/lib/systemd/system/
# 安装 systemd 运维脚本
sudo systemctl enable php-fpm
sudo systemctl start php-fpm
sudo systemctl status php-fpm
# 以上，php-fpm 就会被启动并且守护，注意看  status 里面的信息
```

我在执行的时候，遇到了一个 exit code = 78 的错误，就是 fpm 的 error_log 文件没能创建导致的，可以手动创建，或者更改一个路径，因为我们 prefix 选了 /usr/local/php7，所以 log 也在这下面，不太建议，可以设定到 /var/log 或者 /data/log 下面，看各自服务器运维的规范了。

新版的 php 越来越完善了，带有了各种操作系统的运维脚本，有 Debian 系的，也有 CentOS 系的，sapi 这个目录里，有各种各样的服务器接口支持，Apache 的，FastCGI 的，甚至还有商业服务器 LightSpeed 的，应有尽有。应该多看看这个目录里的文件，总好过网上胡乱找的运维脚本。