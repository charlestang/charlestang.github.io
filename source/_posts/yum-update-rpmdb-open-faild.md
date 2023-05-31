---
title: 使用 yum update 遇到 rpmdb open faild
tags:
  - DevOps
  - Linux
  - maintain
id: '1004'
categories:
  - - 日　　记
date: 2021-02-22 21:22:50
---

真是活久见了，当我使用 `yum update` 命令的时候，发现竟然报错了：

```generic
yum update
error: rpmdb: BDB0113 Thread/process 4196/140144005818432 failed: BDB1507 Thread died in Berkeley DB library
error: db5 error(-30973) from dbenv->failchk: BDB0087 DB_RUNRECOVERY: Fatal error, run database recovery
error: cannot open Packages index using db5 -  (-30973)
error: cannot open Packages database in /var/lib/rpm
CRITICAL:yum.main:

Error: rpmdb open failed
```

都怪我之前写了各种自动守护脚本，导致服务器上跑的各种服务长久都没什么抖动，于是乎，我很久也不用登录了，不过今天还是跑飞了，上去看看，服务死了，而且 systemd 没有拉起来，太奇怪了。

手动执行了 `systemctl restart` 后，我想起来久没上来，应该更新一下子，就报错了。从来没见过这个错误，这次可能真的一年多没更新了吧。

搜到了解决方案：

```shell
# 第一步，备份文件，建议做备份
mkdir /root/backups.rpm.mm_dd_yyyy/
cp -avr /var/lib/rpm/ /root/backups.rpm.mm_dd_yyyy/

# 第二步，删除错误的文件，开始重建
rm -f /var/lib/rpm/__db*
db_verify /var/lib/rpm/Packages
rpm --rebuilddb
yum clean all
```

一次尝试成功，可以愉快的 `yum update` 了。

当然以上解决方案来自 [SO](https://unix.stackexchange.com/questions/198703/yum-errorrpmdb-open-failed)。