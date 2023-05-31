---
title: 从头开始学C语言：char* 和 char 【】
tags: []
id: '643'
categories:
  - - something-about-daily-work
    - Linux
  - - 工作相关
date: 2014-09-04 23:49:49
---

想要把丢掉的东西捡起来，还是很辛苦啊，今天我就发现，我连char* 和 char []的区别都不知道。

```c

#include 

int main(int argc, char* argv[]) {
 char* buf1 = "this is a test";
 char buf2[] = "this is a test";
 printf("size of buf1: %d\n", sizeof(buf1));
 printf("size of buf2: %d\n", sizeof(buf2));
 return 0;
}

```

结果是：

```shell

$ > ./main
size of buf1: 4
size of buf2: 15

```