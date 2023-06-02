---
title: Lucene笔记03
tags:
  - lucene
  - note
id: '280'
categories:
  -   - 工作相关
date: 2008-12-18 09:40:03
permalink: lucene-note-03/
---


<!-- more -->
要完成最基本的搜索过程，Lucene需要以下几个对象的合作：

*   IndexSearcher——这个对象主要用来检索IndexWriter生成的索引文件，所以IndexSearcher构造的时候，使用一个包含了索引所在目录的Directory对象来构造。IndexSearcher提供的是一种对索引文件的只读访问，里面提供了多种搜索方法。在我第一次的笔记里代码中用到的search方法，接受一个Query对象和一个HitCollector对象，返回值为空。搜索结果被填充到HitCollector中。
*   Term——该对象是一个和Field相似的对象，包含一个名字和值对。但是目前，在代码里还没有遇到过这个对象，虽然书里提到在建立索引和搜索的过程中都会用到这个东西，但是实际上，我并没有看到。
*   Query——Query类是一个抽象类，在Lucene的内部有许多的实现，虽然说，书中也提到了最基本的Query是TermQuery，但是看了看内部的代码，在笔记1中提到的代码内部，实际上用到是BooleanQuery，而不是TermQuery。
*   TermQuery——最基本的Query，上面也提到了，用来匹配文档中包含的特定的域的特定的值，暂时也没有碰到过。
*   Hits——这个对象本来应该是一个简单的容器，用来包含搜索得到的排序结果的，但是实际上，在笔记1中的代码里，已经看不到这个东西了，Lucene已经不推荐使用这个东西，现在用到的东西是HitCollector似乎是一个更高级的容器了，在代码中我们看到，我们从这个对象中去除了一个Document的数组，包含的元素正是搜索结果。
*   QueryParser——这个对象在书中没有提到，实际上，我觉得必须要有的，本质上就是把一个字符串转换成一个Query对象，实际上，这个东西应该是设计得非常的复杂的，因为搜索引擎一般都提供了很丰富的搜索语法，Lucene也是一样的。构造QueryParser的时候，还可以指定专门的Analyzer。