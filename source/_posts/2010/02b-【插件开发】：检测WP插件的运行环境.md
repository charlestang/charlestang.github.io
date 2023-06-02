---
title: 【插件开发】：检测WP插件的运行环境
tags:
  - develop
  - plugins
  - WordPress
id: '362'
categories:
  - [WordPress, Plugins Develop]
date: 2010-02-16 09:31:36
permalink: check-the-runtime-evn-of-wp-plugins/
---

WP的插件在开发完成后，会在用户的服务器上运行，而用户的服务器环境基本上可以用千奇百怪来形容。开发过程中，在本地运行得好好的插件的，一旦安装到用户的服务器上，也有可能变得无法运行。

所以，作为WP插件的开发者，最好不要对插件最终的运行环境做任何假设。而且，最好能够在插件被启用的时候，进行必要的检查，给用户以提示，对于自己没法兼容的问题，应该明确指出，避免用户遭遇不必要的麻烦。

在我个人的WP插件开发过程中，我主要遇到的问题，基本上都是PHP相关的问题。
<!-- more -->
第一个是PHP的版本问题，现在主流的PHP版本是PHP 5.x，而事实上，PHP 4.x仍旧大行其道，如果插件中用到了PHP 5的特性，那么就要想到，插件可能出现兼容问题。比如PHP 5和PHP 4在面向对象方面有一些不同，应用了新特性的插件，在旧有环境下，可能无法正常工作。

我自己遇到的一个例子是DOM Document函数扩展，在PHP 4 和PHP 5中，差别很大，没法兼容，对于这种情况，我也没有很好的办法，只能为两种版本各创建一个函数的版本。做这样的事情非常吃力，乃至我后来已经决定不再开发支持PHP 4版本的插件，只是在插件的说明中写明，未进行过基于PHP 4环境的测试工作，请用户慎重，可能无法运行。这也是一种权衡利弊，有的时候，你的时间精力都有限，可能不愿意做这种吃力不讨好的事情，那也是无可厚非的，但是最好说明这一点。

另一个问题是，个别函数的问题的。比如我遇到一个是mb_str*系列函数的问题，这个系列函数，对于中国用户来说，可能意义特别重大，因为这个系列函数可以正确处理亚洲字符和兼容UTF8字符集。而事实上mbstring这个扩展，并非是每个服务器环境都会配备的，如果调用到了系列的函数，必须要进行检测，好在有好多此系列的函数，可以通过自己实现来弥补。

一般来说，对于有可能不存在的函数，都可以通过自己实现来解决，但是这其中也有一些小陷阱，在解决这种类似的兼容问题后，最好进行全面的测试。举个例子，如果运行时php环境没有包含mbstring扩展，那么当需要调用mb_strlen函数的时候，很简单，可以用自己实现的版本；可是另一些情况就不行，我这里想举个例子，就是scandir函数，这个函数是PHP的内置函数，但是在很多服务器环境中，出于安全的考虑，可能会被禁用，常见的被禁函数有（passthru, exec, phpinfo, system, ini_alter, readlink, symlink, leak, proc_open, popepassthru, chroot, scandir, chgrp, chown, escapeshellcmd, escapeshellarg, shell_exec, proc_get_status），如果插件中用到了，最好认真针对其进行测试。我在处理scandir函数的时候，也用了自己实现函数的法子来解决，谁知道，一测试才发现了不对劲，看看这个提示：

```shell

Fatal error: Cannot redeclare scandir() in E:\Green_Software\xampp\htdocs\demos\index.php  on line 24

```

这是我遇到的错误提示。后来写了一小段代码进行了测试，才发现这个问题，scandir是内置函数，在php.ini中，通过disable_functions选项将scandir屏蔽掉后，function_exists('scandir')函数将返回false值，然而，这个函数的状态却是declared。也就是说，这个函数明明“声明”了，却并不“存在”，那么一般套用的先判断函数是否存在，再决定是否实现自己版本的做法，就失灵了，会引发上述错误。这个问题让我相当头痛，在我看来，想要完美地解决，几乎是不可能。我用了一个非常笨拙的方法，就是对这一类可能会被禁止的函数进行封装。然后在实际调用的时候，调用自己重命名过的函数版本。

综上可以知道，就算同样是function_exists返回false情况，用同一种方法，也不能一并解决所有问题。最好的办法，还是用不同的办法综合起来解决问题，并且进行尽可能全面的测试工作，最后对插件可能引发的问题进行详细的说明。

在具体开发过程中，还是不要进行任何假设，对runtime环境进行一遍检查比较稳妥，下面贴一个本人进行环境安全检查的例子：

```php



Sorry, PHP function 'scandir' is forbidden in your server, so that the plugin will not work. Please disable the plugin.

 

```



 

如上，用户会在打开后台页面时，就发现一条警告信息，说明此插件可能无法正常工作。