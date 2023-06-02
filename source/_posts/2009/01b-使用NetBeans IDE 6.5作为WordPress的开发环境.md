---
title: 使用NetBeans IDE 6.5作为WordPress的开发环境
tags:
  - debug
  - development
  - IDE
  - NetBeans
  - WordPress
id: '287'
categories:
  - [WordPress, Plugins Develop]
date: 2009-01-30 14:27:25
permalink: use-netbeans-to-develop-wp/
---

从一个大牛那里看到了[介绍NetBeans IDE for PHP的文章](http://wp.gdragon.info/2008/11/22/wordpress-and-netbeans-ide/)，立刻下载下来尝试。立刻被它那强大、便捷、体贴的开发功能所吸引。本文主要介绍我在安装、试用、开发过程中的一些使用体验及感受。

![](http://lh6.ggpht.com/_QYicOeu89Bk/SXNOTOsS87I/AAAAAAAABBM/KsNZMHoMzMw/s400/NetBeans-01.png "NetBeans Web Site")
<!-- more -->
### 从NetBeans官方网站下载IDE

打开[NetBeans的官方网站](http://www.netbeans.org/)，点击Download，可以看到下载页面，如果没有其他的开发需求，选择for PHP的版本即可，大小只有26MB。

上面的语言选择框，大家不要费神去选了，我试过了，选择English和简体中文，下载下来的东西都是同一个，都是Multi-Language版本，而且安装的时候，不可以选择语言，NetBeans会根据系统的语言设定，来自动选择语言。据说可以通过修改配置文件的方式来更改界面语言，想用英文的同学，请自己Google之。

运行NetBeans IDE需要java虚拟机，如果需要开发java的同学，可以只下载JRE，很简单，打开http://java.com，下载即可。有些像我一样，想要以防万一的同学，可能想要安装JDK，那么[下载地址在这里](http://cds.sun.com/is-bin/INTERSHOP.enfinity/WFS/CDS-CDS_Developer-Site/en_US/-/USD/VerifyItem-Start/jdk-6u11-windows-i586-p.exe?BundledLineItemUUID=7R5IBe.ms04AAAEem.tX3uQi&OrderID=IP5IBe.mZV4AAAEeketX3uQi&ProductID=DY5IBe.ogAkAAAEdcjBGb7Et&FileName=/jdk-6u11-windows-i586-p.exe)。我给出的链接是JDK 6 Update 11 for Win版本。

先安装JRE（或者JDK），然后再安装NetBeans IDE 6.5。下面的图是NetBeans装好启动后的样子。

[![](http://lh6.ggpht.com/_QYicOeu89Bk/SXNb1hh4a7I/AAAAAAAABBU/cfCq3tgTPc0/s400/NetBeans-02.png)](http://picasaweb.google.com/lh/photo/VM7-kFI4WBZdSutP-wArPg?feat=embedwebsite)

### 将WordPress导入到NetBeans中

要开发WordPress的插件和主题，需要将整个WordPress作为项目导入到NetBeans中。

[![](http://lh6.ggpht.com/_QYicOeu89Bk/SXNb11gLmJI/AAAAAAAABBc/QSYA8anbB2Q/s400/NetBeans-03.png)](http://picasaweb.google.com/lh/photo/VdQQf2p0P-5QqGY1AHJuBQ?feat=embedwebsite)

步骤1：选择项目。“**文件->新建项目**”，然后选择PHP项目里的“**基于现有源代码的PHP应用程序**”。

[![](http://lh4.ggpht.com/_QYicOeu89Bk/SXNb2AhYMPI/AAAAAAAABBk/gY9mJReyGm8/s400/NetBeans-04.png)](http://picasaweb.google.com/lh/photo/_huaRF-0nzBtKkX57MHESA?feat=embedwebsite)

步骤2：名称和位置。在源文件夹中填入本地WordPress所在的目录。填入项目名称，可随意。其他如上图所示即可。

[![](http://lh6.ggpht.com/_QYicOeu89Bk/SXNb2KbK0GI/AAAAAAAABBs/dpvS7jvyI9M/s400/NetBeans-05.png)](http://picasaweb.google.com/lh/photo/72StQpojQH-gZu8N1eTTsw?feat=embedwebsite)

步骤3：运行配置。填入项目URL即可，为了在本地调试，一般会填入本地地址如http://localhost/wp27/。其他如上图所示。

### 使用XDebug进行调试

NetBeans支持PHP的调试。调试功能需要XDebug的支持，这是一个PHP扩展，你的服务器上可能已经装了，也可能没有装，不过，安装起来非常方便，对于Windows下的用户来说，只是下载一个DLL文件，然后拷贝到指定的目录即可。

1.  到[这里](http://www.xdebug.org/)下载XDebug，注意匹配DLL与PHP的版本号。在链接里的网页上，点击obtaining，进入下载页面，鼠标放在下载链接上，可以在状态栏看到将要下载的文件名。php_xdebug-2.0.x-5.x.x-xxx.dll，后面一个是PHP的版本号，要与你安装的版本相符合。（PHP版本可以用phpinfo()来查看）
2.  下载后，将DLL文件拷贝到PHP扩展文件夹，一般是/php/ext/下面。
3.  修改php.ini文件，这个文件的所在一般取决你php是怎么安装的，可能在system32里（bin安装的用户），也可能在php根目录下（使用zip安装的），也可能在apache/bin/目录里（使用xampp的用户），注意，一定要找到起作用的那个php.ini，这个也可以在phpinfo()里面看。添加下面的代码。

```XML

[xdebug]
zend_extension_ts="D:/xamp/php/php5.2.5/ext/php_xdebug.dll"
xdebug.remote_enable=On
xdebug.remote_host="localhost"
xdebug.remote_port=9000
xdebug.remote_handler="dbgp"

```

5.  注意：上面的代码段，可能php.ini里已经有了，而是被注释掉了，那么你去掉上述那几行字的注释就可以了。另一个注意点，[xdebug]段的配置和[zend]段的配置不能共存，否则apache启动不了，添加了上述代码，如果启动不了apache，那么查找是否存在[zend]段的配置，然后注释掉，我是XAMPP安装的环境，就碰到了这个问题。
6.  重启WebServer。

做过上述操作后，NetBeans就可以感知到调试器的存在了。

### 一般项目开发

我们已经将wp2.7的所有文件都导入到了NetBeans里面，那么具体开发一个插件项目，或者主题项目的时候，我们可以在项目面板上，将某个插件的根目录，或者某个主题的根目录使用如下方法添加到收藏夹，以后就在收藏夹面板下工作即可。

[![](http://lh6.ggpht.com/_QYicOeu89Bk/SXQm5QcgZgI/AAAAAAAABCI/LschHqVw95s/s400/NetBeans-06.png)](http://picasaweb.google.com/lh/photo/hhddQGqFo5spU-RHEYu5EA?feat=embedwebsite)

收藏夹完全可以充当项目开发面板的工作。下图就是添加后的效果。

[![](http://lh4.ggpht.com/_QYicOeu89Bk/SXQm5R7KO3I/AAAAAAAABCQ/eCJGK5dmT44/s400/NetBeans-07.png)](http://picasaweb.google.com/lh/photo/yxGkDHD97csGUsjQq-1wsw?feat=embedwebsite)

### 配置项目运行

一般，调试主题或者插件，都是某个特定的页面，比如归档页面，静态页面，或者某个单篇日志页面。如果只是主页，那么默认的设置即可了，如果不是主页，那么需要指定启动参数。大家可能习惯了修改永久链接后的WP的页面地址了，但是那个在调试环境下行不通，必须还原到query string的模式。

[![](http://lh6.ggpht.com/_QYicOeu89Bk/SXQm5s9b7WI/AAAAAAAABCY/3Q46QF5Ep90/s288/NetBeans-08.png)](http://picasaweb.google.com/lh/photo/h1f6Q97r497VcvVsjDqEiw?feat=embedwebsite)

从上图菜单中打开对话框，配置方式如下：

[![](http://lh5.ggpht.com/_QYicOeu89Bk/SXQm51I5xvI/AAAAAAAABCg/xKcJIjLmt5Q/s400/NetBeans-09.png)](http://picasaweb.google.com/lh/photo/h3NjHTgKkJieuN0igO050w?feat=embedwebsite)

注意上图中红色框框里的部分，这个例子就是指定显示id为289的页面或者日志。

设置好运行设置，调试时也会使用这个参数。

调试的时候从调试菜单进去，打开调试对话框，如果只需要调试PHP的话，选第一项，如果还需要调试Javascript的话，选第二项，可以选择你喜欢的浏览器。（有些平台上不能选，Win上面没有问题）

[![](http://lh4.ggpht.com/_QYicOeu89Bk/SXQr9cJq2pI/AAAAAAAABC4/VKmLbv8P5Lw/s400/NetBeans-10.png)](http://picasaweb.google.com/lh/photo/oiZKeAf0OYTcBYbDGQC_vw?feat=embedwebsite)

使用FF，初次选择Javascript调试，会要求安装一个FF插件，装上即可。

好了，作为一个简要的介绍，就写到这里了。

后记：上述内容，并非完全翻译，只是遵循了原文的条理，大部分内容都是我个人的感受和体验，当然，图也是我自己重新截取的。NetBeans作为一款PHP的开发工具，与Eclipse版本的ZendStudio相比，更加的平易近人，比较简单，没有很多复杂的选项，与UEStudio相比，智能化更强，集成的功能更丰富，而且可以和浏览器联调。

这两天，都在使用NetBeans作为环境开发插件，觉得真的很不错。尤其是在WP下，NetBeans会自动对所有代码文件建立索引，你在某个函数上单击，该函数会被高亮，然后用Ctrl+B或者右键菜单，可以直接跳到函数的声明，非常的方便。仅有的一个小缺点是，NetBeans无法对PHP内建函数使用有区别的高亮颜色，不过大家对PHP的内建函数应该也比较熟悉了，再加上，你在内建函数上Ctrl+B，也可以跳到一个类似C语言H文件的文件里，可以直接查看这个内建函数的函数头和说明，都省了查阅手册的时间，也算是弥补了那个小缺点。

还有一点我比较欣赏的，就是NetBeans支持代码重构，可以自动格式化，支持javadoc格式的注释风格，使用这个编辑器可以创建非常优美的注释格式。最后，这个基于java的IDE当然也是跨平台的，以后可以一直用下去了，嘿嘿~~

赶快试试吧！祝大家新年好运~~