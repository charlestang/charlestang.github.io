---
title: PHP 开发笔记
tags:
  - PHP
categories:
  - [工作相关, PHP]
date: 2023-08-11 21:57:00
permalink: 2023/php-development-notes/
---

说起来，我也是一个从事了 PHP 开发工作至少 8 年的老人了，后来很长时间不写 PHP 代码了，不过，我觉得作为我踏上工作岗位的第一种语言，就好像人生的母语一样，还是应该捡起来这门手艺。是以为记。

## 工具

其实，PHP 世界也有各种各样的工具，只是 PHP 本身太过强大，导致大家经常不用这些工具，效率就已经够了，当然，用了的话，会更好！

### PHP_CodeSniffer

[PHP_CodeSniffer](https://github.com/squizlabs/PHP_CodeSniffer) 是一组由两个 PHP 脚本组成的工具，主要的 `phpcs` 脚本对 PHP、JavaScript 和 CSS 文件进行 Token 划分，以便检测是否违反了定义的编码标准，而第二个 `phpcbf` 脚本则可自动修复此类问题。PHP_CodeSniffer 是一种重要的开发工具，可以确保你的代码保持干净、一致。

这个工具可以使用默认的配置文件进行设置，例如 `phpcs.xml` 文件，这样就有了一个慢慢积累代码规范配置的地方。整个团队可以不断把项目的编码规范，积累到这个文件里，然后通过 code base 分发到每个程序员。

在 IDE 里，比如 VS Code 里面就默认带有了 PHP CS 相关的配置项，可以指定二进制文件的路径。

### PHP CS Fixer

[PHP CS Fixer](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer) 是另一款工具，可以修复你的代码，使其遵循标准，无论你是想遵循PSR-1、PSR-2等定义的PHP编码标准，还是其他社区驱动的标准，比如Symfony标准。你还可以通过配置来定义你（团队）的编码风格。

你可能要问了，这个 `php-cs-fixer` 命令功能和前一个工具 `phpcs/phpcbf`，是不是重复的？其实还真是。

根据[作者自己的说法](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer/issues/3459)，两者的设计理念是不同的，但是这些年发展下来，两边功能在趋同。不过几个资深的玩家，给出的结论仍然是两个都保留。因为虽然有重叠的部分，但是各有很多独特的部分。至少规则集是不完全一样的。

这款工具同样可以用配置文件来配置，例如 `.php-cs-fixer.php`，它的配置文件是一个 PHP 文件，这一点也很有特色。同理，整个团队也可以通过 code base 来分享代码格式化工具的规则。

就是我配置到了 VS Code 里发明容易报错。

### GrumPHP

因为一次又一次地要为代码质量辩护而感到疲惫不堪吗？那么 [GrumPHP](https://github.com/phpro/grumphp) 为你而生！这个 composer 插件将在你的软件包存储库中注册一些 `git hook`。当有人提交代码更改时，GrumPHP 将在提交的代码上运行一些测试。如果测试失败，你将无法提交你的更改。这个实用的工具不仅可以改善你的代码库，还可以教育你的同事按照你们团队确定的最佳实践写出更好的代码。

很有意思，这款工具也是关注代码质量的，这回事关联在 git 提交的流程里。我还没有来得及尝试这个工具。