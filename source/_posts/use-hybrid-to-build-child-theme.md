---
title: 使用Hybrid框架的起点
tags:
  - develop
  - framework
  - hybrid
  - themes
  - WordPress
id: '298'
categories:
  - - WordPress
date: 2009-02-18 23:16:07
---

在上一篇《[Hybrid主题框架综述](http://sexywp.com/introduction-to-hybrid.htm)》中，我们已经介绍了Hybrid的基本原理。这篇文章，我们将主要介绍如何使用Hybrid来制作一款主题。本文主要面向的读者为主题制作爱好者，和狂热的DIY fans们。
<!-- more -->
子主题，就是指，以另一个已经存在的主题的页面元素结构和功能为基础，创建完全自定义的样式，和附加功能。而在制作过程中，完全不修改另一个主题的代码。而“另一个主题”在这个过程中，就自动成为了“父主题”。

```php
/*   
Theme Name: Rose
Theme URI: the-theme's-homepage
Description: a-brief-description
Author: your-name
Author URI: your-URI
Template: use-this-to-define-a-parent-theme--optional
Version: a-number--optional
.
General comments/License Statement if any.
.
*/
```

上面一段代码，我想每个主题制作爱好者都不会陌生，这是存在于style.css头部的一段注释，WordPress使用这段信息，加载一个主题。其中的Template，就是在制作子主题的时候用于说明父主题的字段。具体在制作一款子主题的时候，只要将Template:hybrid填写到style.css的头部，就可以使用Hybrid作为父级主题了。当然，这个说明同样也适用于其他主题框架，或者任何一款主题（不推荐使用普通主题作为父级主题）。

创建子主题，就相当于站在巨人的肩膀上，你要处理的文件数量非常少，一般来说只有两个就够了，一个是style.css，另一个是functions.php。style.css的作用是用于说明子主题的外观样式，而functions.php的作用，是用于附加原来父级主题所没有的功能。

这里要做一个**特别说明**，就是关于**文件加载的顺序**的说明。如果你制作了一款子主题，那么WordPress在加载的时候，**首先加载的是子主题的functions.php然后才是父级主题的functions.php**。这意味着什么呢？在Hybrid的functions.php里，使用add_action函数挂载了非常多的东西，根据Hybrid主题框架综述的说明，几乎所有的页面内容，都通过action来挂载。那么如果有哪部分内容，你不想要，或者你想替换成你自己的，那么你是无法直接在子主题的functions.php里面实现卸载的。你能直接操作的，只是挂载，而不能卸载。那么非要卸载是不是没有可能了呢？也不是。这里给出一个方法，首先，创建一个函数，action_to_remove，然后在函数体内写好你要卸载的action，然后将这个函数hook到全局的action **init** 之上，就可以实现卸载了。代码如下：[（什么是Hook？什么是Action？）](http://sexywp.com/try-to-explain-hook-in-wp.htm)

```php
add_action('init','action_to_remove');  function action_to_remove(){    remove_action('hybrid_header','hybrid_site_title');  }
```

通过上述代码，我们移除了Hybrid主题中的title部分。其实，这个问题也有其一般意义，因为当你想要移除一个action的时候，这个action根本还没有被add过，那么你的移除动作是无效的。以后如果有必要，我会专门撰文介绍这个问题。

上面两段，对于插件开发爱好者来说，可能非常容易理解。一般同学如果不理解，没关系，直接跳过就ok了，毕竟Hybrid没有往主题里挂过多的不必要的东西，一般情况不需要移除任何东西的。

这里总结一下，创建子主题的过程：

1.  在wp-content的themes文件夹下，创建一个文件夹，用作子主题的目录，如my-custom-hybrid。

2.  在my-custom-hybrid目录里，创建两个文件，一个是style.css，一个是functions.php（可以不要这个文件）。

3.  编辑style.css文件，在头部按照上文的格式，撰写注释信息，在Template后面，填上hybrid。

4.  在style.css文件内部，使用CSS语法，创建你自己的样式。

5.  在functions.php内部，添加一些功能，或者嵌入某些插件。

到这里，如果你真的看明白了，想要动手制作了，那么我还要再推荐给你一个非常好的东西。制作一款子主题，并非必须从0开始，也即从一个空白的style.css开始。Hybrid的作者非常贴心的创建了一个子主题skeleton，就是为了给广大主题爱好者创建一个良好的基础。该子主题的style.css文件，按照页面元素的层次结构和出现顺序，罗列了所有的class名称和id名称，比如，导航条部分的代码样子如下：

/**
  
* Page navigation

  
************************************************/

/* Wrapper for navigation */
  
#navigation {}

    /* Page nav */
  
    #page-nav {}

  
        #page-nav ul {}

  
            #page-nav li {}

  
                #page-nav li a {}

  
            #page-nav li.current_page_item {}

瞧见没有？是不是结构非常的鲜明，一目了然呢？[下载地址](http://themehybrid.com/themes/hybrid)。

好了，今天就介绍到这里吧，下次，将要撰写《Hybrid资源一览表》，欢迎大家继续关注！