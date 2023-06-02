---
title: Linux 运维：SSH 服务的最佳实践
tags:
  - Linux
  - shell
  - ssh
id: '804'
categories:
  - [工作相关, Linux]
date: 2019-03-01 00:17:05
permalink: ssh-best-practices/
---

最近又提起了兴趣去折腾 VPS，买好一台新的 VPS 服务器后，第一件事情就是登上去设置环境，当然，SSH 登录必不可少，这也是远程操作一台服务器的先决条件。不过 SSH 服务器，默认不是按照最优的方式去配置的。所以，我打算自己总结一下 SSH 服务的最佳实践。

## 安装 ssh 服务器

如果购买的是一般云计算的 VPS 服务器，当然是没有这个过程了，不可能没有安装 ssh 服务器的。如果想把自己淘汰的旧电脑变成一台 Linux Server 的话，可能就会遇到这个问题。例如，我昨天把自己 2009 年的一台 Macbook Pro 安装上了 Linux，我选择了使用最为广泛的 Ubuntu，选择了最新的 19.04 版本，主要希望它能对硬件有比较好的兼容性。

一般来说，在个人电脑上，最好的选择是安装 Desktop 版本，因为你毕竟有屏幕、键盘等输入输出设备，往往还有无线网卡，装成 Server 的话，想让它兼容你电脑上的各种硬件是很痛苦的，但是如果装成 Desktop 的话，想把它改造成一个提供服务的 Server 是很简单的。所以，我们一般都安装 Desktop 版本。

比较邪门的就是 Ubuntu 的 19.04 Desktop，竟然连 ssh server 都没有装，只有一个 ssh-client。

```shell
# 1.我觉得 apt-get 一点不好用，装个 aptitude 包管理器
apt-get install aptitude
# 2.检查 ssh 安装状态
aptitude search ssh
# 3.安装 ssh server
aptitude install openssh-server
# 4.检查服务状态
systemctl status ssh
# 5.到这里基本安装完毕了，以上在 Ubuntu 19.04 上测试过
```

## 禁止 root 用户直接登录服务器

新的 VPS 分配的时候，都是默认设置 root 用户，并且设法把密码发送给管理员知道。root 用户是 Linux 系统权限最高的用户，一旦泄漏了，后果不堪设想，黑客可以使用 root 的权限完全控制一台服务器。

比较好的做法是，禁止 root 账户直接登录到服务器上，因为如果允许 root 登录，就可能让黑客通过攻击直接得到 root 的权限。

比较好的实践方式是，设定一个非 root 的账户，用于日常登录使用，需要的时候，使用 sudo 临时取得权限，或在本地 shell 登录到 root 帐号。

```shell
# 使用 adduser 添加一个用户
adduser charles
# 使用 passwd 创建密码
passwd charles
# 使用 usermod 改变这个用户的 shell 为自己最喜欢的 zsh
usermod -s /bin/zsh charles
# 登录用户
su charles
# 进入用户的 home 目录
cd
# 创建 .ssh 目录
mkdir .ssh
# 创建公钥文件，用于注册可以登录的客户端
touch .ssh/authorized_keys
# 为了让这个用户得到执行 root 权限的能力，加到 sudoers 里面
gpasswd -a charles wheel
# 将一些环境变量带到 sudo 的环境（高级）
visudo
```

上面的代码，在系统里建立了一个新的用户，给这个用户创建一个密码，密码可以用于使用 sudo 命令。

然后使用 `gpasswd` 将用户加到 `wheel` 用户组，在 CentOS 上，就可以让用户得到 sodu 权限。 多年来我积累了一套自己使用非常习惯的 shell 配置，也建议读者这么做，可以去看看我的做法 https://github.com/charlestang/env.git 就会明白我在说什么。实现这套配置，环境变量少不了，比如 vim 的配置问题。

你可能会发现，sudo 后面使用 vim 的话，很多高级配置都无法生效。其他的命令也可能有这个问题。产生的原因其实是在一个用户的环境下设置的环境变量，使用 sudo 的时候，就会失去。可以通过代码片段的 visudo 命令，打开配置文件，指定要代入到 sudo 场景下的环境变量。

使用 sudo 会带来很多的不变，但是，作为一个运维人员，还是要养成不使用 root 的好习惯。各种小问题都是可以克服的。

## 使用基于公钥验证的登录

一般来说，购买一台服务器，新分配的时候都是默认用户名密码登录的，国内的阿里云、腾讯云都有这样的，国外的 Linode，前两天体验的 Vultr 也是。

但是，密码验证这件事情，在密码学里叫 PSK，pre-shared key，预先共享的。也就是至少有两方知道这个密码。而且，在公有云，是云平台设定的第一个密码，所以云平台是知道的。

更安全的方式，是使用非对称加密的方式，也就是基于公钥验证的登录。首先要在本地创建一个公私钥对，然后，把公钥注册到服务器的 `authorized_keys` 文件里。

```shell
# 在自己的电脑上创建 RSA 的公私钥对
ssh-keygen -b 4096 -t rsa
# 这个命令会在你的 ～/.ssh/ 目录创建 id_rsa 和 id_rsa.pub（公钥）文件
```

![](../images/2019/02/password-strength-1024x351.png)

插图节选自《HTTPS权威指南》

关于非对称密钥的长度问题，我看到 CentOS 7 的文档里面介绍，默认的 RSA 的长度是 2048 位，文档里认为足够了，而且建议的最短长度是 1024 位。上面的例子里，我特意用了 4096 位，哈哈，希望能用 30 年……插图选自一本技术书籍，内容是2012年，权威机构对密码长度和对抗强度的一个估算。

公钥文件配置在服务器的非 root 用户的 ~/.ssh/authorized_keys 文件里面，内容贴进去就可以了。一般来说，服务器缺省设置，都是支持使用公私钥验证进行登录的。下面是对`/etc/ssh/sshd_config`的配置；

```ini
# 开启公钥验证
PubkeyAuthentication yes
# 不允许 root 帐号登录
PermitRootLogin no
# 不允许使用密码验证登录
PasswordAuthentication no
ChallengeResponseAuthentication no
```

## 更换SSH服务的默认端口

SSH 服务的默认端口是 22，这个端口已经是全网皆知的了，也是网络上自动化工具攻击的首要目标，希望自己的服务器安全的话，就首先要把这个端口给更换掉。

推荐使用 10000 号以上的端口，设置的时候，可以这样：

```ini
# 1. 先新增一个监听的端口号，先不要删除 22 端口
Port 22
Port 10022
# 2. 重启 sshd 服务
> systemctl restart sshd
# 3. 退出登录，然后用自己的电脑去测试能否连接新的端口号
# 4. 如果登录成功，删除 Port 22，然后再次重启 sshd 服务
```

为什么按照上面的顺序操作？很多云服务器，都有默认的安全组或者防火墙配置，极有可能，默认情况下，除了 22 端口，其他都访问不了。所以，不要忙着取消 22 端口，而是先新增一个，测试一下联通性。不然，可能你退出了，就连不回来了。虽然，也不会有什么大的后果，但是会带来不少的麻烦。

## 优化SSH服务器端的性能

有一些常见的缺省设置，可能导致SSH服务的连接缓慢，简单调整参数，就可以使连接速度变快：

```ini
# 关闭 DNS，默认情况下，服务器会解析连接上来的服务器的域名（Hostname）
UseDNS no
# 这种验证方式也是拖慢连接速度的常见问题，其实在 CentOS 7中此项默认已经是 no 了
GSSAPIAuthentication no
```

## 总结

感觉还有很多的细小的点没有总结全，不过这个帖子可以放着，慢慢总结吧。