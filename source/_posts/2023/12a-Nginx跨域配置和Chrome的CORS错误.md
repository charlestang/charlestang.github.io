---
title: Nginx 跨域配置和Chrome 的 CORS 错误
permalink: 2023/nginx-cors-config/
categories:
  - - 工作相关
  - - 工作相关
    - 心得体会
  - - 日　　记
tags:
  - nginx
  - CORS
  - Chrome
date: 2023-12-19 20:35:37
updated: 2024-01-05 00:53:27
---
最近，我完成了一个小项目，使用了当下比较时髦的 Vue 3 + TypeScript + Vite + Element Plus，采用前后端分离架构。为了减少对后端 API 的维护量，我将后端的 API 写在了主站的代码里。这样一来，前台网站的域名和后台网站的域名不同，就出现了跨域的问题。

<!--more-->

## 跨域问题的由来

浏览器有一种安全策略，叫做同源策略。它是一种约定，可以防止网页上的 JS 脚本对其他网站的网页进行读取或者修改。这个策略的主要目的是保护用户的信息安全。

我们都知道，浏览器使用 Cookie 保存了用户的登录态，或者 Session ID 之类的信息。在一定时间段内，这些身份凭据并不会过期。而浏览器向服务器发送请求的时候，根据协议，会带上这些身份凭据。如果没有同源策略的约束，你在访问 A 网页的时候，网页上的脚本，往 B 服务器发送一个请求，同时携带了 B 服务器的身份凭据，这样一来，A 网页的恶意脚本，就以用户的名义，在 B 服务器执行了一些指令，从而损害了用户在 B 的利益。

上面的描述，其实就是跨站请求了，如果没有同源策略，则跨站请求会变得极其普遍。其实，CSRF 也是同样的原理。只是同源策略被堵上，并没有完全堵死。对于现在的 CSRF 来说，我们一般采用 CSRF-token 来防范，那是另一个话题了。

总之，我们需要理解的就是，对于一个合格浏览器来说，从一个特定域载入的 JS 脚本，是不能访问其他域的资源的。跨域的判定是非常严格的，比如 a.com 的脚本访问 b.a.com，虽然是子域，也被判定为跨域。反过来，也同样判定为跨域。

有了这样的策略保护，对于用户来说，当然是一件好事，但是对于开发者来说，比如我现在面临的情况，就很不方便了。我是正常开发业务的，但是也出现了服务器的域名和前台域名不同的情况。为了给这种情况提供方便，就出现了 CORS，跨域资源共享。

## CORS 跨域资源共享

CORS（Cross-Origin Resource Sharing，跨源资源共享）是一种安全机制，它允许一个网页的许多资源（例如字体、JavaScript 等）可以被其他域名所访问。

当你尝试从一个不同的源（域名、协议或端口）访问资源时，浏览器会发送一个 CORS 预检请求，检查服务器是否允许跨源请求。如果服务器不允许，浏览器就会阻止请求，并在控制台中显示一个 CORS 错误。

要解决这个问题，你需要在服务器端设置相应的 CORS 头部，允许你的源访问资源。具体的设置方法取决于你的服务器软件和配置。如果你不能修改服务器设置（例如，你正在访问一个第三方 API），你可能需要使用一个代理来绕过 CORS 限制。

为了实现 CORS，你需要对 Web 服务器进行配置，在返回的 HTTP 请求头里，携带特定的 Header 信息，告知浏览器，允许进行跨域访问。

那么是怎么配置的呢？

```nginx
if ($request_method = 'OPTIONS') {
   add_header 'Access-Control-Allow-Origin' '*';
   add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
   add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
   add_header 'Access-Control-Max-Age' 1728000;
   add_header 'Content-Type' 'text/plain charset=UTF-8';
   add_header 'Content-Length' 0;
   return 204;
}

if ($request_method = 'POST') {
   add_header 'Access-Control-Allow-Origin' '*';
   add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
   add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
}

if ($request_method = 'GET') {
   add_header 'Access-Control-Allow-Origin' '*';
   add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
   add_header 'Access-Control-Allow-Headers' 'DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
}
```

## 登录态校验的问题

一般用户登录服务器后的身份，都是服务器颁发凭据，登录态一般靠浏览器的 Cookie 来保持，如果 Cookie 种在 Server 的域上，那么客户端就无法访问到这个 Cookie，除非两个域名是父域名和子域名，并用 `document.domain` 来设置域，才能互用 Cookie。不过，在我这个场景下，前台网站是完全不同的域名。

如果采用 JWT Token 之类的鉴权方案，则前台站点就会类似客户端软件那样去管理登录态了，不过，前台站点一般关注业务逻辑，也不需要读取 Cookie 的内容，所以，我还是把 Cookie 保留在了后端服务的域上，由于也受到同源策略的约束，所以默认是不传递的，那么怎么让前台发送请求到后端的时候，带上 Cookie 呢？

在上面的配置里，首先 `Access-Control-Allow-Origin` 头，不能设置为 `*`，需要设定为具体的具名，比如 `https://example.com`，这个需要指向前台的协议和域名：

```nginx
add_header 'Access-Control-Allow-Origin' 'http://example.com';
add_header 'Access-Control-Allow-Credentials' 'true';
```

另外，在客户端发送请求的时候，要在 `XMLHttpRequest` 对象中设置 `withCredentials` 的值为 `true`。这些都是规范中有明确规定的，如果不逐一照做，就没法正确运行跨域请求。

## 预检 Preflight

预检请求（Preflight Request）是在 CORS 中的一个重要概念，它是浏览器在发送实际跨域请求之前自动发起的一种机制，用于确保安全性。预检请求的主要作用是确定服务器是否允许跨源请求，并且了解服务器允许的条件。以下是预检请求的一些关键点：

### 何时发生预检请求

预检请求在以下情况下触发：

- 请求方法不是简单方法（GET、HEAD、POST）。
- POST 请求的 `Content-Type` 不是 `application/x-www-form-urlencoded`、`multipart/form-data` 或 `text/plain`。
- 请求中包含了自定义头部（非 CORS 安全的头部）。

### 预检请求的特点

- **使用 OPTIONS 方法**：预检请求使用 HTTP 的 OPTIONS 方法。
- **包含特定的头部信息**：它包括如 `Access-Control-Request-Method`（告诉服务器实际请求将使用哪种 HTTP 方法）和 `Access-Control-Request-Headers`（列出了实际请求将发送的自定义头部）。
- **不包含实际请求数据**：预检请求本身不包含实际请求的数据，只是一种安全检查。

### 服务器响应

服务器对预检请求的响应应包含以下头部：

- **`Access-Control-Allow-Origin`**：指明哪些源可以访问资源。
- **`Access-Control-Allow-Methods`**：指明服务器支持的方法。
- **`Access-Control-Allow-Headers`**：如果请求中包含自定义头部，服务器必须在此确认这些头部是允许的。
- **`Access-Control-Max-Age`**：指定预检请求的结果可以被缓存多长时间。

### 安全性和兼容性

- **安全检查**：预检请求是一种安全机制，用于防止不受信任的或不允许的跨源请求对服务器资源的访问。
- **透明性**：对于前端开发者而言，浏览器自动处理预检请求，通常无需手动干预。
- **兼容性**：所有现代浏览器都支持 CORS 和预检请求，但老版本的浏览器可能不支持。

总结来说，预检请求是 CORS 中的一个关键环节，它通过让服务器声明哪些类型的跨源请求是可接受的，来增强跨源请求的安全性。

在实际构建中，我发现 Chrome 在发送请求的时候，并不会每次都发送预检，从最上面的代码片段里，可以看到 `add_header 'Access-Control-Max-Age' 1728000;` 代表一次预检的有效期，但是并不能总是按照这个时间，具体我没看过 spec，只是一旦发送预检，如果无法收到 204，则正式的请求根本不能发送，直接就会报错。

### PHP 的问题

我的项目使用 PHP 作为后端，我发现，如果框架层面没有设置好响应 OPTION 的时候，PHP 框架会将 OPTION 请求当做 GET 来处理，但是 OPTION 请求是 Chrome 自动发送的，所以不可能携带 Cookie，这样一来，如果 Nginx 如果不做适当处理，就会出现预检失败。

像本文开头的配置，是可以的，单独处理了 OPTION 请求的返回。如果不这样配置，就会出现我说的问题。

## HTTP 错误的处理

在实际构建中，我发现，请求出现 HTTP 错误的时候，Chrome 也会检查 CORS 策略，但是，Nginx 在错误的时候，不会主动发送跟 CORS 有关的头。这会导致浏览器直接触发 CORS 错误，而不是正确把错误传递到前端的代码。

这会带来很糟糕的体验，因为无法判断错误的原因。需要在 Nginx 进行特定的配置。

```nginx
if ($request_method = 'POST') {
   add_header 'Access-Control-Allow-Origin' '*' always;
   add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
   add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization' always;
}
```

像上面的配置，增加一个 `always`，这个配置表示，即使发生 HTTP 错误，返回值不是 2XX，也要依然返回 CORS 头。只有这样前端代码才能访问出现的错误，进行正确应对。

## HTTP 头的访问

在跨域环境下，不是所有的 HTTP 的头都能正确访问的：

```nginx
Access-Control-Expose-Headers: X-My-Custom-Header, X-Another-Custom-Header
```

要增加上述的配置。才能让 js 正确访问 header 中携带的信息。主要解决一些通过 header 进行鉴权的系统。
