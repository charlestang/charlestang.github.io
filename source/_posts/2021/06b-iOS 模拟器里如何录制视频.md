---
title: iOS 模拟器里如何录制视频
tags:
  - usage
id: '1066'
categories:
  - [小窍门]
  - [工作相关]
date: 2021-06-09 17:26:04
permalink: ios-howto-screenshot-in-simulator/
---

在命令行执行：

```shell
xcrun simctl io booted recordVideo filename.mov
```

录制完毕后，使用`⌃ + C` 终止录制。

还有一种方法，使用 QuickTime 的录屏功能，可以录制指定的屏幕区域。