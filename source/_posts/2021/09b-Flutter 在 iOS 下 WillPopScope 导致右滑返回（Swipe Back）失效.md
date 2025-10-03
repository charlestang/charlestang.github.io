---
title: Flutter 在 iOS 下 WillPopScope 导致右滑返回（Swipe Back）失效
tags:
  - flutter
  - iOS
id: '1080'
categories:
  - - 技术
    - 移动端
permalink: in-ios-willpopscope-disable-swipe-back/
date: 2021-09-06 12:00:33
updated: 2024-08-11 16:52:20
---
本原文发布于 2021-09-06

在有些场景下，App 为了防止用户误触返回按钮或者误触返回键，导致未保存的结果返回，都会想办法拦截用户的返回行为。WillPopScope 就是做这个用的。这个组件会提供一个回调 onWillPop，当用户尝试返回的时候，会被调用，如果返回 false，则会阻止用户的返回行为。

```dart
  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      child: Scaffold(
        bottomNavigationBar: BottomNavigationBar(
          items: _items,
          currentIndex: _currentIndex,
          onTap: onTap,
        ),
        body: IndexedStack(
          children: _pageList,
          index: _currentIndex,
        ),
      ),
      onWillPop: () {
        var now = DateTime.now().millisecondsSinceEpoch;
        if (now - _lastClickExitTime > _exitDuration) {
          Fluttertoast.showToast(msg: "再按一次退出应用");
          _lastClickExitTime = now;
        } else {
          SystemNavigator.pop(animated: true);
        }
        return Future.value(false);
      },
    );
  }
```

我一开始没有太注意这个类，和一个安卓的同事搭档的时候，看到他引入了这个组件，才想明白了，很多安卓手机上，有实体或者模拟的返回键，很容易误触，所以确实很需要这个回调。上面是一个使用 `onWillPop` 防止误触返回的例子。

不过，随着研发的深入，我发现一个很严重的问题。在 iOS 上我有一个习惯动作，就是从屏幕的左边沿，向右滑动，就可以返回上一个屏幕，在 iOS 上，这个动作有个专有名词，叫 Swipe Back，右滑返回。如果我用一个 `WillPopScope` 套住 `Scaffold` 的话，iOS 上这个页面，Swipe Back 就会完全失效。手指滑动上去，完全没有反应。而且令人发指的是，`onWillPop` 也完全不会被触发。等于说，在 iOS 上，这个类的作用仅有一个，就是 Swipe Back 手势被取消，回调也永远不会触发。

这真是太不美了，经过搜索，我发现这个是官方一个很著名的 [issue #14203](https://github.com/flutter/flutter/issues/14203)，2018 年 1 月打开，无数人反馈，至今没有一个明确的回应。有人（可能是官方）表示，这本来就是一个期望中的行为，只是文档没有说明。

也有观点认为，“只是拦截这个动作，而且 `onWillPop` 也可以返回 `true`，还是允许返回的，为什么在 iOS 就彻底失灵了呢？” —— 我也是这么想的。不过，我细细一想，也有点能理解实现者的做法，在 iOS 上，这个动作会有个配套的动画，右滑的时候，会好像翻书一样的视觉效果。如果这时候 App 不允许用户返回的话，滑到一半，这个动画的物理表现到底是怎么样的呢？像皮筋一样弹回？还是怎么做呢？确实有点恼火。还不如完全就没响应。

不过，这就太苦了我们这种想要在 iOS 上保证交互效果的开发。有某个老哥做了一个 `CupertinoWillPopScope` 插件，试图要去解决这个问题，不过我看了一眼，很不喜欢他的实现。他的实现其实基于一个事实，就是 `WillPopScope` 里，如果 `onWillPop` 为 `null` 的话，在 iOS 上，就不会阻止 Swipe Back，这个我自己写个变量也可以控制，何至于引入一个插件，一个变量就能解决的事情。

我自己遇到的一个场景，也确实很恼火，在 App 里，我引用了 flutter_inappwebview 这个插件，主要是提供了一个查看网页的 WebView，在 WebView 里，我想实现的效果是，Swipe Back 的时候，如果网页有 history，只是返回上一页，如果没有 history，就退出 WebView。这就需要我每次都能拦截 Swipe Back 这个动作，然后判定后决定到底是在网页里后退，还是干脆退出 WebView。

不过，因为刚才说的 `WillPopScope` 的问题，导致了很奇怪的局面。当我用了以后。在 iOS 上，效果诡异，我永远失去了 Swipe Back 退出 WebView 的能力，但是，在网页上后退却不受影响。只是退到第一页的时候，就再也滑不动了，不能滑动退出 WebView。如果我去掉 `WillPopScope`，则不论你在哪个页面，都会导致滑动直接退出 WebView，无法实现返回上一页的功能。

只剩下一个办法，就是通过判断 `canGoBack`，来决定是否绑定 `onWillPop`，就可以完全实现我的想法，不过 `canGoBack` 又是一个 `Future` 类型，我又不知道怎么写了。唉。问题仍然还是没有解决的，我特别记录在此，给遇到同样问题的同学一些参考，同时也希望高手看到了不吝赐教。

```dart
  @override
  Widget build(BuildContext context) {
    mUrl = ModalRoute.of(context)?.settings.arguments.toString() ?? "";
    final double pixel = MediaQuery.of(context).size.width / 375;
    return WillPopScope(
      child: Scaffold(
        appBar: MyAppBar.create(
          title: _pageTitle ?? "",
          pixel: pixel,
          actions: [
            IconButton(
              onPressed: () {
                NavigatorUtils.goBack(context);
              },
              icon: Icon(Icons.close),
            ),
          ],
        ),
        body: _webPageContent(),
      ),
      onWillPop: !_canGoBack
          ? null
          : () /** 此逻辑在 iOS 下无效 */ {
              var canGoBack = webViewController?.canGoBack() ?? Future.value(false);
              canGoBack.then((value) {
                if (value) {
                  webViewController?.goBack();
                } else {
                  Navigator.pop(context);
                }
              });
              return Future.value(false);
            },
    );
  }
```

上述代码里，`_canGoBack` 这个变量，是我自己模拟的，但是这个变量的效果和 `flutter_inappwebview` 提供的就不太一样了，插件提供的 API，返回一个 `Future<bool>` 类型，在任何时候都可以判定当前网页是否存在 history 栈，但是我自己实现的 `_canGoBack` 变量，只是判定该网页已经不是首次加载的那个，经历过跳转。在我的场景里，大多数网页，只是看一眼就返回了，用户不会循着链接一层层深入，所以在很大程度上可以达到我要的效果，但是，显然没有真正解决这个问题，如果用户浏览了两个页面，就会退回我上文说的效果了。只是略微好了一点点。

-- End --

-- Update --

现在已经是 2022 年 11 月 17 日了，这个问题官方仍然没有好的解决方法，只是我在上述方案后面，又有了新的一些探索和问题。特此记录一下。

就我现在的理解来看，上述方案的实现背后，有一些关键性的事实：

第一，App 层面，默认是可以响应 Swipe Back 这个行为的，但是，套上 WillPopScope，提供 onWillPop 回调后，Swipe Back 失效（这是上文已经分析过的内容）；

第二，flutter_inappwebview 这个插件提供的 WebView 组件，内部本身可以响应 Swipe Back 这个动作，因为在 iOS 上，这个插件是用 WKWebView 实现的，所以其行为来自 iOS 系统本身的默认行为，这就是为什么开启 onWillPop 后，虽然不能 Swipe Back 退出 WebView，但是如果你在 WebView 内部多次跳转链接，可以用 Swipe Back 后退；本质上，就是有两层，外层是 App 层面的交互行为，内层是 WebView 内部的交互行为，这两者是分离的（从原文的描述中，可以体会到这一点，这里明确总结出来）；

第三，现在遇到的困扰，就是 Swipe Back 这个动作，在穿越 WebView 和 Flutter App 中间的界限的时候，出现了衔接的问题。这个地方本来就需要衔接，因为 App 和 WebView 都可以响应 Swipe Back 动作，那么应该谁来处理这个事件，程序员就需要自己决定。本来，如果 onWillPop 回调，在 iOS 上没有 bug 的话，一切都很美，可惜事与愿违；

第四，上述解决方案，就是在通过编程，来确立 App 和 WebView 谁来接管 Swipe Back 动作的边界，也即设立了一个 \_canGoBack 的变量，作为 flag。核心原理是，内部 history 可以执行 goBack 的时候，就由内部接管，不能执行的时候，就由外部接管。程序员要做的，就是在恰当的时候，正确设定 flag 的值。

原文方案里，我只是在 WebView:onLoadStop 事件中，设定 \_canGoBack 的值为 true/false，也即，如果内部 WebView 加载了超过一个页面，那么就由内部接管事件，这个时候开启 onWillPop 捕获，会自动屏蔽 iOS 下 App 级别的事件处理。

现在我们的业务场景遇到一个新的问题，就是 WebView 加载的内嵌页面，可能是一个 SPA，单页应用，这种类型的应用，在页面内部的路由切换，浏览器不需要重新加载，这个时候，就不会触发 onLoadStart/onLoadStop 事件，导致我们设定 flag 的意图无法实现，此种情景下，就会让 back 按钮一点就会退出整个 WebView。

其实，这个问题，也是一个“传统”的难题。比如，大家有没有这种经历，就是去你去街边小店，点餐的时候，从公众号里，点开一个界面，点到一半，想看一下上一步的内容，点了一下后退，结果整个界面被关掉了，十分恼火。微信发展这么多年，腾讯那么强大，竟然在这个小问题上还是没有完美解决，当然，也可能是点餐界面的开发者太垃圾，不管怎么说，都说明这个问题真的很难，很普遍。

那么在我们这里，这种情况是否有解决方案呢？办法总比困难多，目前，我们想到了一个部分解决问题的方法。就是利用 js 回调通信解决。我认真研究了一下单页应用的原理，在 SPA 内部，路由也是一个老生常谈的问题，就是在页面没有加载的情况下，如何根据用户的操作来切换场景。这也是一个经典的面试题。

SPA 的路由实现，其目标是浏览器不重新加载，全部交由页面的 js 来操控界面的绘制和场景的切换。如果通过地址栏 location 改变路径，可能会造成浏览器重新加载。那么常用的方案有两种，第一，使用 http 协议中的 fragment，也有叫 hash 的，就是一个带有 # 号的网址，浏览器在处理的时候，会自动把 # 后面的部分，理解为页面内部的锚点，不会发起 HTTP 请求，第二，使用 history API，这是现代浏览器都支持的一个内部对象，专门管理浏览器的状态，可以通过 pushState，replaceState，go，back，forward 等 API 进行操作。

使用 hash 进行路由的时候，可以直接更改 location，浏览器不会发送请求，但是，会进行处理。使用 pushState 的时候，浏览器完全不会进行处理，所以，哪怕你发个真实的 path 过去，浏览器也不会刷新。这种方式，可以把地址伪装成真实 URL 的样子，看起来很友好。

我发现 spec 里提到，使用 hash 的时候，浏览器会触发一个事件叫 hashchange，这是一个标准的事件，通过注入 js handler，来捕获 hashchange 事件，我们可以知道，内部页面发生了路由，可以进行 goBack，这时候设定 flag，就可以沿用原文中提到的逻辑了。

但是 pushState 本身就不会触发任何事件，每个框架会个自创建事件进行绑定，我们作为 WebView 的实现方，不太好做通用的方案。

-- End Update --
