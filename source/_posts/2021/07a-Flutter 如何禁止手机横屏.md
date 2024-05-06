---
title: Flutter 如何禁止手机横屏
tags:
  - flutter
  - tricks
id: '1072'
categories:
  - - 客户端开发技术
permalink: flutter-disable-landscape-mode/
date: 2021-07-08 16:40:58
updated: 2024-05-06 14:15:22
---
在一些特定的 App 里，我们不希望手机横屏的时候，App 发生旋转，比如微信，企业微信都是这样的。

代码可以这样设定：

```generic
import 'package:flutter/services.dart';

void main() async => {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations(
    [
      DeviceOrientation.portraitUp,   // 竖屏 Portrait 模式
      DeviceOrientation.portraitDown,
      // DeviceOrientation.landscapeLeft, // 横屏 Landscape 模式
      // DeviceOrientation.landscapeRight,
    ],
  );
  runApp(MainApp());
};
```

在 `main` 函数里，像上面那样设定，就可以做到全局禁用横屏模式了。

不过，在企业微信里，我发现，并不是彻底禁用了横屏模式，如果我在企业微信内部打开了一个网页，这种场景下，就是可以横屏过来用的。也就是，WebView 的场景下，我是可以横屏的，但是在其他界面下不可以横屏。这要怎么设置呢？

```generic
  @override
  void initState() {
    super.initState();
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);
  }

  @override
  void dispose() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);
    super.dispose();
  }
```

像这样，设置到一个 StatefulWidget 的 `initState` 和 `dispose` 里面就可以了。比如在我的代码里，我把 WebView 专门封装了一个页面，叫 WebPage，这样设定后，当用户进入网页的时候，可以横屏，但是退回后，就会强制恢复竖屏。

参考：http://kmanong.top/kmn/qxw/form/article?id=2735&cate=93

参考：https://stackoverflow.com/questions/49418332/flutter-how-to-prevent-device-orientation-changes-and-force-portrait
