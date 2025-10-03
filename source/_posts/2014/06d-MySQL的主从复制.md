---
title: MySQL的主从复制
tags: []
id: '633'
categories:
  - - 技术
    - 后端
permalink: mysql-replication/
date: 2014-06-24 00:14:19
---

如果数据库只有一份，那就是数据存储的单点，对于要求可靠性的服务来说，就存在一个单点故障的可能性，这个时候，我们就要通过复制镜像，来解决单点故障。复制还有一个额外的好处，就是可以根据主从，做读写分离，这样，就不会在写入的时候，因为锁表，而降低MySQL的并发性能，所以MySQL复制是MySQL中非常基础的一种操作。

## 怎么配置

### 配置Master

首先，要做的是确定一个Master，对于充当Master的MySQL Server来说，需要一些特定的配置才能实现，一个是开启binlog，另一个是要设置server－id。

`[mysqld] log_bin = mysql-bin server-id = 1`

### 配置Slave

配置Slave，对于Slave来说，要配置的就是一个唯一的server-id。这个id不能跟Master相同，而且，多个Slave也不能相同。配置完毕后重启。

`[mysqld] server-id = 2`

### 创建User

在Master创建一个user，专门用于进行复制用途的。因为在Slave上，user和password会被用明文存储，所以，这个user的权限要尽可能的小，一定要不同于超级用户。

`create user repl@'your.domain' identified by 'password'; grant replication slave on *.* to repl@'your.domain';`

注意，这里第2句，grant语句，必须是赋权限给*.*的，因为replication slave权限是一个global privileges，所以，必须这样，如果想要限制权限在一个比较小的范围，不想复制所有的db的话，可以在my.cnf增加配置项replicate-do-db和binlog-do-db来限定数据库的范围。

### 获取Master的位置

在Master的数据库上，知行flush tables with read lock;语句，然后知行show master status;这时候，就可以看到当前的binlog文件名和当前知行的sql语句位置。将文件名和执行的位置都记录下来。

这时候，如果Master的数据库的内容非空的话，应该做的事情，就是使用mysqldump来导出数据。空数据库的话，就没必要做什么事情了。

### 建立连接

在上文空数据库的情况下，是很简单的，stop slave，直接在slave上使用change master to语句，将各项参数设置完毕后，就可以执行start slave了。

如果Master原来有数据，应该把刚才生成的dump文件，传送到slave上，然后首先stop slave，然后导入dump的数据，然后执行change master to语句，将刚刚dump前记录的bin文件和位置都设置正确，然后才能start slave，其实也不麻烦。

## 状态检查

在比较理想的世界里，到这里，我们的工作就结束了，但是，世界是不理想的，因为各种原因，这种replication的联系，经常会中断的。所以要时不时检查这个联系。

在Master上可以执行show master status看到的东西和上面看到的是一样的。

在Slave上可以执行show slave status，可以看到很多的信息和错误提示。一般情况下是没错的，一旦发生错误了，就应该从这里获取相应的信息来解决问题。