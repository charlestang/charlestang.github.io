---
title: 插件开发全攻略（10）---在你的WordPress插件中使用Javascript和CSS
tags:
  - develop
  - plugins
  - translate
  - WordPress
id: '100'
categories:
  - [WordPress, Plugins Develop]
date: 2008-06-25 21:24:04
permalink: how-to-write-a-wp-plugin-10/
---

现今的许多插件对javascript和层叠样式表依赖更多了。将你插件中的javascript和css放置到分离的文件中是非常重要的，那样做会使插件维护起来更加容易。此系列中的这个部分将介绍怎样在你的插件中加载javascript和CSS文件。
<!-- more -->
### 添加你的javascript

你的插件可能需要装载prototype类库，或者一个自定义的脚本。这一节将向你展示几个WordPress函数，它们可以帮助你装载脚本，并且避免脚本冲突。

#### wp_register_script函数

**wp_register_script**函数允许你注册要调用的脚本，并且允许你设定先决条件。比如说，如果你的脚本需要prototype事先加载，那么你可以通过这个函数来指定。

这里是**wp_register_script**函数的参数：`wp_register_script($handle,$src,$deps=array(),$ver=false);`

*   **handle**是一个独一无二的名字，后面会用此名字引用你的脚本。这个参数是必须的。
*   **src**是你的javascript文件的绝对路径。这个参数是必须的。
*   **deps**是一个依赖数组。比如说，如果你的脚本需要使用prototype，你要把它罗列在这里。这个参数是可选的。
*   **ver**是一个字符串，标明了脚本的版本。这个变量是可选的。

举个例子，如果你有一个脚本要装载：_http://yourdomain.com/wp-content/plugins/your-plugin-directory/js/script.js_

让我们做一些假设：

*   你希望handle的名字为“my_script_handle”。
*   你的脚本依赖于prototype类库
*   你的版本是1.0

你将在你的插件代码初始化调用那个函数，或者在**wp_head** action之后调用：

```php

wp_register_script('my_script_handle','http://yourdomain.com/wp-content/plugins/your-plugin-directory/js/script.js', array('prototype'),'1.0');

```

#### wp_enqueue_script函数

**wp_enqueue_script**函数除了**src**参数是可选的以外，其他与**wp_register_script**是一样的。如果提供一个**src**，入队函数会_自动地注册_脚本，因此使用**wp_register_script**函数并不是必须的。然而，**wp_register_script**函数允许你手动注册你的脚本，这样，你可以仅使用一次**wp_enqueue_script**函数就将你所有的脚本装载。

如果我们像上一个例子中那样调用脚本，那么看起来像下面的样子：

```php

wp_enqueue_script('my_script_handle','http://yourdomain.com/wp-content/plugins/your-plugin-directory/js/script.js', array('prototype'),'1.0');

```

### 一个javascript的例子

对于Devlounge Plugin Series插件，我们将添加一个javascript文件，后面的文章中会用它。使用这个文件的目的，就是为了说明怎样使用**wp_enqueue_script**函数。

*   文件将会放下下列地址：http://yourdomain.com/wp-content/plugins/devlounge-plugin-series/js/devlounge-plugin-series.js
*   这个文件依赖于prototype
*   版本是1.0

你可能会回忆起，这个系列文章早期的一篇文章中，我们添加了一个action叫**wp_head**。那个action添加后，会调用一个函数，叫做**addHeaderCode**。让我们来修改这个函数，添加我们新的javascript：

```php

function addHeaderCode() {
            if (function_exists('wp_enqueue_script')) {
                wp_enqueue_script('devlounge_plugin_series', get_bloginfo('wpurl') . '/wp-content/plugins/devlounge-plugin-series/js/devlounge-plugin-series.js', array('prototype'), '0.1');
            }
            $devOptions = $this->getAdminOptions();
            if ($devOptions['show_header'] == "false") { return; }
```

            

上述代码的工作如下：


首先，检查wp_enqueue_script函数的存在性
然后调用该函数
我们使用 get_bloginfo('wpurl') 来得到WordPress安装根目录，然后手写路径中剩下的部分


加载层叠样式表

我已经往我的样式目录里面添加了一个新的样式表。这里是我们的一些前提：


这个文件存储在下列位置：http://yourdomain.com/wp-content/plugins/devlounge-plugin-series/css/devlounge-plugin-series.css
我在这个CSS文件中指定了一个ID叫做#devlounge-link
你已经添加了下面的代码 在文章的末尾：<a href="#" id="devlounge-link">取得博客留言的数量</a>


在样式表文件中，我已经添加了下面的ID：

```css
#devlounge-link{
background-color:#006;
color:#fff;
}
```


在插件中添加样式表，就和在addHeaderCode函数中添加一行代码一样简单：


```php
function addHeaderCode() {
            echo '' . "\n";
            if (function_exists('wp_enqueue_script')) {
                wp_enqueue_script('devlounge_plugin_series', get_bloginfo('wpurl') . '/wp-content/plugins/devlounge-plugin-series/js/devlounge-plugin-series.js', array('prototype'), '0.1');
            }
            $devOptions = $this->getAdminOptions();
            if ($devOptions['show_header'] == "false") { return; }

```
            

在第2行，我只是简单地打印出了新的样式表。