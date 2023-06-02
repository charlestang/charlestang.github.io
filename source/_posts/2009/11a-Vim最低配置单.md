---
title: Vim最低配置单
tags:
  - vim
id: '356'
categories:
  -   - 工作相关
date: 2009-11-10 22:54:56
permalink: the-absolute-bare-minimum-vimrc/
---

初次安装vim编辑器时，我们必须要配置~/·vimrc文件才能让vim变得更加好用。最少最少，你要配置下面一些内容：

> ```txt
> " 不再与老旧的Vi兼容
> set nocompatible
> 
> " 开启filetype支持
> filetype on
> filetype plugin on
> filetype indent on
> 
> " 语法高亮
> syntax on
> 
> " 这个选项为什么不是默认的？
> set hidden
> 
> " 执行宏的时候不要更新显示set lazyredraw
> 
> " 至少让你知道当前是在什么状态下
> set showmode
> 
> " 启用增强的命令行自动补全。必须再编译时开启 +wildmenu 选项
> set wildmenu
> 
> " 更容易的编辑此文件，即vimrc文件。用ev命令表示edit vimrc。
> nmap <silent> ,ev :e $MYVIMRC<cr>
> 
> " 并且令配置立刻生效，用sv命令表示source .vimrc
> nmap <silent> ,sv :so $MYVIMRC<cr>
> ```

==========

上面一些选项还有很多我不懂的，以后研究明白了再添加解释。此文就作为我学习使用vim编辑器的起点吧~~