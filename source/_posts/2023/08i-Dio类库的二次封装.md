---
title: Dio 类库的二次封装
tags:
  - Flutter
  - Dio
categories:
  - - 技术
    - 移动端
permalink: 2023/dio-encapsulate/
date: 2023-08-28 14:07:00
updated: 2024-05-06 14:14:31
---

使用 Flutter 开发 App 都免不了要使用网络访问的类库，Dio 是其中最流行的，我之前调研的一些范例 App 代码，都引用了 Dio。Dio 是对 http 的一套封装，提供了很多友好的功能。

不过，要在项目里使用，一般还要进行一次封装，你如果搜索 Dio 封装，会找到一大堆的文章，专门讲怎么封装 Dio 的。

<!-- more --> 

## 为什么要再次封装？

Dio 自己已经是一个封装好的类库了，为什么在项目里使用，还需要再次封装呢？

先来看看 Dio 官方提供的例子：
```dart
import 'package:dio/dio.dart';

final dio = Dio();

void getHttp() async {
  final response = await dio.get('https://dart.dev');
  print(response);
}
```
上面的代码，创建了一个全局的 Dio 对象，然后，调用 GET 方法，获取了一个网页，然后打印返回对象。

看起来接口已经无比简洁了，毫无封装的必要。其实这个例子大有问题。

首先，Dio 对象是进行网络访问的一个资源，那么进行网络连接的一些基本参数的设定，例子里是完全没有体现的。比如各种超时时间设定，鉴权逻辑，错误处理逻辑，公共请求参数，返回值的解析等等，完全没有在例子里体现出来。

## 封装要解决哪些问题？

根据我们一般的的开发经验，在一个项目里，如果涉及到要跟后端通信，那么有一些基本的东西，我们是可以复用的。

### 基础设置

比如，连接超时时间，发送超时时间，返回超时时间，这些一般都是在每个请求里是通用的。

又比如，连接的后台服务器的域名也是通用的，接口一般遵循某种规范设计，那么发送的包体，返回的包体格式也都是一致的，有固定的包头和载荷格式。一般很多服务器的鉴权机制也是固定的。比如使用 access_token 或者其他 token 等。

这些东西都需要在初始化 Dio 对象的时候指定，所以，我们一定需要找一个特定的地方来放置这些初始化代码。

一般创建一个 Dio 非常占用资源，我们可能也需要使用一个单例模式来长期重复使用一个 Dio 对象。

### 通信协议

创建 Dio 对象，以及初始化设置，毕竟是一个一次性工作。但是，网络请求的协议，则是高度复用的了，每一次的 API 调用，都要用到协议。

协议就是客户端和服务器端约定的通信包体的格式。一般来说，在一个项目里，应该只有一种通信协议。比如用什么格式组织请求参数，用什么格式返回参数。

如果不事先约定好，那么收到请求时候，就不知道如何响应。

### 请求鉴权

对于 UGC 的网站来说，用户创建和维护自己的内容是最重要的。HTTP 协议是无状态的，但是客户端 App 传递给用户的感觉，往往是一直在线的，那么就需要通过 HTTP 协议去建立一个会话。

浏览器的一般做法是通过 Session 来保持，而客户端一般通过一个特殊的 token，每个请求都带上 token，帮助服务器鉴定用户的身份，并恢复用户的会话和状态。

这种类型的机制，一般都是通用的，App 和自己的后台服务器之间，只有一套这样的机制。在具体写业务的时候，不可能每个 API 的调用都各自去重新考虑鉴权的问题，往往需要通用。

### 错误处理

这是另一个非常需要重用的领域。不少应用服务器的错误处理都是统一的，错误码都是统一按照号段编码。

这里面大多数的错误，都是各个业务模块去处理，而里面有不少，却是需要统一处理的。我举个例子，比如密码过期，登录态失效，这样的错误是所有业务调用都有可能碰到的错误码，而其处理方式又是完全一样的。

比如登录态失效，需要跳转到登录页面，而密码过期，需要重置密码，不管你原来在干什么，遇到这两个错误码，只能执行特定的逻辑。

除了这类问题被归集到错误处理以外。还有一个问题。就是我们客户端在网络请求的时候，可能遇到各种错误，比如网络错误，比如连接错误，比如业务逻辑本身错误。而显然这三种错误是完全无关的，在系统里也往往由不同的模块提供，至少他们肯定在不同的网络层次上。但是，无论哪一层的错误，我们都需要给用户统一而且友好的错误提示，要想进行这样的处理，你得首先把三类错误一起拦截，这也需要进行代码复用。

### 单元测试

单元测试，是另一个我们必须封装 Dio 的理由。我们写的 App，要想代码质量保持稳定并进行长期维护，必须持续积累单元测试。

但是我们知道，网络请求这种逻辑，都是由外部系统配合完成的，如果不对网络服务器进行 mock，进行单元测试是不可能的。让服务器配合我们做各种 API 返回值的可能性，那就是痴人说梦，成本上也无法负担。

网络请求模块，必须能够被无缝替换，并进行 mock，这样我们才能通过模拟各种 API 返回值的情况，来测试本地逻辑的正确性。

### 调试功能

如果你想在电脑上利用工具调试 API，那么一个网络代理功能，也是不可或缺的，给 App 上的网络模块配置代理的功能，是所有业务模块在进行网络请求的时候都要考虑的通用功能，这种也属于封装层面要解决的问题。

## 封装的设计

明确了上面的这些目标，我们无论是去网上搜一个 Dio 的封装好的代码，还是自己写一个，都有了明确的判断标准和检验标准。

### 单例模式

对 Dio 的封装，第一个问题是，我们是否需为 Dio 对象使用单例模式？你是不是自然而然就使用了单例模式，而没有问问为什么？我们希望通过单例模式达到什么目的？

是昂贵的系统资源复用？复杂的对象结构的复用，避免反复实例化带来的性能损耗？对象回收再利用带来的性能提升？

用或者不用，都没什么关系，只是我们希望这个决策是尽可能出于理性。

事实上，可能这些原因都有吧。首先，Dio 对象的结构是否复杂呢？我们从代码可以看出来，基本上，Dio 对象主要组成部分就是 Options 和 Interceptors，主要是配置信息和一些拦截器的逻辑代码。数据结构是比较复杂的，对象群也比较多，如果采用单例确实能够节省一点。

第二点，Dio 本质上是对 HttpClient 的封装，在 Http 包的主页上声明：

> If you're making multiple requests to the same server, you can keep open a persistent connection by using a [Client](https://pub.dev/documentation/http/latest/http/Client-class.html) rather than making one-off requests. If you do this, make sure to close the client when you're done

什么意思呢，对同一台 Server 的多次请求，可以使用一个持久化的连接，也即连接可以被复用。那么这必然可以节省一些时间的。如果不采用单例，就很难利用到这个功能了。毕竟 httpClient 被包裹在 Dio 对象的里层。

基于以上一些分析，Dio 对象的实例应该被单例化，这样对系统整体的性能更加有利。

### 通用配置信息

通用配置信息，比如各种超时时间，以及服务器的根网址（如果有的话），还有就是所有请求都要用到的过滤器，拦截器等等，这些东西，基本每次请求都要带上。

如何存储这些信息呢？可以使用全局变量，或者类静态变量，也可以从配置文件读取，还可以作为单例对象（一次性可以改掉整个系统的设置）的属性等等方法。

我选择了作为单例对象的属性这个方法，来设计我自己的封装。其实这个和使用全局变量相比并没有什么特别的优势，只是保存几个值而已。不过呢，我比较喜欢这种格式的 API。

```dart
class ClientOptions {
  static final ClientOptions _instance = ClientOptions._();
  ClientOptions._();
  factory ClientOptions() => _instance;

  Duration connectTimeout = const Duration(seconds: 30);
  Duration receiveTimeout = const Duration(seconds: 30);
  Duration sendTimeout = const Duration(seconds: 30);

  String? baseUrl;
  String? proxy;

  List<Interceptor> interceptors = [
    // 访问制定域名的时候，自动携带登录态
    AuthInterceptor(),
    // 将连接错误，网络错误，业务错误统一起来
    ErrorInterceptor(),
  ];
}
```
上面是我实现的一个单例模式的配置类。

### 应用层协议

你的 App 在访问自己的 Server 的时候，往往都是有最基本的协议的。比如，以前腾讯的 QQ 和服务器通信的协议叫 OIDB，有一套二进制的包头和包体结构。采用了一种类似 TLV 的数据结构。

每个 API 的调用，都需要构建包头，包体，收到回包后，也需要解包，分析包头和包体的内容。

腾讯的的 QQ 是基于 UDP 的二进制数据协议。而我们当今，都是在更上层的 HTTP 层，而应用通信采用的则是 JSON 格式。虽然安全性和性能未必有腾讯那么高，但是更易于理解，也更易于调试。

举例来说，我的 App，请求包体就是一个 JSON 对象。例如：

```json
{
  "param1": "val1",
  "param2": "val2"
}
```
而服务器的回包是有结构的：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "key1": "val1",
    "key2": "val2"
  }
}
```

这不是一种完全标准和规范的 RESTful 风格，而是一种我此前开发过的 Web 应用比较常见的做法。

这种做法采用 JSON 结构来携带服务器返回状态，通过载荷字段 data 来返回数据。不借助 HTTP status code 携带业务信息（这也是非常常见的，返回的 JSON 对象直接就是载荷了，不用解包，HTTP 200 表示成功，其他错误则附着在 HTTP status code 4xx、5xx 值上面）。

对于我的包设计来说，需要进行解包操作，真正的业务数据对象是 data 载荷，所以我会在系统里设计一个 BaseEntity 对象，作为返回包体的抽象，其作用就是解读 code 和 message，然后，将 data 构建为业务 Model。

```dart
class BaseEntity<T> {
  BaseEntity(this.code, this.message, this.data);

  int? code;
  late String message;
  T? data;

  BaseEntity.fromJson(Map<String, dynamic> json) {}
}
```
以上是 BaseEntity 的接口设计。这里采用了 dart 的泛型，代表通用包体包裹了里面的业务对象，通过 fromJson 构造，将 JSON 解包结果的 `Map<String, dynamic>` 转换成 BaseEntity 对象，并且 data 成员就构建成 T 的对象。

至于 T 有关的 JSON 对象如何转换的问题，涉及到 Flutter App 里面如何使用 JSON API 的话题，怎么在强类型语言里，顺利转换 JSON 对象，这是一个专门的话题，就不展开了。

### 接口设计

封装 Dio，就不得不考虑，你封装后的接口设计。我怎么思考这个问题呢？我肯定希望自己的封装使用的时候，能自然一点，优雅一点，我是先假想自己使用的方法，再依据自己潜在的用法来实现。

我希望的用法是这样的：

```dart
var result = await ApiClient().post<BusinessModel>(requestParam);
```
可以看到，是一种简单，直接，明了的用法，当然要依据具体应用的需求和使用场景的复杂度来设计自己想要使用的 API，然后，去实现这个 API，就能完成最终的封装。

从这个使用的场景看，我首先需要一个实例，然后调用 POST 方法，通过泛型告知返回的业务 Model 类型。扩展一下：

```dart
try {
  var result = await ApiClient().post<BusinessModel>(requestParam);
} catch( e ) {
  //do sth. when error.
}
```

增加了错误处理，我希望所有的错误处理，都能抛出异常，这样我可以统一处理。错误的逻辑。

这种东西我很难说什么对错，或者大家是否觉得优雅，都是一些很主观的东西，我以前用过一种风格是这样的。

```dart
await ApiClient().post(requestParam, onSuccess: (data) {}, onError: (error) {})
```
这种是回调式的 API 接口，也是一目了然，只是我个人不喜欢这种风格。如果采用这种风格，其他各种组件和设计也都要考虑到这个接口的特点。这种风格的特点是，业务逻辑和错误处理是交织的，我就写出过，在 onSuccess 里，再次发动 HTTP 请求，则明显里面又要嵌套一层 onSuccess 和 onError，让我自己看着十分别扭。

```dart
class ApiClient {

  // 单例模式
  static final _instance = ApiClient._();
  ApiClient._();
  factory ApiClient() => _instance;

  // Dio 实例的单例，lazy loading
  Dio? _dio;
  Dio get dio {
    _dio ??= _createDio();
    return _dio!;
  }

  Dio _createDio() {}

  // 设置代理服务器，方便调试
  set proxy(String proxy) {}

  

  Future<T> get<T>( String apiPath, {
    Map<String, dynamic>? queryParameters,
  }) {
  return dio.get(apiPath, queryParameters: queryParameters)
            .then<T>(_parseResponse);
  }

  Future<T> post<T>( String apiPath, {
    Map<String, dynamic>? queryParameters,
    data,
  }) {
    return dio.post( apiPath, queryParameters: queryParameters, 
    				 data: data)
               .then<T>(_parseResponse);
  
  }

  /// 通用包解析
  /// 服务器的包都有通用的格式，code, message, data
  /// 其中 data 是载荷
  /// 如果发生业务层面的错误，会由 ErrorInterceptor 进行拦截
  /// 直接抛出错误
  Future<T> _parseResponse<T>(Response response) async {
    var resp = BaseEntity<T>.fromJson(response.data!);
    return resp.data as T;
  }

}
```
整套的封装，只有这么一个类，采用_parseResponse 作为解包的一个操作。只提供了 get 和 post 两个接口，使用 RESTful 的还可以把其他几个指令都封装一下，还有上传下载文件。

现在很简陋，当然值得做的很多很多，不过那些都可以慢慢添加。至少现在完全能够满足我的需求。我发现我在整个 App 里只用了 get 和 post 两种，传文件，请求并发的情况都不存在。

### 单元测试

之前已经进行了一些关于单元测试的探讨，至少我现在还是认为单元测试非常重要。这是一种可以通过天长日久逐渐积累，最终形成有力的自动化质量保障手段的一种方法论。

在这里，我们首先假设 Dio 是经过充分测试的，所以，我们不需要忧心，第二，我们的 ApiClient 也就是对 Dio 的封装，只是一层薄薄的包裹，也不需要担心。

真正需要测试的是，我们调用 ApiClient 的代码段落，这里的难点是，发起的网络请求是一个异步操作，如何进行测试呢？

首先是 Mock 的问题，我此前想复杂了，打算设计一个接口，然后，用 ApiClient 实现接口。这样我在具体使用的地方，可以替换一个 DummyClient 或者 PuppetClient 进去，这样，可以控制返回值或者指定返回值，实现 mock。

后来我发现 dart 有一个很优秀的特性。就是它的 Class 是天然自带接口的。在 dart 里，没有 interface 这个关键字。而是每个 class，默认隐含一个 interface，于是，你想要替换一个类 TargetClass 的时候，你只要用 ReplaceClass  implements TargetClass，将 TargetClass 看做一个接口，直接提供一个新的实现，就可以做到替换了。简直 Perfect！

在所有引入 ApiClient 的地方，我们都通过构造函数传入 ApiClient 的实例，这样在我们测试业务对象时候，就可以直接传输一个 DummyClient 的实例，就可以操控网络部分的返回值了。

而异步怎么测试呢？

我在系统里，选用了 bloc 作为我的状态管理框架。这套框架，我用过以后，非常喜欢，我觉得它提供了一种大一统的逻辑框架。

它把这个客户端看成是一种事件响应处理的模型。整个框架是事件驱动的。这正暗合了客户端的使用特点。你写的所有代码，本质上，都是一个个的 EventHandler。

在 bloc 框架里，处理事件处理之外，就是状态管理。核心是 bloc，里面是一系列的 Handler，接受到 Event 之后，进行处理，处理完毕，就 send 一个 state 到界面上，界面根据 state 情况，进行界面重绘和更新。

bloc 框架也提供了一套测试组件，bloc_test，将每个测试用例，理解为一个 event 和 state 的序列。输入一个或者一组 event，然后收到一个或者一组 state。
我们编写用例的时候，只要控制好输入的 event，测试收到的 state 就可以了。非常顺滑和美妙，这也是我非常喜欢 bloc 的原因。

GetX 的接口看起来也很美妙，只是，不像 bloc 这么一统，一致，以及测试方便。在 GetX 里我可能要学懂很多概念，但是在 bloc 里，只需要学懂一种概念体系，就完事了。

### 鉴权和错误处理

鉴权部分，我是放在 Interceptor 里实现的，主要是通过一个 AuthInterceptor，对特定域名，在 HTTP 的 Header 里注入了 token，这样服务器侧完成对 token 的校验即可，对客户端写逻辑来说是透明的。

而错误处理，我增加了一个 ErrorInterceptor，它起到的主要作用是，将连接错误，网络错误，还有服务器的位置错误，都强制扭曲成标准的包体，然后将各种规格不一的错误码，都统一成同一套错误码。

这样做的好处是，我可以将已知的错误信息，都按照更加用户友好的方式提供给用户展示，还可以照顾到错误信息的多语言问题。不用被服务器的多语言能力所左右。

对于未知的错误，则都在客户端隔离掉，提供统一的错误信息。

## 总结

我之前就是使用一个 demo 项目里看来的网络请求类，作为自己的项目里的封装，那时候我还很不了解 Dart 和 flutter，后来在项目逐件成型上线后，为了项目能更好发展，我在逐步替换和重构若干模块和机制。这时候自己写一个和封装一个 Dio，就更加成了我一个目标。

开始想找一个现成的，后来发现各个项目千差万别的，怎么可能正好有我喜欢的封装方法呢？这里我找了几款，也看了一些技术文章，我发现很多都在鼓吹自己封装功能多齐全，技术多先进。而我看了莫名奇妙的 API 后，觉得他们的实现都不符合我的心意。

关键是一般都文档缺失，测试缺失，只有主体部分的代码，一看就像是作坊式代码。这种代码，如果一旦用了，很难保证作者不会弃坑，那时候就是叫天不灵叫地不应了。免费开源，你还能要什么自行车呢？

现成的类库里往往封装了很多高级特性，不少代码也利用了大量语言特性和语法糖，看起来也极其精妙，这方面我觉得我不如他们写的。但是我同样也不觉得自己就比他们差了。他们强的地方，我其实用不着，也不知道会在什么地方用到，他们弱的地方，却是我很需要的东西。

比如，设计上的考量和思考，文档，配套测试用例和测试方法。都对一个长期项目至关重要，也关乎项目后期和远期维护，甚至换人维护的方便程度。都不可不察。

--完--
