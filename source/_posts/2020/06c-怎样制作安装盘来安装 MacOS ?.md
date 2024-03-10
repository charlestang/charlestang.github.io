---
title: 怎样制作安装盘来安装 MacOS ?
tags:
  - install
  - mac
id: '915'
categories:
  - [工作相关, Linux]
  - [Mac]
date: 2020-06-09 14:04:04
permalink: how-to-reinstall-macos/
---

话说，不作死就不会死。

我的第一台 MacBook Pro，是一台 2009 Mid，真是有年头了，后来我换了电脑，就给了老爸，后来我又换了电脑，就把第二台给了老爸，老爸说第一台也没用了，还你吧，于是我现在多了一台闲置的 MBP 出来，还是 2009 Mid。

我之前就在家里跑了个树莓派 1 代，挺 Happy，想着，用 MBP 这逆天的性能，跑个 Linux，岂不是无敌了，于是开始了我作死之旅。

<!-- more -->

怎么自己制作安装盘，在一台 MBP 上安装 Linux，我不记得写没写过文章了，反正也是个作死之旅，现在想写也想不起来过程了。就记得我很激进选了个当时最新的 Ubuntu 19.04，为什么脑残得没选 LTS，我也是想给当时的自己一个大嘴巴子。装完以后，有点后悔，想退回 18.04 LTS，结果啪啪打脸，第二次制作的安装盘就装不了了，死活引导不了。

上个礼拜吧，我想 apt 一下，发现完全无法执行了，原因是官方不再支持 19.04，很久了…… 好郁闷，于是搜了很多文章，死活升级到了 19.10，本来故事到这里圆满了都，结果我作死的性格作祟，又想，上次没升级 LTS，够打脸，既然 20.04 LTS 出来了，那我干脆一鼓作气上去吧，又来了一次 do-release-upgrade 命令。哈哈！你猜怎么的？ MBP 变砖了。装到一半报错，无法继续下去，重启无法引导了……

我悔恨……

因为此时的我，已经找不到当初怎么制作安装盘装 19.04 的过程了，最后想，我特么为啥非要装作死的 Linux 呢？装个 Mac OS 当 Unix 用呗，也可以探索下。又开始作死了。

然后我惊讶地发现，（一点不惊讶），新版操作系统是不能安装在老电脑硬件上的，所以我显然是不能安装 Mojave 或者下一个更新版本的，经查我最多能装 EL Captain，问题是去哪里下载呢？

又是一通搜索。

找到了下载地址和制作安装优盘的方法。

For macOS Catalina:

```shell
sudo /Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia --volume /Volumes/FlashInstaller

```

For macOS Mojave:

```shell
sudo /Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia --volume /Volumes/FlashInstaller
```

For macOS High Sierra:

```shell
sudo /Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/FlashInstaller
```

For OS X El Capitan

```shell
sudo /Applications/Install\ OS\ X\ El\ Capitan.app/Contents/Resources/createinstallmedia --volume /Volumes/FlashInstaller --applicationpath /Applications/Install\ OS\ X\ El\ Capitan.app
```

For OS X Yosemite:

```shell
sudo /Applications/Install\ OS\ X\ Yosemite.app/Contents/Resources/createinstallmedia --volume /Volumes/FlashInstaller --applicationpath /Applications/Install\ OS\ X\ Yosemite.app --nointeraction
```

For OS X Mavericks:

```shell
sudo /Applications/Install\ OS\ X\ Mavericks.app/Contents/Resources/createinstallmedia --volume /Volumes/FlashInstaller --applicationpath /Applications/Install\ OS\ X\ Mavericks.app --nointeraction
```

下载完毕好不容易可以制作安装盘了，优盘插进去，发现系统识别不了！！！优盘竟然坏了。我想起来上次作死里面做了个 Linux 引导安装盘的，但是不对啊，为啥 Mac OS 读不出来一个正常的引导盘呢？完全无语，难道这就是我安装 18.04 失败的原因？因为引导盘没做好？

蛋疼，已经没时间去反省和缅怀了，先修复优盘吧。

这就涉及到，怎么修复一块图形化界面无法正确处理的优盘，其实就是坏优盘。

继续开始搜索。

```shell
#先用 diskutil，查看一下这个优盘的设备名字
diskutil list
# 看到是 /dev/disk4
# 用命令尝试格式化
sudo diskutil eraseDisk FAT32 <usb_name> MBRFormat /dev/disk4
# 发现我根本不知道优盘的名字，于是没法用这个命令了
# 换命令，强制格式化
diskutil partitionDisk /dev/disk4 1 MBRFormat "MS-DOS FAT32" <new name> 32GB
# 提示我，32GB 太大，超过了磁盘大小，这下有点懵，这就是32 GB 的啊，改写多少呢？难道是那个该死的 1024 和 1000 的梗？
# 还好机智，想起来 diskutil list 里看到写的是 31.6GB，填上去，试试，谢天谢地，过了，优盘复活了！
```

以为一切就绪，很兴奋想要做安装盘了，发现，我下载的是 pkg 格式，这些个命令都是从 app 进去制作安装盘的。

继续开始搜索，发现解决方案很简单，就是双击 pkg，它会把一个 Install OS EL Captain.app 安装你的 Applications 目录，就可以用上面介绍的方法制作安装盘了。神烦。诡异的逻辑。

终于可以安装了，果然，MBP 安装 MacOS 还是顺利的，需要注意的点就是，可能还是需要把硬盘重新格式化一下，因为 Linux 的硬盘分区格式，MacOS 是访问不了的。在启动后使用磁盘工具进行操作。

安装速度比较慢。安装完后，我的电脑又能用了。不过呢，用了一段时间，又发现实在太难用了，而且，还出现了死机的现象。怎么才能把 MacOS 打造成一台常驻的 Server 呢，比起 Linux 来说，还是太麻烦了。