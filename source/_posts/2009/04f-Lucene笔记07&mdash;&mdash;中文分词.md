---
title: Lucene笔记07&mdash;&mdash;中文分词
tags:
  - lucene
  - note
id: '345'
categories: 历史归档
permalink: lucene-note-07/
date: 2009-04-28 16:55:10
---


<!-- more -->
### 什么是分词？什么是中文分词？

分词，就是将一段文字，按照语义上的最小单位切割开来。对于中文来说，虽然，很多汉字本身就具有相对独立的意思，但是更多情况下，单个的汉字是与其他一个或多个汉字组合在一起形成一个含义的。举个例子，“我是一个学生”，分词的结果是：“我/是/一个/学生”，再比如，“我/打算/去/做/分词/的/研究”。中文分词，就是将中文段落划分成词。

分词是理解语义的前提。人类依据自身的知识，在看到文字的时候，就自动完成了分词的过程。然而，计算机不具备人类的知识，更加不具备人类的智能，让机器实现自动切分文本，就成为了一个重要的研究课题，隶属于自然语言处理技术领域。在各种语言的分词中，最为困难的，可能就是中文分词了，因为中文语法复杂，规则少，特例多，歧义性强。中文领域文本处理技术，大大落后于西文，分词就是制约因素之一。

分词是搜索引擎建立索引的重要环节。我们固然可以对单个汉字建立索引，但是那样建立的索引，体积庞大，效率低下，检索缓慢，精确率低。分词完毕后，就能大大减少索引的体积，提高检索的效率。对于检索领域来说，分词可能仍非必要环节，但是对于自然语言处理领域来说（典型的如机器翻译），分词就必不可少。

### 分词的基本方法

分词一般有三种方法，基于字符串匹配的分词方法，将一段文本，与一个充分大辞典，逐条进行匹配，实现分词。按照长度优先级的不同，可以分为最大匹配、最小匹配；按照匹配方向的不同，可以分为正向匹配、逆向匹配。这些方法可以互相组合。

基于理解的分词方法，这种方法让计算机模拟人对句子的理解，对句子进行语法分析，语义分析，最后实现分词。该方法实现难度大，需要大量的语言知识和信息，目前还没有可生产的系统。

基于统计的分词方法，是通过对大量语料统计两个字相邻出现的频率，识别出词的方法。该方法虽然不需要辞典，而且能够实现对新词的识别。

三大类分词方法，各有利弊，参见文献【2】，现实中的分词系统，往往是综合系统，也即两种以上方法的综合，以此实现最优的分词效果。

### 在Lucene中分词

在Lucene中执行分词任务的是Analyzer对象，该对象中最关键的方法，是tokenStream方法，该方法可以返回一个包含着token的集合，也即TokenStream对象。TokenStream本身，是一个有着类似迭代器接口的抽象类，其具体类有两种，一种是以Reader对象作为输入的Tokenizer对象，另一种是以另一个TokenStream对象作为输入的TokenFilter。

到此，我们已经不难看出，实际执行切割任务的是Tokenizer，而TokenFilter则正如其名，对切割的结果进行过滤。要得到一个分词完毕的结果集合，必须要各类Tokenizer和TokenFilter的合作才可以完成，而Analyzer在这里，就扮演着一个组装器的角色。

从StandardAnalyzer中，我们不难发现Lucene的思路。首先创建一个StandardTokenizer实现第一次切割，然后是StandardTokenFilter，实现对token的归一化，如将复数词变成单数词，接着是一个ToLowerCaseFilter，将所有的token转换成小写字母，最后是StopFilter，将所有的stop words（无意义虚词）去掉。这样就完成了对一个英文文字段落的分词。

这样的设计，将复杂的分词实现全部对用户透明，用户具体使用的时候，就非常容易，只要创建一个Analyzer对象，然后传递给IndexWriter或者QueryParser（分解用户的查询，第一个步骤也是分词）即可。

### 在Lucene中实现中文分词

有了上面的理解，我们就知道，要让Lucene能够实现中文分词，我们必须创建自己的Analyzer，以及与其相关的Tokenizer和TokenFilter，有了这几个类的配合，就可以实现中文分词。

我在网上调研了数个中文分词系统，但是，里面实现了Lucene接口的并不多，好在我只是做一般性科研用途，对性能，效率不需考量，所以，我就直接选择了按照Lucene的接口设计的Paoding Analysis包。如果，我们期望能够得到更高的精确率和分词效率，我们还需要选用更加优秀的分词组件才行，那时候，就必须要自己手动来进行一次封装，以实现Lucene的接口，不过，这并不是一个复杂的事情。很多分词组件本身已经非常全面，例如ICTCLAS，已经实现了定制化分词，其给出的结果，就直接是最终结果了，所以，如果要包装ICTCLAS，我们要做的事情就很简单了，将ICTCLAS返回的结果，用TokenStream包装即可，可能单实现一个Analyzer就足够了。即便考虑得全面一些，事情也不会太复杂。

### 总结

市面上的中文分词组件非常多，一般应用，我们完全可以采用现成的系统。没有必要重复发明轮子。但是这些系统大多数难以适用于要求更高的商业系统，那时候就不得不选购一些相关的解决方案，或者在某开源系统的基础上进行再开发。

我个人在实际项目中，选用了Paoding Analysis，主要考虑到该实现完全使用Java，具有优秀的跨平台特性，而且用起来也最为省心，分词效果也还不错。虽然效率可能存在一定的问题，但是由于系统本身内容较少，也就不是矛盾的主要方面了。日后可以考虑更换更为高效和更为准确的系统。当然，前提是你在构建系统的时候，不要将你使用的Analyzer硬编码进系统，而是使用配置文件等方式来接入。

参考文献：

【1】百度百科：中文分词 [http://baike.baidu.com/view/19109.html](http://baike.baidu.com/view/19109.html "http://baike.baidu.com/view/19109.html") （中文分词的基本方法，技术难点，基本应用）

【2】三种中文分词算法优劣比较 [http://www.blogjava.net/jiangyz/articles/238120.html](http://www.blogjava.net/jiangyz/articles/238120.html "http://www.blogjava.net/jiangyz/articles/238120.html")

【3】[开源中文分词软件](http://www.coreseek.com/forum/index.php?action=vthread&forum=1&topic=2)

【4】[Lucene中文分析器的中文分词准确性和性能比较](http://approximation.javaeye.com/blog/345885)

【5】[几款免费中文分词模块介绍](http://searcher.org.cn/search/20070903/98.html) （原文已经丢失）

【6】[关于中文分词的一些琐碎资料](http://www.webryan.cn/2009/04/something-about-chinese-seg/)

常见分词系统：

【1】中科院计算所ICTCLAS [http://ictclas.org/index.html](http://ictclas.org/index.html "http://ictclas.org/index.html") （很多企业和研究机构的分词系统，带有词性标注，便于搞科研）

【2】海量信息技术有限公司的中文智能分词 [http://www.hylanda.com](http://www.hylanda.com "http://www.hylanda.com") （据说是中搜使用的分词系统，传说业界公认最好的分词）

【3】猎兔 中文分词 [http://www.lietu.com/demo/index.jsp](http://www.lietu.com/demo/index.jsp "http://www.lietu.com/demo/index.jsp")

【4】极易中文分词组件 [http://www.jesoft.cn/](http://www.jesoft.cn/ "http://www.jesoft.cn/") （基于正向最大匹配算法）

【5】庖丁解牛中文分词 [http://code.google.com/p/paoding/](http://code.google.com/p/paoding/ "http://code.google.com/p/paoding/") （开源项目）

【6】简易中文分词系统 [http://www.hightman.cn/index.php?scws](http://www.hightman.cn/index.php?scws "http://www.hightman.cn/index.php?scws") （提供php扩展）

【7】还有许多许多