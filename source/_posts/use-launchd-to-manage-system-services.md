---
title: 【Mac】使用 launchd 管理系统后台服务
tags:
  - launchd
  - mac
id: '574'
categories:
  - - Mac
  - - 小窍门
date: 2020-12-17 00:09:54
---

在 Mac 上安装了 Adobe Photoshop 2021 后，我发现一个代表 Adobe Creative Cloud 服务的图标，出现在 Mac 系统右上角的菜单栏（Menu Bar）上。如果点击这个图标，就会弹出一个窗口，展示 Adobe 的登录表单。这个图标很容易误点，在图标上点击右键，菜单里也没有“退出”选项。打开“系统偏好设置”，“用户与群组”，在“登录项”选项卡上，也没有看到 Adobe 注册什么登录项。到底怎么才能退出这个恼人的程序呢？唯有了解了 launchd 这个系统服务管理机制，才能做到。

![Image result for adobe creative cloud icon](https://cdn4.iconfinder.com/data/icons/proglyphs-free/512/Creative_Cloud-512.png)

Adobe Creative Cloud 的图标
<!-- more -->
## 基本概念

`launchd` 是 MacOS 上用于管理系统级或者用户级后台服务进程的管理工具。也是官方推荐的系统后台进程管理工具，就好像在 Linux 系统里，我们使用 `systemd` 去管理后台服务进程一样。

`launchd` 是一个程序，以系统常驻进程的形态运转，是 MacOS 系统启动后的第一个进程，在 Terminal 终端，键入命令 `ps aux` 可以看到，`launchd` 的进程ID（PID）是 `1`。也即这是系统的**第一个进程**。

与 `launchd` 交互的工具，叫 `launchctl`。可以认为是它的管理客户端程序。通过该命令，我们可以发送指令给 `launchd` 完成对系统服务或后台进程的管理。

`launchd` 的管理对象都是后台进程，这些后台进程使用一种特定格式的配置文件叫 `launchd.plist` 来描述被管理的对象。这种文件是 `XML` 格式的，根据不同的运行权限，放在不同的目录里面，请看下面的表格。

目录

说明

`~/Library/LaunchAgents`

用户自己提供的用户级 Agent。

`/Library/LaunchAgents`

管理员提供的用户级 Agent。

`/Library/LaunchDaemons`

管理员提供的系统级 Daemon。

`/System/Library/LaunchAgents`

苹果官方提供的用户级 Agent。

`/System/Library/LaunchDaemons`

苹果官方提供的系统级 Daemon。

存放 launchd 配置文件的常用目录

通过 `launchd` 管理的进程，人为被分为了几个种类：

*   服务（Services）—— 在后台运行，用以支持图形界面应用（GUI App）运行的服务进程，比如响应系统全局快捷键，或者进行网络通信等；
*   守护进程（Daemons）—— 理论上，不属于服务的后台进程，都归为守护进程一类，不过这里特指运行在后台，且不能与用户交互图形界面产生联系的进程；
*   代理（Agents）—— 以用户的名义，在后台运行的进程，可以和用户图形界面产生联系，比如呼起一个软件的界面，不过官方不推荐这么用。

## 基本操作

通过对基本概念的理解，我们已经知道了这个系统工具的原理。从这个原理层面来理解，Adobe 公司这样设计自己的软件是不道德的。它使用权限很高的系统后台服务进程，只是为了拉起一个常驻在系统菜单栏的小图标，而这个小图标也不提供几乎任何有效的功能，只是一个登录入口，有点大炮打蚊子的感觉。关键是，这个小图标很容易误点，一旦点到就会弹出一个巨大的登录表单，骚扰了用户，对于不懂技术的用户来说，还无法简单退出。

```shell
# 罗列系统当前运行的进程清单
launchctl list

# 查看特定服务的配置信息
launchctl list com.adobe.AdobeCreativeCloud

# 加载特定的服务配置
launchctl load <file_path>

# 卸载特定的服务配置
launchctl unload -w /Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist
# 特此说明，-w 参数的作用是，如果自动执行了 load 命令尝试去恢复服务注册，则让其无效
```

使用命令`launchctl list` 可以罗列出，系统当前在运行的服务清单，赫然可以看到 `com.adobe.AdobeCreativeCloud` 在列，正在运行，进程 ID 513。这个 `com.adobe.AdobeCreativeCloud` 在 `launchd` 系列里的概念叫 Label。

使用命令 `launchctl list com.adobe.AdobeCreativeCloud` 可以查看这个服务的一些配置信息，可以里面有这个服务启动的程序所在的目录，启动参数等。

如果我想把一个服务注册到系统服务里，使用命令 `launchctl load` 就可以做到，当然，还需要编写一个配置文件，在 Mac 系统里，是一种叫 plist 的格式（满足 XML 规范）。

如果我想要把一个服务注销掉，使用命令 `launchctl unload <plist_path>` 就可以做到。在上面，我们通过 `launchctl list` 命令找到了 `com.adobe.AdobeCreativeCloud` 这个 Label，怎么才能找到其配置文件呢？使用 `locate com.adobe.AdobeCreativeCloud` 命令，这是 `*nix` 系列系统的常见命令，相当于搜索。当然，首次使用的时候，还有一些麻烦，就是要建立索引，不过，Mac 系统的 Terminal 执行此命令，一般会提示如何建立索引的。照着执行便可。个人觉得比 Spotlight 要好用一点。

```shell
launchctl unload -w /Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist
```

找到那个 `com.adobe.AdobeCreativeCloud` 所在的 plist 配置文件的路径后，我们就可以用 `launchctl unload <plist_path>` 来卸载这个服务了。以后也不会开机自动启动了。注意，上面的例子里用了 `-w` 参数，如果不用此参数的话，你会发现一旦系统重启，那个恼人的小图标就又会出现。因为另有别的服务进程，或者应用程序，重新注册了这个系统服务。而使用 `-w` 参数，就是为了杜绝此种情况，使 `unload` 命令被持久化，让我们意图注销的“流氓”服务无法被重新加载。