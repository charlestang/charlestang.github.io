---
title: Lucene笔记02
tags:
  - lucene
  - note
id: '278'
categories:
  -   - 工作相关
date: 2008-12-17 14:15:29
permalink: lucene-note-02/
---


<!-- more -->
要完成最基本的建立索引的过程，Lucene需要以下几个对象的合作：

*   IndexWriter——Lucene内部用来创建索引的最重要的组件。可以创建新索引，或者从文档增量地创建索引。
*   Directory——Directory是一个抽象类，用于表达索引存放的目录，在lucene内部提供了两个实现，一个是FSDirectory，一个是RAMDirectory，顾名思义了。Directory可能在内部提供了锁的机制，使得建立索引和搜索可以同时进行。
*   Analyzer——又是一个抽象类，是IndexWriter的构成组件之一，主要用来分析文本，包括分词，去除stop words等等功能。在构建一个项目的时候，选取或者创建正确的分析器是至关重要的。
*   Document——是Lucene处理的对象，一个Document是一组Field的集合
*   Field——Lucene建立的索引中，每个Document都包含一个或者多个命名的域，被包装在Field类中，Field有多种的类型，Keyword，UnIndexed，Unstored，Text

按照书中的说法，在进行一个最简单的建立索引的过程时候，必须要用到这几个类，但是上一次的笔记中，我也帖了我敲的代码，貌似则个Directory是没有直接在Indexer的代码中提到的，不过，我进IndexWriter的构造函数看了一下，其实是用到的，如果我们在构造一个IndexWriter的时候，没有传递一个Directory给它，而是只传了一个路径，那么会默认使用FSDirectory对像的，这是一种使用了简单锁机制的Directory对象。