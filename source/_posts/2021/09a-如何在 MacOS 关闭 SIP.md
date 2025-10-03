---
title: 如何在 MacOS 关闭 SIP
tags:
  - mac
id: '1079'
categories:
  - - 技术
    - 工具
permalink: howto-disable-sip-on-macos/
date: 2021-09-04 16:16:47
updated: 2024-05-06 14:18:09
---
SIP 是 MacOS 的一项新特性，System Integrity Protection，系统完整性保护，主要用于阻止系统运行未授权的代码。除了通过 App Store 正规途径分发软件给用户，开发者还可以通过公正，直接分发软件给用户。除此以外的软件分发，都是不被授权的。

执行命令：

```generic
csrutil status
```

可以判断系统的 SIP 特性当前状态是否开启。

关机后重启进入恢复模式，才可以在命令行关闭 SIP 特性。

```generic
csrutil disable
```

可以关闭 SIP 特性，但是关闭 SIP，会导致系统处于某种危险状态中，这时候运行不安全的软件，就不会被系统阻止，要谨防系统遭到入侵。

重启进入恢复模式的方法是，启动时候，按住 `⌘+R` 组合键。如果想要恢复 SIP 的话，还是需要进入恢复模式。执行 `csrutil enable` 就可以恢复 SIP 了。
