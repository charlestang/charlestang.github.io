---
title: Lucene笔记06
tags:
  - lucene
  - note
id: '340'
categories:
  - 工作相关
date: 2009-04-14 19:36:41
permalink: lucene-note-06/
---


<!-- more -->
在[笔记03](http://blog.charlestang.org/lucene-note-03.htm "Lucene Note 03")中，已经提到了使用Lucene进行搜索的几个必要组件：

*   **IndexSearcher**——该对象内包含了很多search方法的重载，搜素一个索引，主要就是使用该对象的实例。
*   **Query**——该类是一个抽象类，其派生类产生的对象，是对各种形式搜索的封装。
    *   TermQuery——匹配那些包含单个查询词语（term）的文档。可以使用BooleanQuery进行组合。
    *   BooleanQuery——匹配由其他查询（TermQuery或PhraseQuery或者BooleanQuery）布尔组合后形成的查询的文档。
    *   FuzzyQuery——模糊查询。
    *   RangeQuery——范围查询。
    *   还有很多……
*   **QueryParser**——将人类语言翻译成上述某种Query对象。
*   **TopDocs**——搜索结果的容器。TopFieldDocs是其派生类，也是存放搜索结果的容器。

上面已经提到了，IndexSearcher中有很多重载的search方法，不过我仔细看了一下，建议使用的并不多。

```java
public TopFieldDocs search(Query query, Filter filter, int n, Sort sort)
public TopDocs search(Query query, Filter filter, int n)
public TopDocs search(Query query, int n)

//following low-level
public void search(Query query, HitCollector results)
public void search(Query query, Filter filter, HitCollector results)
```

Filter是一个抽象类，就像其名字标识的一样，该对象将会过滤搜索结果，挡住一些结果，放行另一些。如果我们在建立索引的时候，对日期按照YYYYMMDD的格式建立了索引，那么我们在搜索的时候，可以使用PrefixFilter来查询某一年YYYY的文档。另外，我们也可以使用RangeFilter来搜索某个特定字段存在于某个范围内的文档。Sort则是一个可以改变排序结果的对象，可以告诉Lucene按照某个或者某几个特定的字段排序搜索结果，还可以让Lucene将搜索结果逆序。

HitCollector是一个抽象类，其子类的对象，都要提供一个collect方法，IndexSearcher会将每个文档的id和其原始得分传递给该方法。在这里，就可以自定义对最后结果的排序算法了。这里，可以看一下默认的TopDocCollector的collect方法实现：

```java
  public void collect(int doc, float score) {
    if (score > 0.0f) {
      totalHits++;
      if (reusableSD == null) {
        reusableSD = new ScoreDoc(doc, score);
      } else if (score >= reusableSD.score) {
        // reusableSD holds the last "rejected" entry, so, if
        // this new score is not better than that, there's no
        // need to try inserting it
        reusableSD.doc = doc;
        reusableSD.score = score;
      } else {
        return;
      }
      reusableSD = (ScoreDoc) hq.insertWithOverflow(reusableSD);
    }
  }
```

默认的算法，就是根据原始分数的高低，来对搜索命中结果进行排序。实质上就是一个堆排序，这里用到的hq对象，是一个优先级队列。

1.  每传递进来一个文档id，将该文档的分数与上一次操作结束后，得分最低的文档比较（优先级队列长度是有限的，填满后，抛弃得分最低的文档）

2.  如果，得分较高，插入队列，并记录下这次操作被挤出队列的文档，否则，抛弃之。

如果我们自己来设定排序方法的话，我们可能先要调用IndexReader对象，取得我们计算排序所必须的字段，然后，在这个函数内实现我们的计算公式。这里，我就在想，是否可以更早一步地介入到Lucene的搜索过程中，比如这里，score已经计算好了，是否有机会介入到计算scroe之前的地方，这样，我们就可以用自己的公式来计算scroe。这只是一个想法，还没有进一步验证和研究。

今天看过的一些文章的摘抄：

1.  [不选择使用Lucene的6大原因](http://blog.csdn.net/accesine960/archive/2008/03/22/2207462.aspx "不选择使用Lucene的6大原因")

2.  [Moving Lucene a step forward](http://www.jroller.com/melix/entry/why_lucene_isn_t_that "Why Lucene isn't that good?") ——上面那篇中文的文章中提到的英文原文。

3.  [数学之美 系列九 -- 如何确定网页和查询的相关性](http://www.googlechinablog.com/2006/06/blog-post_27.html "The introduction of TFIDF") —— TF·IDF统计法的一个基础介绍。