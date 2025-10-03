---
title: 适配 Flutter 的 PopScope
permalink: 2024/adapt-to-the-new-api-popscope/
categories:
  - - 技术
    - 移动端
tags:
  - flutter
date: 2024-08-11 16:52:51
updated: 2025-10-03 01:40:55
---
此前，我写过一篇文章，抱怨 Flutter 的 WillPopScope 的一些问题《[Flutter 在 iOS 下 WillPopScope 导致右滑返回（Swipe Back）失效](/in-ios-willpopscope-disable-swipe-back/)》，当时，我就提出过，在 iOS 上，Swipe Back 这个手势，要播放个动画的，这个交互动作的观感是，像翻书一样的，好像翻起了一页纸，你会看到纸下面是什么内容的。而 Android 系统，完全不是这个交互动画效果，是直接返回的。而 WillPopScope 就是拦截在 Android 上的返回动作，所以出现了一个问题，就是如果你用 WillPopScope，你发现，在 iOS 上牺牲了 Swipe Back 的交互手势。

<!--more-->

GitHub 上的那个 issue，常年累月一直有人跟帖，但是从未真正解决过。不过，我才知道 Android 14，增加了一个新特性，叫 Predictive Back，我看了一下动画演示，不难看出，这个交互效果已经和苹果的 Swipe Back 的动作的效果趋于一致了。用户从左边缘右滑的时候，会看到即将前往的页面的预览图片。

> ... allows the user to peek behind the current route during a valid back gesture and decide whether to continue back or to cancel the gesture ...

到最新版本，不但从 App 返回桌面会看到预览图，从一屏返回到同一款 App 的上一屏，也会看到预览图，从而让用户有了完全一致的返回体验。在一个 App 里，你可以一直从左侧右滑，一直到退出到桌面上。

Flutter 里，被我诟病的那个 WillPopScope，是框架完全收到了用户的后退指令，就是右滑动作已经结束了，才响应，这时候，只有两个选择，一个是执行，一个是拦截。等于这个时候，用户已经交出了控制权了。但是，Predictive Back 的定义是，用户可以自己决定松开手执行动作，还是返回去放弃动作。于是，WillPopScope 的问题等于成为 Flutter 不兼容 Android 的问题了。于是，终于得到了解决。

解决方案，也是非常简单的，就是在用户发起动作之前，就应该判定好，当前界面是否允许返回。如果允许返回，那么将选择权交由用户决定。用户可以用手势动作控制是否返回。如果不能返回，则不允许用户发起该手势。可以去细看我此前解决 WillPopScope 导致 Swipe Back 失效的问题的方案，其实思路完全一样。就是去维护一个 canBack 的标志位，如果可以返回就去掉 WillPopScope，现在等于这个行为变成官方支持的了，自然比我那三脚猫的解决方案优秀多了。完美。

知道了这些原理，怎么去修改代码来适配新的 API，就变得比较简单了。

```dartlang
WillPopScope(
  onWillPop: () async {
    return _myCondition;
  },
  child: ...
),
```

在 WillPopScope 中，`onWillPop` 的语义是，当时这个用户执行了返回动作，比如滑动屏幕边缘，或者按下安卓的返回键，这时候，通知了框架，在 `onWillPop` 中，可以决定是否响应用户的动作。如果 `return false` 则用户的动作指令没有效果。

在 PopScope 中，

```dartlang
PopScope(
  canPop: _myCondition,
  child: ...
),
```

`canPop` 属性已经决定了用户能不能发起返回的动作，如果是 `false` 则界面根本不响应用户的返回操作。其实，就没有一个 `onWillPop` 这样的时点，来执行对应的判断，所以整体的判定更加提前，所以叫 ahead of time API。但是，在用户完全做完这个 pop 的动作后，还是会有一个回调给到框架，告知到底 pop 成功了没有，方便程序做进一步的动作。可见整个语义都完全改了。这个 API 叫 `onPopInvokedWithResult`，最新版 v3.24 就是这个 API 了。

所以，整体看，就有点点 tricky，就是 PopScope 明明 ahead of time 了，但是其回调反而更晚。理解到这里，基本也就够了。
