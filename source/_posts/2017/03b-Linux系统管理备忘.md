---
title: Linux系统管理备忘
tags:
  - Linux
id: '451'
categories:
  - [工作相关, Linux]
date: 2017-03-08 16:26:41
permalink: linux-system-management/
---

如何知道自己用的是Linux还是Unix？
答：执行uname -a命令。

如何知道自己用的是哪个Linux发行版？
答：执行lsb_release -d命令。

如何知道当前系统时间？
答：执行命令date。

什么是UTC，CST和EDT？
答：UTC（=Universal Time Coordinated），协调世界时(过去曾用格林威治平均时GMT来表示)；EDT（=Eastern Daylight Time），美国东部夏令时间；CST（=Central Standard Time），美国中部地区标准时间，不过我个人认为还有一个意思（China Standard Time）就是中国标准时间，因为有时候，你会看到中国时间后面也会带个CST的。

如何修改系统时区？
答：各发行版不太一样，在最新的Ubuntu 11.04上，使用命令dpkg-reconfigure tzdata命令来修改时区，会弹出一个命令行下的字符图形界面，比较方便。在一般的Linux发行版上，可以尝试tzselect命令，可以通过命令行交互式地设置时区。

如何设定系统时间？
答：使用date --set="Sun Aug 21 10:13:43 CST 2011" 命令来设置，引号中的字符串，可以先用date命令来输出，然后修改时间到正确值，再设回去。

不知道mysql的root密码，如何重设？
答：停止mysql服务器，重新启动，增加--skpi-grant-tables参数重启服务器，不需要密码就可以登陆服务器，登陆后，UPDATE user SET password=PASSWORD(‘new_password’) WHERE user=’root’;使用该sql语句修改密码，修改完后，不要忘记执行flush privileges，然后退出，正常重启mysql服务器。