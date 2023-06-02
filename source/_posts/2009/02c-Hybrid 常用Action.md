---
title: Hybrid 常用Action
tags:
  - develop
  - framework
  - hybrid
  - reference
  - themes
  - WordPress
id: '309'
categories:
  - WordPress
date: 2009-02-26 00:08:20
permalink: hybrid-references/
---


<!-- more -->
### Home页面流程图

1.  [hybrid_head()](#hybrid_head)
2.  wp_haed()
3.  body
4.  hybrid_before_html()—action，默认没有被hook
5.  div#body-container
6.  hybrid_before_header()—action，默认没有被hook
7.  div#header-container
8.  div#header
9.  [hybrid_header()](#hybrid_header)
10.  end#header
11.  end#header-container
12.  [hybrid_after_header()](#hybrid_after_header)
13.  div#container
14.  hybrid_before_container()—action，默认没有被hook
15.  div#content
16.  [hybrid_before_content()](hybrid_before_content)
17.  /*wp loop begin*/
18.  div.hybrid_post_class()
19.  h2.post-title inline
20.  p.byline inline
21.  div.entry-content inline
22.  p.entry-meta inline
23.  end.hybrid_post_class()
24.  /*end wp loop*/
25.  [hybrid_after_content()](#hybrid_after_content)
26.  end#content
27.  [hybrid_after_container()](#hybrid_after_container)
28.  end#container
29.  div#footer-container
30.  [hybrid_before_footer()](#hybrid_before_footer)
31.  div#footer
32.  [hybrid_footer()](#hybrid_footer)
33.  wp_footer()
34.  end#footer
35.  hybrid_after_footer()—action，默认没有被hook
36.  end#footer-container
37.  end#body-container
38.  /body

#### hook到hybrid_head()的函数列表

1.  hybrid_meta_content_type()
2.  hybrid_meta_robots()
3.  hybrid_meta_author()
4.  hybrid_meta_copyright()
5.  hybrid_meta_revised()
6.  hybrid_meta_abstract()
7.  hybrid_meta_description()
8.  hybrid_meta_keywords()
9.  hybrid_meta_template()
10.  wp_generator()
11.  hybrid_favicon()
12.  hybrid_head_feeds()
13.  hybrid_head_pingback()
14.  hybrid_head_breadcrumb()

#### hook到hybrid_header()的函数列表

1.  hybrid_site_title() —提供同名filter，参数为标题包括其html tag，没有被hook
2.  hybrid_site_description() —提供同名filter，参数为站点描述，包括其html tag，没有被hook

#### hook到hybrid_after_header()的函数列表

1.  [hybrid_page_nav()](#hybrid_page_nav) —启动两个action，并提供一个同名filter，参数为导航条包括其html tag，没有被hook

#### hook到hybrid_before_content()的函数列表

1.  hybrid_breadcrumb() —提供一个同名filter和一个名为hybrid_breadcrumb_args的filter
2.  hybrid_get_utility_before_content() —该函数打印位于Content之前的Sidebar，在Hybrid中被赋予一个名称为Utility

#### hook到hybrid_after_content()的函数列表

1.  hybrid_get_utility_after_content() —该函数打印位于Content之后的Sidebar
2.  hybrid_navigation_links() —该函数打印WP自带的简单页面导航Prev和Next

#### hook到hybrid_after_container()的函数列表

1.  [hybrid_get_primary()](#hybrid_get_primary) —该函数首先提供一个filter，名为hybrid_primary_var，参数sidebar_id，如果传入false可以关闭侧边栏，该函数打印主侧边栏，并在此之前和之后分别触发一个action
2.  [hybrid_get_secondary()](#hybrid_get_primary) —原理基本上和上一个相同，提供的filter名字为hybrid_secondary_var
3.  hybrid_insert() —提供一个同名filter，参数为要打印出来的内容，默认为false，这是专门给用户用来添加sidebar的hook

#### hook到hybrid_before_footer()的函数列表

1.  [hybrid_get_subsidiary()](#hybrid_get_primary) —其功能等同于侧边栏，同上面两个侧边栏

#### hook到hybrid_footer()的函数列表

1.  hybrid_copyright() —打印版权信息，提供同名filter
2.  hybrid_credit() —与上面一个类似，也提供同名filter
3.  hybrid_query_counter() —打印页面生成时间和数据库查询数的函数

#### 由hybrid_page_nav()触发的action

1.  hybrid_before_page_nav() —action，默认没有被hook
2.  hybrid_after_page_nav() —action，默认没有被hook

#### 由hybrid_get_primary()和hybrid_get_secondary()和hybrid_get_subsidiary() 触发的action

1.  hybrid_before_primary() —action，默认没有被hook
2.  hybrid_after_primary() —action，默认没有被hook
3.  hybrid_before_secondary() —action，默认没有被hook
4.  hybrid_after_secondary() —action，默认没有被hook
5.  hybrid_before_subsidiary() —action，默认没有被hook
6.  hybrid_after_subsidiary() —action，默认没有被hook