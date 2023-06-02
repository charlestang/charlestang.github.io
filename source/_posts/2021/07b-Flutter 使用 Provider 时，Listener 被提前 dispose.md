---
title: Flutter 使用 Provider 时，Listener 被提前 dispose
tags:
  - experience
  - flutter
id: '1075'
categories:
  - [工作相关, Flutter]
  - [工作相关, 心得体会]
date: 2021-07-23 22:52:40
permalink: flutter-provider-listener-dispose/
---

学会了使用 Provider 后，真是感觉无比畅快，恨不得每个页面都替换成使用 Provider 来开发。不过今天遇到了一个问题：

```generic
Unhandled Exception: A SettingsProvider was used after being disposed.
```

场景是这样的，我有一个 SettingsProvider 保存着“设置”页面的状态，这个页面也就是一般的 App 用于放置“退出登录”按钮的，也正式这个功能引发了问题。

业务逻辑是这样的，当用户点击退出登录按钮的时候，为了防止连续重复请求，我会先把按钮设置成禁用，并展示 Indicator，然后，发起网络请求，去服务器注销 Push Alias，以及注销当前客户端的登录态。

注销成功，或者注销失败，我会解除按钮的禁用，而注销成功后，我会把页面跳转到 Login。这里有些很复杂的情况需要交代：

1.  注销 Push Alias 是在极光；
2.  注销成功后，才能在自己的 Server 注销 registration_id；
3.  完成操作 2，才可以去服务器注销本地登录态；
4.  完成操作 2，才可以销毁本地保存的登录态，不然无法执行 2（需要登录态）；
5.  操作 1 可能会阻塞整个流程导致最终无法退出登录；
6.  完成操作 4 后，需要跳转到 Login。

其实上面一些事情的操作顺序也好，约束条件也好，都还可以进一步推敲，我要说的是，当我执行到 6 的时候，爆了一个 Uncaught Exception，就是上面说的那个 A SettingsProvider was used after being disposed.

经过我在网上搜索和反复比对后我发现，这个错误的成因是这样的。我在网络请求成功或者失败的回调里，尝试解放退出按钮的状态，但是这个时候，异步的执行已经把整个页面给 Pop 掉了，导致了 Provider 的 Listener 提前被 dispose 了，这时候，再去 notifyListeners() 就会导致上面的问题。这个问题提示很难被理解，也很难解决。

网上一种说法，你需要把 Provider 放到更加高一层级的节点上去，这肯定不是一个正确的解，因为这个错误的发生不是 Provider 被销毁，而是因为页面跳走，Provider 的 Listener 被 dispose 导致的。

我用的解决办法是，在调用的时候，用 Provider 的属性 hasListeners 来提前判断一下，是否还有需要通知的对象，然后再调用 notifyListeners()，就不会引发这个错误了。

```generic
  set isWaiting(bool val) {
    _isWaiting = val;
    if (hasListeners) {
      notifyListeners();
    }
  }

  set buttonValid(bool val) {
    _buttonValid = val;
    if (hasListeners) {
      notifyListeners();
    }
  }
```

代码示例如上。上面这个问题的解决，给我的启示是，当进行异步编程的时候，各种任务同步或异步的发起并执行，各种任务结束的时刻不同，这时候决不能对任务完结的顺序有任何侥幸，否则会给程序代理很多不可预测的问题。

-- UPDATE--

最近又遇到个问题，我也续在这里吧，跟这个问题对称的，也是调用方法的时候，报对象已经被 dispose 了，说对称，因为这回是 Provider 被 dispose 了。场景是这样的，在 Provider 里面，触发网络请求，网络请求是异步的，在网络请求回来后，处理完数据，调用 notifyListeners() 是比较常见的一种方法，但是因为这是一个异步的方法，所以，这时候，因为某些原因，Provider 自己已经被 dispose 了，同样会引起 Uncaught Exception。

这个情况怎么处理呢？我这里也写一个，不过未必是最好的，可能也是 SO 看到的。

```generic
_disposed = false;

@override
dispose() {
  _disposed = true;
  super.dispose();
}

void updateData() async {
  await DioUtils.instance.requestNetwork(
    url,
    onSuccess: (data) {
      // do something
      if (!_disposed) {
        notifyListeners();
      }
    },
    onError: (code, msg) {}
  );
}

...
```

这个方法使用一个类变量来记录 Provider 是否已经被 dispose，并在 dispose 的时候，改变值，这样就可以随时知道当前的 Provider 是否已经被 dispose 了。虽然不是很雅观，但是很直接地解决了问题。

-- END --