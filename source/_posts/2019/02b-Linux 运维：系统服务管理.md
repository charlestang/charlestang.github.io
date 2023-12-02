---
title: Linux 运维：系统服务管理
tags:
  - Linux
  - shell
id: '803'
categories:
  - [工作相关, Linux]
  - [日　　记]
date: 2019-02-28 01:49:30
permalink: linux-management-sys/
---
我发现，每隔一段时间，运维 Linux 服务器的方法，就会变迁一次，害得我总是要重复学习这件事情，真是太不友好了。Linux 服务器运维的方法不是一种半衰期很长的技巧么？世道都变了啊……

## Ubuntu 桌面系统初始化

这两天安装了一个 Ubuntu 19.04 Desktop 到我的最老的 Macbook Pro上面，打算当成家庭的 Server 使用的。

```shell
# 1. 说实在的，我就看不出来这个新版的 apt 命令有什么好用的
#    当然，底层的命令 apt-get 和 apt-cache 更难用
apt install aptitude
# 2. 替换掉 vim-tiny，不知道这么多年过去了，为什么还是这样
aptitude remove vim-tiny
aptitude install vim
# 3. 桌面版连个 netstat 命令也没有，装一下（推荐使用 ss 命令代替）
#    不是梯子的 ss，我没写错，就是 ss 命令
aptitude install net-tools
```
## CentOS 检查系统已注册服务

```shell
# 注意：从 CentOS 7 开始，已经不推荐使用 chkconfig 了
# 检查有哪些注册了的服务（SysV 流派的系统服务，迟早会被新的方式取代的一种）
chkconfig --list
# 关闭这种流派的服务：在2，3，4，5四个run level下关闭名叫 agentwatch 的服务
chkconfig --level 2345 agentwatch off
# 删除指定名字的服务：删除名叫 agentwatch 的服务
chkconfig --del agentwatch
# 检查有哪些注册了的服务（systemd 流派的系统服务，CentOS 7+）
systemctl list-units
# 只列出 service 类型的
systemctl list-units --type service
# 禁用服务：禁用一个名叫 aegis.service 和 agentwatch.service 的服务
systemctl disable aegis
systemctl disable agentwatch
systemctl status agentwatch
rm /etc/init.d/agentwatch
rm /etc/systemd/system/aliyun.service
rm /usr/sbin/aliyun-service
rm /usr/sbin/aliyun-service.backup
# 如果手动暴力删除了一些 service 的配置文件
systemctl reset-failed
systemctl list-units --type service
# 执行上述两个命令，发现没有残留了
```
## CentOS 上安装支持 BBR 的 kernel

*   [什么是BBR？](https://github.com/google/bbr)
*   [BBR原理以及有什么作用？](https://cloud.google.com/blog/products/gcp/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster)
*   [BBR 论文](https://queue.acm.org/detail.cfm?id=3022184)
*   [怎么在 CentOS 7 上启用 BBR](https://yeahlinux.com/how-to-get-google-bbr-on-centos-7/)（英文）

```shell
# 查看当前的发型版本
cat /etc/*release*
# 导入新的 repo，参见 http://elrepo.org/tiki/tiki-index.php
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
# 安装与 CentOS 7 对应的 rpm 包
yum install https://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
# 检索对应的 kernel 包
yum --enablerepo=elrepo-kernel search kernel-ml
# 安装正确的 kernel 包
yum --enablerepo=elrepo-kernel install -y kernel-ml.x86_64
# 确认安装了哪些 kernel 包
rpm -qa  grep kernel
# 查看目前的配置
egrep ^menuentry /etc/grub2.cfg  cut -f 2 -d "'"
# 这步骤之后，机器需要重启，然后确认现在内核的版本号
uname -a 
# 启用 BBR
echo 'net.core.default_qdisc=fq'  tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=bbr'  tee -a /etc/sysctl.conf
sysctl -p
# 确认 BBR 是否启动
lsmod  grep bbr
```
## 在 Linode 上申请了一台 CentOS 7

最近，腾讯云审核非常严格，于是我又购买了一台 Linode 的服务器来玩，以防万一，按照以前我的性格，我会选 Debian 9 发型版的，但是最近比较偏爱 CentOS，就选择了 CentOS 7，其实，CentOS 8 也出来了，不过真的鬼使神差还是选了 7。

按照我一贯的做法，先要更换 SSH 的端口号的，主要是为了安全，感觉在互联网上非常奇怪，出现一台新的开放端口的机器后，常用端口就立刻会被不断攻击，所以，我习惯的做法是立刻把各种要命的服务都改成冷门的端口号。

没想到，Linode 上生成的 CentOS 7 实例机器，竟然默认了非常多的安全设置，让我完全没有想到。

首先是 SELinux，我挣扎了半小时，还是放弃了，这么多年来没有打起勇气搞明白这东西，感觉实在太麻烦了。

编辑 /etc/selinux/config 文件，将 SELinux 切换到 disabled，然后重启服务器。可以彻底关闭 SELinux，然后我在 56000 端口开启 SSH，没想到还是连不上，iptables -L 发现，竟然还有 iptables，当我尝试 systemctl stop iptables 的时候，发现告诉我，系统没有 iptables.service 的 unit，这就让我摸不着头脑了。

网上继续搜索，发现，CentOS 7 默认使用的是 firewalld 这个服务，真是让人晕头转向，又简单研究了一下 firewalld 的用法。

```shell
# 检测 firewalld 是否开启，显示 running 就是开启着
firewall-cmd --state
# 列出当前开启了哪些服务，发现有 dhcpv6-client 和 ssh
firewall-cmd --list-service
# 然后加入你要增加的端口
firewall-cmd --permanent --service=ssh --add-port=56000/tcp
# 重新加载配置
firewall-cmd --reload
```

这里我 Link 一篇文档，非常赞，以备查阅《[Understanding Firewalld in Multi-Zone Configurations](https://www.linuxjournal.com/content/understanding-firewalld-multi-zone-configurations)》。这篇文档详细介绍了 firewalld 的原理，以及操作范例，看完基本都明白了，很不错。

在这台 CentOS 上，我想使用 yum 源来安装 ss-libev，没想到遇到了很大的阻碍，以前我在阿里云的 CentOS 实例上，轻松可以 yum install 的东西，在这里竟然遇到了很大的阻碍，折腾了两三天竟然还没有装成功，Linode 的默认实例配置里，添加了 ss-libev 的源后，发现缺少两个关键的依赖，libsodium 和 libmbedlts 两个东西，我尝试手动编译安装了 libsodium 发现并不行，因为 rpm 是个体系，手动编译不能补充这个依赖，它只认自己数据库里面的数据。

这下有点麻烦，于是我想到了换源，是不是 Linode 服务器提供的 yum 源有问题，尝试换成 163 的源，然而不管用，再尝试换成阿里云的源（我先尝试了这个，拷过来是不行的，因为可能是私有的域名或者只对国内 IP 开放更新的），换阿里云的办法是：

```shell
# 首先是备份原有的文件
cd /etc/yum.repos.d
mv CentOS-Base.repo CentOS-Base.repo.linode.backup
# 然后是下载阿里云的 repo 文件代替
curl -o CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
# 然后是更新缓存
yum makecache
yum update
```

然后搞笑的是，我更换了阿里云的源发现，竟然仍然无法正常用 yum 安装 ss-libev，还是那两个依赖解决不了，实在无语了暂时还没搞明白怎么回事。然后我打算放弃治疗手动安装算了，libev 的 GitHub 官方页面推荐使用 snapcraft.io 来安装，所以我顺便看了一眼怎么安装 snapcraft.io，第一个步骤是给 yum 增加 epel repository。

```shell
sudo yum install epel-release
```

然后我灵机一动，难道这就是我苦寻的遗失的源？一试，果不其然，那我也不用编译安装了，直接成功 yum install 了。到此，我又把阿里云的源换回去了，说实在不怎么信任阿里云。万一参杂点私货呢？对吧。

这里再记录一下，怎么用 Screen 去后台长期运行一个程序：

```shell
screen -dmS SessionName /bin/cmd -o options
# -d -m 这两个参数组合起来的意思是，不要启动 screen，而是直接 detach 状态执行命令
# -S 的意思是给这个 Session 取个名字
```

我这里 Link 一篇文档以备查阅《[使用 Screen 管理你的远程会话](https://www.ibm.com/developerworks/cn/linux/l-cn-screen/index.html)》。

## 低配置的服务器临时增加 swap 来编译

今天在以前买的腾讯云服务器上编译 PHP ，发现竟然因为内存不够被杀掉了，得增加 swap 文件来，解决内存不够无法编译的问题：

```shell
# 首先检查一下现在系统的内存，单位用 MB
free -m 

# 看到服务器没有配置任何 swap，total = 0
# 看看是否有已经定义的 swap 文件
swapon -s

# 看到没有任何文件
# 然后来格式化一个 swap 分区，512M
dd if=/dev/zero of=/swapfile bs=1024 count=512k

# 然后在上面创建一个 swap 空间
mkswap /swapfile

# 激活 swap，然后使用上面的 swapon -s 检查是否成功
swapon /swapfile

# vi /etc/fstab，在里面最后一行配置
/swapfile          swap            swap    defaults        0 0

# 修改文件权限
chown root:root /swapfile 
chmod 0600 /swapfile

# 最后用 free -m 看看 swap 的 total 增加了没有
# 看看操作系统依赖 swap 的频繁度
cat /proc/sys/vm/swappiness

# 默认值是 60，太频繁使用 swap 会拖慢速度，毕竟内存更快
sysctl vm.swappiness=10

# 改低这个参数，done。
```

使用上面的步骤，就完成了 swap 的添加，然后再次尝试编译，成功了。

以上内容引自：[《How To Add Swap on CentOS 6》](https://www.digitalocean.com/community/tutorials/how-to-add-swap-on-centos-6)

这个过程的逆过程就比较简单了：

```shell
# 关闭 swap
swapoff -a

# 确认
swapof -s

# 看到没有文件了
vi /etc/fstab 

# 去掉关于 swap 的配置
rm /swapfile 

# 就彻底删掉了 swapfile
```

## 在 Ubuntu 20.04 上安装 MySQL

其实毫无难度的，就是用 apt install mysql-server 就可以了。我这里想说的是，装完了以后，怎么登录进去呢？整个安装过程是没有交互式的。

你可以 sudo mysql，直接用 root 权限调用客户端，就会以 root 身份登录了，不需要密码。
```shell
mysql -uroot -p
```
首次安装好数据库后，不需要密码，直接按回车就可以登录进去了。值得一提的是，现在创建用户和密码的方法变了。
```mysql
create user admin@localhost identified by '123@qwe';
```
上面的用户定义了一个本地用户，密码是 `123@qwe`，我以前喜欢用`Grant`语句直接授权和创建用户和密码，现在似乎是不行了。
```mysql
grant all privileges on db_name.* to admin@localhost;
```
上面的语句是授权用户访问一个数据库的语句，`privileges` 关键字不是必须的，可以省略。

然后需要执行：
```mysql
flush privileges;
```
关于这一点，腾讯有一片文章介绍得不错：

[《如何在 Ubuntu 20.04 上安装 MySQL》](https://cloud.tencent.com/developer/article/1622599)

## 如何在 Ubuntu 20.04 上安装 PHP

也说个简单的做法，就是用 apt install php-fpm，如果你是安装 php 这个包，你会发现海量的依赖，会把整个 apache 2 都给带出来。因为默认是这样的。

不过 nginx 伺服静态文件要好一点，所以，现在流行 LNMP 多一点，你可能不想安装 apache 2，那么你就应该安装 php-fpm 这个包。

使用 apt 的好处是，以后升级的时候，简单一点。如果没有逼到非要自己编译，最好不要自己编译，实在麻烦而且无趣，当然并不难。

## 首次在 CentOS 服务器上安装 MySQL

安装服务器比较简单：
```shell
yum install mysql-server.x86_64
```
装完服务器后，服务器默认是不启动的，使用 systemctl 命令进行启动
```shell
systemctl start mysqld.service
```
然后，root 的初始密码是什么呢？
```shell
mysql -uroot -p
```
你会发现，MySQL 初始并未设置密码，比较安全的方式是，你登录成功后，马上设置一个新的密码，使用命令：
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '你的密码';
FLUSH PRIVILEGES;
```
即可完成 root 密码的设定。
