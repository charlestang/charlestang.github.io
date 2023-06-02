---
title: 插件开发全攻略（08）---构建一个WordPress插件用户面板
tags:
  - develop
  - plugins
  - translate
  - WordPress
id: '98'
categories:
  - [WordPress, Plugins Develop]
date: 2008-06-22 18:16:20
permalink: how-to-write-a-wp-plugin-08/
---

将会有这么一种情况，你将有一个主要的管理面板，但是希望能够让独立的用户设定他们自己的偏好。在Devlounge Plugin Series这个例子中，我们添加了一个是否把文字添加到文章末尾的选项。然而，假如一个登录用户不希望看到这段文字呢？为什么不给他们一个选择，而且不影响到所有其他的用户呢？
<!-- more -->
这篇文章将会涉及到这个问题，让你可以添加你自己的用户面板。

![](http://lh5.ggpht.com/TangChao.ZJU/SF4i2dd9kRI/AAAAAAAAAdE/ZJZK2Lt6P-M/s800/users-panel.gif)

### 命名你的选项

```php

class DevloungePluginSeries {
var $adminOptionsName = "DevloungePluginSeriesAdminOptions";
var $adminUsersName = "DevloungePluginSeriesAdminUsersOptions";

```

第3行显示，我添加了一个成员函数，叫做**adminUsersName**。我给这个变量取了一个长而且独特的名字**DevloungePluginSeriesAdminUsersOptions**。

### 设定你的缺省用户选项

你将需要一个地方来初始化你的选项，尤其是当一个用户第一次激活了你的插件的时候。然而，这些选项在管理面板之外也应该起作用，不论用户是登录了还是没有登录。

这里是一个我引入到**DevloungePluginSeries**类中的函数：

```php

//Returns an array of user options
function getUserOptions() {
global $user_email;
if (empty($user_email)) {
get_currentuserinfo();
}
if (empty($user_email)) { return ''; }
$devOptions = get_option($this->adminUsersName);
if (!isset($devOptions)) {
$devOptions = array();
}
if (empty($devOptions[$user_email])) {
$devOptions[$user_email] = 'true,true';
update_option($this->adminUsersName, $devOptions);
}
return $devOptions;
}

```

这个函数完成以下任务：

*   检查用户是否已经登陆（3-7行）。这个检查仅需要查看变量user_email是否设定即可。
*   尝试找到以前存储在数据库中的选项（第8行）。
*   如果没有找到option，设定默认值（第9-15行）。
*   返回option供你使用

### 初始化管理用户option

可以在任何时候调用getUserOptions来取得用户管理options。然而，那么插件第一次安装的时候呢？应该有某种函数被调用，以取得用户选项。我添加了下面这个函数到init函数:

```php

function init() {
$this->getAdminOptions();
$this->getUserOptions();
}

```

第3行调用了新函数getUserOptions。由于已经有了一个action调用了init函数，不需要额外的步骤了。

### 怎样使管理面板和用户面板一起工作

你会回想起上一篇关于[设定一个管理面板](http://sexywp.com/how-to-write-a-wp-plugin-07.htm)的文章中，WordPress管理员可以设定文章末尾的内容，代码是否是否在头部显示，评论中的作者名字是否大写。而用户面板允许那些不是管理员的用户有能力设定他们是否希望这些options。

我们将允许用户决定，如果他们：

*   想要内容在文章的末尾显示（仅当管理员启用了这个option）
*   想要评论作者的名字大写（仅当管理员启用了这个option）

### 设定用户面板函数

我们要做的第一件事情就是编写一个函数来显示用户面板。函数名字为printAdminUsersPage。下一段代码将会读入我们早先设定的options并且检查一下是否有任何文章选项已经被提交。这一节中所有的代码都默认包含于printAdminUsersPage函数。

```php

//Prints out the admin page
function printAdminUsersPage() {
global $user_email;
if (empty($user_email)) {
get_currentuserinfo();
}
$devOptions = $this->getUserOptions();
//Save the updated options to the database
if (isset($_POST['update_devloungePluginSeriesSettings']) && isset($_POST['devloungeAddContent']) && isset($_POST['devloungeAuthor'])) {
if (isset($user_email)) {
$devOptions[$user_email] = $_POST['devloungeAddContent'] . "," . $_POST['devloungeAuthor'];
?>
Settings successfully updated.
adminUsersName, $devOptions);
}
}
//Get the author options
$devOptions = $devOptions[$user_email];
$devOptions = explode(",", $devOptions);
if (sizeof($devOptions)>= 2) {
$content = $devOptions[0];
$author = $devOptions[1];
}
?>

```

上述代码：

*   取回用户options（第7行）
*   存储发送的数据到数据库（第9-18行）
*   为用户读入用逗号分隔的变量

下一段代码将会显示用户面板必须的HTML表单。所有的代码做的事情就是显示表单元素，并且读入已经取得的选项。

```txt
Devlounge Plugin Series User Options
Allow Content Added to the End of a Post?
Selecting "No" will disable the content from being added into the end of a post.
 /> Yes /> No
Allow Comment Authors to be Uppercase?
Selecting "No" will leave the comment authors alone.
 /> Yes /> No

```


设定用户面板Action

当设定管理面板的时候，我们定义了一个函数叫做DevloungePluginSeries_ap，以帮助初始化管理面板。我们现在将要再次求助于此函数来添加我们的用户面板。


```php
//Initialize the admin and users panel
if (!function_exists("DevloungePluginSeries_ap")) {
function DevloungePluginSeries_ap() {
global $dl_pluginSeries;
if (!isset($dl_pluginSeries)) {
return;
}
if (function_exists('add_options_page')) {
add_options_page('Devlounge Plugin Series', 'Devlounge Plugin Series', 9, basename(__FILE__), array(&$dl_pluginSeries, 'printAdminPage'));
}
if (function_exists('add_submenu_page')) {
add_submenu_page('profile.php', "Devlounge Plugin Series User Options","Devlounge Plugin Series User Options", 0, basename(__FILE__), array(&$dl_pluginSeries, 'printAdminUsersPage'));
}
}
}
```


在第12行，你能看到一行代码：

往profile.php页面中添加了一个子菜单
让一个用户级别高于或者等于0的用户访问用户面板
调用我们的printAdminUsersPage函数


关于访问级别的（此例中为0）更详细的描述，可以参考用户级别。