---
title: Lucene笔记01
tags:
  - code examples
  - lucene
  - note
id: '272'
categories:
  - 日　　记
date: 2008-12-10 16:24:30
permalink: lucene-note-01/
---

由于项目需要，开始学习Lucene，现在手头在看的就一本书《Lucene in Action》，别的材料手头也没有，不过，有一点非常遗憾，就是这本书已经非常旧了，所以，决定一边看，一边验证，主要是参看一下源代码，也是没有办法的事情，就在博客上做点小笔记好了。
<!-- more -->
### From the very beginning

第一章，就有两个小例子，用来展示一下Lucene的功能，可惜，那两个例子是基于Lucene 1.x版本的，现在Lucene的版本已经发展到了2.4.0，并且在向3.0迈进了，很多东西的结构都变了。

两个代码例子，我照着敲了一遍，发现根本就跑不了，根据我的理解，我又改了点东西，记录在下面：

Indexer的代码范例：

```java

package MainTest;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Date;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriter.MaxFieldLength;

public class Indexer {

/**
 * @param args
 * @throws Exception 
 */
public static void main(String[] args) throws Exception {
if (args.length != 2){
throw new Exception("Usage: java " + Indexer.class.getName()+ " ");
}

File indexDir = new File(args[0]);
File dataDir = new File(args[1]);

long start = new Date().getTime();
int numIndexed = index(indexDir, dataDir);
long end = new Date().getTime();

System.out.println("Indexig "+numIndexed + " files took " + (end - start) + " milliseconds");
}

public static int index(File indexDir, File dataDir)
throws IOException{
if (!dataDir.exists() !dataDir.isDirectory()){
throw new IOException(dataDir + " does not exist or is not a directory");
}

IndexWriter writer = new IndexWriter(indexDir, new StandardAnalyzer(), true, MaxFieldLength.LIMITED);

indexDirectory(writer, dataDir);

int numIndexed = writer.maxDoc();
writer.optimize();
writer.close();
return numIndexed;
}

private static void indexDirectory(IndexWriter writer, File dir)
throws IOException{

File[] files = dir.listFiles();

for(int i = 0; i< files.length; i++){
File f = files[i];
if (f.isDirectory()){
indexDirectory(writer,f);
}else if (f.getName().endsWith(".txt")){
indexFile(writer,f);
}
}
}

private static void indexFile(IndexWriter writer, File f)
throws IOException{

if(f.isHidden() !f.exists() !f.canRead()){
return;
}

System.out.println("Indexing " + f.getCanonicalPath());

Document doc = new Document();
//doc.add(Field.Text("contents", new FileReader(f)));
//doc.add(Field.Keyword("filename", f.getCanonicalPath()));
Field contents = new Field("contents",new FileReader(f));
Field filename = new Field("filename", f.getCanonicalPath(), Field.Store.YES, Field.Index.NO);
doc.add(contents);
doc.add(filename);
writer.addDocument(doc);

}
}

```

Searcher的代码范例，这部分好像变化了很多东西啊：

```java

package MainTest;

import java.io.File;
import java.util.Date;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

public class Searcher {

/**
 * @param args
 * @throws Exception 
 */
public static void main(String[] args) throws Exception {
if (args.length != 2){
throw new Exception("Usage: java "+ Searcher.class.getName() + " ");
}

File indexDir = new File(args[0]);
String q = args[1];

if (!indexDir.exists() !indexDir.isDirectory()){
throw new Exception(indexDir + " does not exists or is not a directory.");
}

search(indexDir, q);
}

public static void search(File indexDir, String q)
throws Exception{
Directory fsDir = FSDirectory.getDirectory(indexDir);
IndexSearcher is = new IndexSearcher(fsDir);

QueryParser qp = new QueryParser("contents", new StandardAnalyzer());

Query query = qp.parse(q);

int hitsPerPage = 10;
TopDocCollector collector = new TopDocCollector(hitsPerPage);

long start = new Date().getTime();
is.search(query, collector);
ScoreDoc[] hits = collector.topDocs().scoreDocs;
long end = new Date().getTime();

System.err.println("Found " + hits.length + " document(s) (in " + (end - start) + " milliseconds) that matched query '" + q + "':");

for (int i = 0; i < hits.length; i++){
int docId = hits[i].doc;
Document doc = is.doc(docId);
System.out.println(doc.get("filename"));

}
}
}

```

以上代码都在jdk 1.6.x + lucene 2.4.0上测试通过的。