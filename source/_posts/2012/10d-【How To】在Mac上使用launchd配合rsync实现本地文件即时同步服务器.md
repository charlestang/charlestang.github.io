---
title: 【How To】在Mac上使用launchd配合rsync实现本地文件即时同步服务器
tags:
  - launchd
  - Linux
  - mac
  - rsync
  - usage
id: '512'
categories:
  - [工作相关, Linux]
  - [Mac]
date: 2012-10-07 17:20:54
permalink: use-launchd-and-rsync-source-sync/
---

Web开发人员，经常要做的一个事情，就是将源代码上传到服务器。但是这是一个极其痛苦的过程，因为这个过程机械，重复，无技术含量，关键是因为Web应用往往没有调试环境，一般的调试方法，都是改了代码，然后马上刷新浏览器来看结果，所以上传代码变成了一个太过频繁的事情，以至于频繁到了让人厌倦的地步。
<!-- more -->
可以说很多的开发人员都面临着这样的问题，几乎是所有的使用终端-服务器模型工作的开发。他们因为各种原因要在本地终端工作，又因为各种原因要将本地文件同步到远端服务器。最痛苦的莫过于是Web开发，因为他们经常每改一行代码都要传一次。于是想出了各种办法来解决问题。

FTP-现在各种主流IDE都支持使用FTP协议，从远端目录创建项目，然后在保存的时候，将变更文件传送到远端服务器。比如NetBeans，PHPStorm，Eclipse系列，UltraEdit等等。缺点：非加密传输（甚至是明文），每传一个文件，发起一次连接，握手三次，一般还要使用Passive Mode，又增加三次握手，所以，速度相当慢，上传文件覆盖，如果上传了一半网络中断……

SFTP-使用ssh通道的FTP协议，用法跟FTP一样，优点是安全，加密传输，缺点是FTP的各种缺点，加速度慢，因为安全，因为加密，还有个缺点是配置麻烦，可能要配置公私钥对，你总不希望每次都要输入密码吧，界面上也不支持啊……

版本控制工具-SVN，Git，等等，在本地编辑完文件，commit/push到服务器，还自带了版本控制。缺点，必须手动执行，也可以从IDE里手动执行，比如快捷键，此外，据我所知，SVN也好，还是Git也好，都不能让上传的文件，立刻发生作用，SVN需要export或者update，Git也需要merge，否则文件只是入“库”了，并没有直接进入到文件系统……

NFS-这个确实是很牛逼的解决方案，把远端服务器的硬盘映射到本地，等于直接在服务器编辑了。缺点，速度慢，中国这网络条件，除非是内网，否则卡死。另外这个东西也需要安装，配置，不像其他三种，天然就会。

以上描述的，除了NFS，我都用过了，只能说是能用，但是不理想。不够方便，不是终极解决方案。随着工作年限的加长，能力的增长，负担的项目公司的也好，自己玩的也好，都越来越多的情况下，这个文件同步问题上升为非常尖锐的矛盾了。不得不努力学习了。

然后我想到了rsync，那个我一直不愿意学习的东西。因为每次执行man rsync，我都有点抓狂的感觉，狂多的英文，狂多的选项，都不知所云，好吧，我是懒人一个。事实证明，rsync确实可以解决问题。而且我很邪恶地觉得，很多人学习rsync都是被逼的，XD。

rsync我学得不多（因为懒），现在刚到够用的地步，主要有几个特性：

*   增量 - 强大的原因，对比文件差异，然后只传输差异部分
*   压缩 - 强大的原因，怎么实现秒传？传得越少，速度越快
*   黑名单 - 某些目录和文件是永远不用传的
*   安全 - 有权限校验，可以走ssh通道，根据主机、或者用户名
*   连续 - 不是一次只传一个文件

总结一下就是四个字：多，快，好，省。缺点是很难提起学习它的兴趣。就是一个*NIX命令而已，整那么复杂。如果使用ssh作为传输的通道，那么rsync可以快速上手。

```shell
rsync --rsh=ssh -avz SRC user@host:/path/to/DST
```

使用这个命令，就可以把SRC目录，拷贝到服务器上的/path/to/DST/目录下了。而且是每次把差异部分给拷贝过去，非常快。关于为什么快有个文章[《rsync核心算法》](http://coolshell.cn/articles/7425.html "rsync核心算法")可以看看。

到了这里，快速安全传输的问题都解决了。当然，还是要配置ssh公私钥对的。又来了一个问题，这个也需要手动激发。就不能自动么？第一次我想的是用crontab，基本解决问题了，crontab的时间粒度是1分钟，基本够用了，但是还不是那么爽。

然后我想到了iNotify，这个是Linux Kernel用来监测文件系统变化的工具，前面研究过一点点，我的系统是Mac OS X，我想这个东西既然是BSD，跟Linux属于同一个祖宗的东西，当然Mac更正宗一点，那么一定是有个类似的东西或者方案，可以用的，于是搜索“Mac OS X inotify”，找到了StackOverflow上面的[一个帖子](http://stackoverflow.com/questions/1515730/is-there-a-command-like-watch-or-inotifywait-on-the-mac "Mac上如何监控目录变化")。哈哈哈，问题解决了。

```xml
<!--?xml version="1.0" encoding="UTF-8"?-->
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>logger</string>
    <key>ProgramArguments</key>
    <array>
      <string>/usr/bin/rsync</string>
      <string>-avz</string>
      <string>--rsh=ssh SRC user@host:/path/to/DST</string>
    </array>
    <key>WatchPaths</key>
    <string>/path/to/SRC/</string>
  <dict>
</plist>
```

放到~/Library/LaunchAgents/rsync.plist文件中，然后执行：

```shell
launchctl load ~/Library/LaunchAgents/rsync.plist
```

然后，就实现了每当目录下有文件变化，就自动同步到服务器了。希望诸君能得到启发，找到自己的NB方案。