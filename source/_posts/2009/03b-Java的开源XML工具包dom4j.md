---
title: Java的开源XML工具包dom4j
tags:
  - code
  - code examples
  - java
  - tools
id: '310'
categories:
  - 工作相关
date: 2009-03-31 00:12:59
permalink: dom4j-xml-toolkit-java/
---

![The hierarchy of the interfaces in dom4j libaray](http://lh6.ggpht.com/_QYicOeu89Bk/SafPc8W7V6I/AAAAAAAABJo/pe3JBdV_QJg/s400/dom4j-interface-hierarchy.png)

**dom4j**是一个使用简便的开源类库，专门用来在Java平台上处理XML，XPath和XSLT，该类库使用了Java Collections Framework，完全支持DOM，SAX和JAXP。

**dom4j**为一个XML文档在内存中创建了一个树对象模型。 它提供了一组强大易用的API，通过XPath和XSLT来处理、操纵或者遍历XML文件，此外其中还集成了SAX、JAXP和DOM。

为了提供高度可配置的实现策略，**dom4j**基于接口设计。只需要提供一个DocumentFactory实现，您就可以创建您自己的XML树实现。这种设计，使得在扩展dom4j以定制您需要的特性时，能非常简单地重用dom4j的代码。

本文档将通过代码实例的方式为您提供一个dom4j的实践指南。在实验室项目中，这个开源工具包给我的工作带来了很大的便利，在这篇文章中，我将对项目中用到dom4j完成的任务做个总结，以期和互联网上的众多文档能够互相补充。
<!-- more -->
### 读取XML文件

一般性地读取XML文件，在dom4j中操作起来将非常简单。

```java
public void readXMLSimple(File file) throws DocumentException{
    //使用SAXReader读取XML文件
    SAXReader sr = new SAXReader();
    Document doc = sr.read(file);
    
    //使用XPath遍历一个XML文件的结点
    Element root = doc.getRootElement();
    List entryList1 = root.selectNodes("entry");
    //或者
    List entryList2 = doc.selectNodes("/feed/entry");
}
```

### 创建一个XML文档并记录到磁盘上

创建一个XML文件，并将其写到磁盘上，也可以使用非常简介的代码来完成，假设我们将上一个代码范例中得到的entry节点的列表，插入到一个新建的XML文档中，然后使用优美的缩进格式保存在磁盘上，我们可以像下面这样编码：

```java
public void createXMLSimple(List entries, File f)
        throws FileNotFoundException, 
               UnsupportedEncodingException,
               IOException{
    Document doc = DocumentHelper.createDocument();
    doc.addElement("feed");
    Element root = doc.getRootElement();
    Iterator i = entries.iterator();
    while(i.hasNext()){
       //从别的Dom中得到的Element都有其本身
        //的root，所以必须创建副本才能插入另一个doc内
        root.add(((Element)i.next()).createCopy());
    }
    FileOutputStream os = new FileOutputStream(f);
    OutputFormat of = OutputFormat.createPrettyPrint();
    XMLWriter xmlw = new XMLWriter(os,of);
    xmlw.write(doc);
}
```

### 读取一个根节点带有默认Namespace的XML

如果我们刚才的代码范例读取的是符合Atom1.0标准的Feed，那么，根节点带有default namespace的http://www.w3.org/2005/Atom。读取这样的XML文档稍微有点麻烦，网上的代码很多，但是很多都不好用，我总结下来，基本上没有办法像你想的那么干净。

```java
public void treatDefaultNamespace(File f) 
        throws DocumentException{
    SAXReader sr = new SAXReader();
    Map ns = new HashMap();
    ns.put("atom", "http://www.w3.org/2005/Atom");
    sr.getDocumentFactory().setXPathNamespaceURIs(ns);
    //Element接口支持迭代器，在这里顺便展示一下
    Element root = sr.read(f).getRootElement();
    Iterator i = root.elementIterator();
    while(i.hasNext()){
        Element e = (Element) i.next();
        //一旦指定了Namespace，则使用XPath的时候必须带上
         //即便是默认的Namespace也一样，不过前面那个名字
         //可以尽可能写得短，编码的时候方便，比如改成a
        String title = e.selectSingleNode("atom:title").getText();
        System.out.println(title);
    }
}
```

### 创建一个根节点带有默认Namespace的XML

创建一个带有default namespace的XML的方法，相当的tricky，因为你创建一个Element的方法有很多种，可以通过add方法，默认的建，也可以使用DocumentHelper对象来创建，不过，每种方法给你的结果都不同，往往让你大吃一惊。其他的那些方法，和得到的多种结果，大家可以在网上看，很多。我就提供一个能创建“干净”的XML的代码范例。

```java
public void createXMLWithDefaultNamespace(List entries){
    Document d = DocumentHelper.createDocument();
    d.addElement("feed","http://www.w3.org/2005/Atom");
    Element root = d.getRootElement();
    //省略迭代entries代码
    root.addElement("title").add(DocumentHelper.createCDATA(title));
    root.addElement("id").add(DocumentHelper.createText(guid));
    root.addElement("category").add(DocumentHelper.createText(category));
    root.addElement("link").add(DocumentHelper.createText(permalink));
    root.addElement("updated").add(DocumentHelper.createText(updated));
}
```

最后，罗列一下上文中用到的所有对象所在的包，没有列出的在J2SE内。

```java
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.io.OutputFormat;
import org.dom4j.io.SAXReader;
import org.dom4j.io.XMLWriter;
```

### 参考文章

IBM Developer Works: [使用 dom4j 解析 XML—使用 domj4 API 创建与修改 XML 文档](http://www.ibm.com/developerworks/cn/xml/x-dom4j.html)

[dom4j官方网站](http://www.dom4j.org/)

[dom4j的javadoc文档](http://www.dom4j.org/dom4j-1.6.1/apidocs/)

[dom4j两种创建namespace的方法的差异! 07-11-30](http://zhangjiansheng.blogspot.com/2007/11/dom4jnamespace.html)

dom4j Cookbook