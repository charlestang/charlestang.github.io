---
title: 【PHP】header函数的陷阱
tags:
  - PHP
  - source code
id: '554'
categories:
  - - something-about-daily-work
    - PHP
  - - 工作相关
date: 2013-05-08 14:41:53
---

PHP的header函数用来发送Http头信息，我在使用中，有个场景，就是代理请求的场景。

从服务器A代理请求服务器B，然后把B的回包透传回客户端浏览器。

这里面尤其重要的是Cookie，因为我要实现Cookie换域，因为Cookie种在服务器B的域名上，我要替换其种在A的域名上，于是就有了这么一个代码：

        

```php

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HEADER, true);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        $result = curl_exec($ch);

        $temp = explode("\r\n\r\n", $result, 2);
        $header = $temp[0];
        $content = $temp[1];

        $matches = array();
        $ret = preg_match_all('#^Set-Cookie.*$#m', $header, $matches);
        if ($ret) {
            foreach ($matches[0] as $cookieinfo) {
                $cookieinfo = str_replace('server.b.domain.com', 'server.a.domain.com', $cookieinfo);
                header($cookieinfo);  // <--- 陷阱就在这里，Set-Cookie不止一行，
                                      //      但是header函数的第二个参数replace，默认是true，
                                      //      所以，理论上只有最后一个cookie会被正确种上
                                      //      这个bug困扰了很久，引以为戒，应改为header($cookieinfo, false);
            }
        } 

```