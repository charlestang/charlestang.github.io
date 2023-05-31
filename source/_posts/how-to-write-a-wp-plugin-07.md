---
title: 插件开发全攻略（07）---构造一个WordPress插件管理员面板
tags:
  - develop
  - plugins
  - translate
  - WordPress
id: '89'
categories:
  - - wp
    - Plugins Develop
  - - WordPress
date: 2008-06-06 16:26:49
---

任何需要用户输入（诸如改变一个变量）的插件，都需要某种管理面板。[建立一个管理面板](http://codex.wordpress.org/Adding_Administration_Menus)，并不是那么难的，所以，一个插件作者决定不创建管理面板，而是让用户自己去修改PHP代码的行为让我很是苦恼。让一个用户（TA的PHP知识可能是0）去修改代码通常来说不是一个好主意。本文将深入探讨成功地为你的插件创建管理面板，到底需要些什么。
<!-- more -->
[![](http://lh5.ggpht.com/TangChao.ZJU/SEvHTWZ83PI/AAAAAAAAAck/PV2Chbk0YdI/s800/admin-panel.gif)](http://picasaweb.google.com/TangChao.ZJU/Blog02/photo#5209476529229978866)

### 存储变量的地方

当你想要给你的插件创建一个管理面板的时候，你首先会碰到的问题之一就是到底在哪里存储变量值。非常幸运，WordPress通过options使得这件事变得非常容易。我将会在后续的系列文章中解释options和数据库存储。现在来说，所有你需要做的事情就是点点你的头，然后跟着我的指导，把你自己的管理变量存储到WordPress数据库中。

通常我考虑到options的时候做的第一件事情就是，给我的管理options取一个独特的名字。我把这个名字以成员变量的形式存储在我的类中。在这个Devlounge Plugin Series插件的例子中，我把这个变量声明添加到**DevloungePluginSeries**类中。

### 命名你的管理Options

```php

class DevloungePluginSeries {
var $adminOptionsName = "DevloungePluginSeriesAdminOptions";
function DevloungePluginSeries() { //constructor
}

```

  

第2行显示了我存储我的成员变量的地方。我将我的变量命名为**adminOptionsName**并且给予它一个很长而且独特的值**DevloungePluginSeriesAdminOptions**。

### 给你的管理Options设定缺省值

你需要一个地方来初始化你的管理选项，尤其是当一个用户第一次激活你的插件的时候。然而，你还必须保证这些options在升级中是安全的，以防万一你决定将来添加更多的options。我使用的技巧是，提供一个专门的函数来调用你的管理options。你的插件的需求可能不一样，但是绝大多数的管理面板不会难以置信地复杂，所以一个函数对你的管理options来说，已经足够了。

下面这个函数是我插入到类DevloungePluginSeries中的：

```php

//Returns an array of admin options
function getAdminOptions() {
$devloungeAdminOptions = array('show_header' => 'true',
'add_content' => 'true',
'comment_author' => 'true',
'content' => '');
$devOptions = get_option($this->adminOptionsName);
if (!empty($devOptions)) {
foreach ($devOptions as $key => $option)
$devloungeAdminOptions[$key] = $option;
}
update_option($this->adminOptionsName, $devloungeAdminOptions);
return $devloungeAdminOptions;
}

```

这个函数做的事情是：

*   给你的管理options赋默认值（3-6行）
*   尝试从数据库中找出以前存储过的值（第7行）
*   如果options曾经存储过，那么存储的值会覆盖默认值（8-11行）
*   options被存储到WordPress数据库中（第12行）
*   options被返回供你使用（第13行）

### 初始化管理Options

getAdminOptions函数可以在任何时候调用来获得管理options。然而，当插件第一次安装的时候呢？应该有某个函数被调用也能获得管理options。我在DevloungePluginSeries类中添加了这个函数：

```php

function init() {
$this->getAdminOptions();
}

```

  

短小简单。但是必须有一个action来调用这个函数。

```php

add_action('activate_devlounge-plugin-series/devlounge-plugin-series.php',  array(&$dl_pluginSeries, 'init'));

```

这个action有些复杂，但是很容易理清楚。下面是这个action做的事情：

*   当一个插件被激活的时候你告诉它运行
*   你给它主要的插件PHP文件，就是devlounge-plugin-series/devlounge-plugin-series.php。这当然是假设你把插件放到了wp-content/plugins/目录中。
*   你传递了一个引用给实例变量dl_pluginSeries并且调用了init函数。

所以，任何时候插件被激活，init函数都会被调用。

### 管理面板怎样工作

在我深入到创建实际的管理面板的代码的时候，描述一下管理面板的行为是有好处的。这里有一些你设定你管理面板的步骤：

*   检查任何表单数据是否已经被提交。
*   如果表单数据存在，输出提醒。
*   显示管理面板Options。

在管理面板中，一个非常困扰你的问题可能是_e的使用。_e函数允许WordPress搜索你文本的本地化版本。这将帮助WordPress在将来翻译你的插件。这个函数的工作类似一个普通的echo，但是你传给它的是你的文本和一个标识变量（典型的是你的插件名称）。一个例子：

`_e('Update Settings','DevloungePluginSeries');`

这句代码和：

`echo "Update Settings";`

是相同的。

### 设置你的管理面板函数

我们想要做的第一件事情就是设定一个函数，来真正地打印出一个管理面板。函数名字叫做printAdminPage。下一段代码将要读入我们早先设定的options并且检查是否所有的发布options已经被提交。这一段的所有代码假设写在printAdminPage函数中。

```php

//Prints out the admin page
function printAdminPage() {
$devOptions = $this->getAdminOptions();
if (isset($_POST['update_devloungePluginSeriesSettings'])) {
if (isset($_POST['devloungeHeader'])) {
$devOptions['show_header'] = $_POST['devloungeHeader'];
}
if (isset($_POST['devloungeAddContent'])) {
$devOptions['add_content'] = $_POST['devloungeAddContent'];
}
if (isset($_POST['devloungeAuthor'])) {
$devOptions['comment_author'] = $_POST['devloungeAuthor'];
}
if (isset($_POST['devloungeContent'])) {
$devOptions['content'] = apply_filters('content_save_pre', $_POST['devloungeContent']);
}
update_option($this->adminOptionsName, $devOptions);
?>



```

 

上面所有代码做的是装载options并且测试是否表单的每个部分都已经被正确提交。if语句并不是必须的，但是有的时候对于调试来说很有用。第一被测试的表单变量是update_devloungePluginSeriesSettings。这个变量被赋值给我们的“提交”按钮。如果它没有被设定，那么说明这个表单没有被提交。

就像说好的一样，在第16行，我使用了apply_filters函数来格式化内容，以便存入数据库。

下一段代码将会显示一个HTML表单，那是管理面板所必须的。它有一些复杂，所以我会这里概括一下。所有的代码做的事情，就是显示表单元素和读入options。

```php


">
Devlounge Plugin Series
Content to Add to the End of a Post
<?php _e(apply_filters('format_to_edit',$devOptions['content']), 'DevloungePluginSeries') ?>
Allow Comment Code in the Header?
Selecting "No" will disable the comment code inserted in the header.
 /> Yes /> No
Allow Content Added to the End of a Post?
Selecting "No" will disable the content from being added into the end of a post.
 /> Yes /> No
Allow Comment Authors to be Uppercase?
Selecting "No" will leave the comment authors alone.
 /> Yes /> No





需要在上述代码中观察的是options的引用，和HTML和PHP是怎样集成的。设置管理面板Action现在，printAdminPage函数已经添加了，我们需要通过一个action调用它。首先函数必须被设定在正好在action的上面，在类的范围之外。

//Initialize the admin panel
if (!function_exists("DevloungePluginSeries_ap")) {
function DevloungePluginSeries_ap() {
global $dl_pluginSeries;
if (!isset($dl_pluginSeries)) {
return;
}
if (function_exists('add_options_page')) {
add_options_page('Devlounge Plugin Series', 'Devlounge Plugin Series', 9, basename(__FILE__), array(&$dl_pluginSeries, 'printAdminPage'));
}
}
}

 上面的代码做了下面这些事：创建了一个叫做DevloungePluginSeries_ap的函数。测试变量dl_pluginSeries是否存在（4-7行）。这个变量是我们的类的引用。一个叫做“Devlounge Plugin Series”的管理页面被初始化了，并且，我们的printAdminPage函数被引用了。（8-10行）。add_options_page函数的调用方法为：add_options_page(page_title,menu_title,access_level/capability,file,[function]);访问级别（在这个例子中是9）在WordPress Codex的Users Levels page页面有详细的描述。必须设置一个action来调用DevloungePluginSeries_ap函数：

add_action('admin_menu', 'DevloungePluginSeries_ap');

```