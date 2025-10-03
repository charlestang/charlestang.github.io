---
title: Vim 常用小窍门收集
tags:
  - tips
  - tricks
  - usage
  - vim
id: '440'
categories:
  - - 技术
    - 工具
permalink: vim-tricks-collections/
date: 2011-06-14 22:31:30
updated: 2025-09-25 23:07:30
---

Vim 应该是现在世界上最流行的编辑器，没有之一。就算你千般百般地不喜欢它，掌握它也成了一件必须的事情了。因为日后你如果做程序员，在非 Win 系列的服务器上搞开发，Vim 绝对是无法避免的。你日常能接触到的 server，emacs 可能没装，但是 Vi 不可能没装，就这样。

特意开辟这个文章，用于收藏一些工作中常用的操作，主要有这么几个原则：

1.  非常有用
2.  不常用
3.  每次用都想不起来应该怎么用

不知道大家是不是经常跟我一样有这种感受呢？我会把我遇到的这类操作，都详细写在这里。

## 简单的列编辑

比如：将配置文件中的指定列前面加上注释符号。

```php
#fastcgi.conf
fastcgi_param GATEWAY_INTERFACE CGI/1.1;
fastcgi_param SERVER_SOFTWARE nginx;
fastcgi_param QUERY_STRING $query_string;
fastcgi_param REQUEST_METHOD $request_method;
fastcgi_param CONTENT_TYPE $content_type;
fastcgi_param CONTENT_LENGTH $content_length;
fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
fastcgi_param SCRIPT_NAME $fastcgi_script_name;
fastcgi_param REQUEST_URI $request_uri;
fastcgi_param DOCUMENT_URI $document_uri;
fastcgi_param DOCUMENT_ROOT $document_root;
```

如上代码是一个很常见的配置文件，我现在要给第 2-12 行前面都加上一个 # 号，注释掉他们，在 EmEditor 里面这个事情无敌简单的，但是到了 Vi 里面，你是不是总也想不起来应该怎么弄？

```raw
:2,12s/^/#/g
```

解释一下，【2,12】在 Vi 中叫 range，看帮助的时候，如果看到 range，这就是一种写法，表明第 2 行到 12 行。  
还有一种写法：

```raw
:s/^/#/g 11
```

将光标移动到第二行，然后执行上面的命令，后面的【11】代表，执行这个命令，重复11次。这里一直没解释里面那个至关重要的乱码串，那个就是替换的命令了。下次再说。

## 删除的时候使用 f 和 t

删除是 Vim 里面非常常用的功能，一个一个字幕删除，用 x，可以代替 del 用。整行删除，dd，应该都会了。删除一个单词，用 dw。这些都是简单提一下，我主要讲两个很好用的功能，就是 f 和 t。

f 的本意是行查找，fa，就是从光标当前位置开始，在本行中，找到第一个字母 a，和 d 结合起来以后，就非常方便了，比如：  
  
在这个代码里，你想删掉第一个参数，可以把光标放在(后面的第一个$上，然后按"df,"，就可以把$a连同后面的逗号都删掉，非常方便。当然了，你可以发挥一下，"d2f,"这个按键序列就是把$a和$b都删掉了，但是呢，用数字这种东西，在实际操作中，我感觉大脑经常反应不过来，需要思考，不实用。

在来说一下 t，t 这个东西，跟f非常像，区别就是t把找光标放到找到的那个字符前面一个位子，比如上面那个例子，我把光标放在第一个 $ 上，然后按下 "dt)" 这个序列，可以把函数的 3 个参数都删掉，但是却不会删掉括号，非常舒服，在括号里删东西，我经常用这个功能。

## 惹人烦恼的^M

久用 Vim 的人，可能会遇到这样的情况，打开一个从别的环境拷贝过来的文件，发现每一行的末尾都有一个^M，非常恼人。

这个问题产生的原因，是因为三种系统的换行符定义不一样造成的。在Dos系统下，行结束符为\r\n，在linux下，行结束符为\n，在Mac下，行结束符为\r，当一个文件在一个系统上编辑，然后拷贝到另一个系统打开的时候，就会出现^M，事实上，还会出现别的恼人情况，比如一打开，发现没有任何断行，这在理论上完全可行，但是估计在Google搜索，这会是另一个问题，其实都是同一个起因。

Vim下面有两个变量 fileformat 和 fileformats，简写为 ff 和 ffs。当你发现文件没有断行或者有 ^M 的时候，你有几种选择。

在 Linux 上，看到 ^M 可以执行 dos2unix，然后将 Windows 文件的 \r\n 转换成\n，然后发现 ^M 消失了。

还可以，:set ff=win，让 linux 下的 Vim 按照 Windows 格式来解析文件。当然也可以查找替换把 ^M 给替换掉。

除此之外，还可以用ffs添加到配置文件来告诉 Vim 按照怎样的顺序来尝试适配。

比如我在 Mac 系统下，set ffs=mac,unix,dos，这样，一般情况下我打开任何系统过来的文件，都能按照正确的格式显示。

## 最好看的配色方案

常用Vim的人，经常会为了配色方案而纠结，仿佛每一种都不是特别好看。其实我也这么觉得的，我分析下来，原因可能是，为Vim贡献配色方案的，大都是西方人，他们的眼睛是蓝色的，感受到的对比度，饱和度，亮度，和东方人的黑眼睛看起来是不一样的。所以他们配出来的配色方案，我们东方人，怎么着都觉得不太好看。

当然，还是能找出来一些能够勉强一看的。我个人比较熟比较习惯的是自带的evening和desert，感觉多不错，而且对我用到的好几种语言，都有不错的表现。

最近，还发现了一套非常强大，经过精心设计的配色方案，叫 solarized，在圈子里影响也很大，http://ethanschoonover.com/solarized 特此推荐给大家，因为，我觉得它配色还算是相当舒服的，对比略低，但是不影响美观。

## 编码相关Encoding

使用:set fileencoding 可以显示文件的编码格式，简写形式是 :set fenc，使用 :set fenc=utf-8 可以转换文件的编码格式为 utf-8

使用 :set encoding 可以显示编辑器当前使用什么编码方案来展示文档，简写为enc，如果utf-8文档使用非utf-8显示，汉字会出现乱码，使用:set enc=utf-8可以将vim使用的编码方案切换的utf-8

## Tab view

用一个vi编辑器，打开多个代码文件，vim从7.0版本开始，支持文件标签页，使用方法也非常简单，使用:tabnew filename来打开一个新文件，就会自动出现在新tab里面，并且在打开文件超过两个的时候，顶部出现标签控制行。

`#在vim中，用新tab打开文件   :tabnew filename`

#在命令行中，用标签页一次打开多个文件  
$ vim -p filename1 filename2 filename3

#在vim中，各个标签页的切换  
:tabn #下一个tab  
或者 gt  
:tabp ＃上一个tab  
或者 gT

`#搜索已经打开的tab   #tabf keyword`

## 手动加载代码高亮

比如，你使用 Vim 从头开始编辑一个 Shell 下的脚本，这个脚本是个命令，所以，一开始你没有给这个脚本设置扩展名，你会在脚本的开头使用 shabang 来指定解析器，后面用 chmod +x 后就可以执行了。

这时候，你发现写了几行代码后，代码高亮并没有生效，是因为你刚开始编辑文件的时候，文件名没有扩展，而且文件的内容全空。所以无法匹配正确的语法高亮，这个时候，你可以保存，然后重新打开文件，那也可以激活代码高亮。Vim 可以通过 shabang 来识别语法类型。

如果你不想这么麻烦，先保存关闭再打开，你可以执行命令：

```raw
:filetype detect
```

当然，如果你没有写扩展名，也不写 shabang 的话，那是没用的。