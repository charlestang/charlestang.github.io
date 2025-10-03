---
title: brew 安装 PHP54 失败
tags:
  - brew
  - mac
  - PHP
id: '655'
categories:
  - - 历史归档
permalink: brew-install-php54-failed/
date: 2014-11-17 15:34:37
updated: 2025-10-03 11:38:50
---
今天使用brew安装PHP54，结果发现出现如下错误：

<!-- more -->

```shell
TCRMBP➜  Homebrew  brew install php54
==> Installing php54 from homebrew/homebrew-php
==> Downloading http://www.php.net/get/php-5.4.33.tar.bz2/from/this/mirror
Already downloaded: /Users/charles/Library/Caches/Homebrew/php54-5.4.33
==> ./configure --prefix=/usr/local/Cellar/php54/5.4.33 --localstatedir=/usr/local/var --sysconfdir=/usr/local/etc/php/5.4 --with-config-fi
checking for krb5-config... /usr/bin/krb5-config
checking for DSA_get_default_method in -lssl... no
checking for X509_free in -lcrypto... yes
checking for pkg-config... no
configure: error: Cannot find OpenSSL's 

READ THIS: https://github.com/Homebrew/homebrew/blob/master/share/doc/homebrew/Troubleshooting.md#troubleshooting
If reporting this issue please do so at (not Homebrew/homebrew):
 https://github.com/homebrew/homebrew-php/issues

/System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/net/http/response.rb:119:in `error!': 400 "Bad Request" (Net::HTTPServerException)
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/net/http/response.rb:128:in `value'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/net/http.rb:913:in `connect'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/net/http.rb:862:in `do_start'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/net/http.rb:851:in `start'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/open-uri.rb:313:in `open_http'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/open-uri.rb:709:in `buffer_open'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/open-uri.rb:210:in `block in open_loop'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/open-uri.rb:208:in `catch'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/open-uri.rb:208:in `open_loop'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/open-uri.rb:149:in `open_uri'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/open-uri.rb:689:in `open'
from /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/lib/ruby/2.0.0/open-uri.rb:30:in `open'
from /usr/local/Library/Homebrew/utils.rb:323:in `open'
from /usr/local/Library/Homebrew/utils.rb:355:in `issues_matching'
from /usr/local/Library/Homebrew/utils.rb:383:in `issues_for_formula'
from /usr/local/Library/Homebrew/exceptions.rb:147:in `fetch_issues'
from /usr/local/Library/Homebrew/exceptions.rb:143:in `issues'
from /usr/local/Library/Homebrew/exceptions.rb:182:in `dump'
from /usr/local/Library/brew.rb:163:in `rescue in'
from /usr/local/Library/brew.rb:66:in `'
```

这个东西怎么造成的呢，其实MacOS系统升级Yosemite后，系统include目录又没了，执行如下命令即可修复这个问题：

```shell
sudo ln -s /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.10.sdk/usr/include /usr/include
```

这个命令是把XCode目录下的include文件给链接到 /usr/include，其实很多configure错误，都可能是这个造成的。如果安装别的失败也可以这么试试。