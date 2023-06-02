---
title: Mac 上开启粘滞键的特性
tags:
  - mac
id: '742'
categories:
  - 小窍门
date: 2016-09-20 15:37:36
permalink: mac-press-and-hold/
---

以前，用 Windows 系统的时候，我学会了“粘滞键”这个专有名词，其含义，就是当按下一个键盘按键，并且保持不动的时候，系统应有的表现。

比如，一般来说，我们期望系统的行为是连续打出多个按键的字符。 我初始安装 Mac 系统的时候，按下一个按键，在 Terminal 等原生的 App 上，其行为是符合我们的预期的。但是，因为我是程序员，我使用 NetBeans 作为开发环境，当我连续按下一个键的时候，我发现，在 NetBeans 里面，只能出现一个字符。

经过咨询同事，问到了一个系统设置：

defaults write -g ApplePressAndHoldEnabled -bool false

defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false

这个设置项，需要使用命令行来执行，类似一个隐藏设置，其含义是，是否由 Apple 系统来接管 按下并保持 这个行为，如果由系统来接管这个行为，则在某些应用中，系统会比较智能地处理这个行为，比如，在 NeaBeans，其判定为只打出来一个字母。如果，使用如上的设置项，则关闭此行为，系统不要插手这个行为的响应，由相应的 App 来处理这个行为，则可以出现我所预期的结果。