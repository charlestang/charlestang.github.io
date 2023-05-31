---
title: 【WordPress】【插件开发】在插件使用数据库存储数据
tags:
  - api
  - database
  - development
  - WordPress
id: '500'
categories:
  - - wp
    - Plugins Develop
  - - WordPress
date: 2012-08-17 22:33:41
---

开发WordPress插件，总是免不了要存储一些数据的。这些数据一般有两种类型，配置信息或者数据本身。配置信息一般可以用来定制插件运行时的一些参数，属于插件的属性。对于配置信息的存储，一般都是用WordPress Option API。WordPress自己就存储了很多博客运行时的自定义参数，这个接口也可以用来给插件存储自己的配置信息，其数据结构通用程度相当高，主要就是键值对（key-value）的形式。使用API `get_option`和`update_option`即可实现读写。具体用法和注意事项，本文不再展开，查看相关文档即可，下文基本关注另一个方面，就是如何存储纯数据。
<!-- more -->
## 什么样的情况下，不能使用Option API，而要直接使用底层DB

开发一款简单插件，改变WordPress的行为特征，这基本上很难用到底层DB，一般有配置信息足以。这种插件属于功能自定义类型的。另外有一种插件，是给WordPress添加一个其本身就不能具备的功能。比如，给WordPress增加网店的功能，你需要存储商品，价格，存量，销量，订单，甚至有账户，余额，充值，扣款，流水等等。等于是在WordPress上粘合了一个完整的网店系统，这就需要使用到DB来建立专用的表，不能把这种复杂的结构化数据都用键值对的形式存储。又比如，我给WordPress做了一个音乐播放器，用户需要存储播放器的外观、皮肤设定，存储数十上百的播放列表，每个播放列表里，还有数十上百的歌曲，这些不可以存储在键值对的数据结构里。

是否有替代的形式呢？我们说，当然有。比如，你可以使用文件，利用磁盘，存储是一种抽象，最底层是磁盘，最上层是数据结构，所以，你永远都可以选择更加底层，更加原始的抽象，只是要付出更大的代价，更高的插件复杂度，更长的开发时间。你可以不用键值对，向下，用DB，你可以不用DB，向下，用文件。

当然，现在你还有一种更好的选择，就是使用网络，也即向WordPress插件的用户，提供云端服务，云端服务有着无尽的好处。毋庸多言。体会不到的可以自己去领悟。当然，这意味更加高的要求，你不只是做一个简单的插件了，而是一种服务。维护成本也是最高的。

好不跑题了，我们现在就假设，你已经因为某种原因或者某种局限性，必须要提供一个standalone的版本，要在用户自己的WordPress安装实例中，建表来存储数据。

## WordPress建DB表的API

WordPress并没有正式开放关于DB建表的API，因为相关的函数没有添加任何文档，我不知道是因为开发者觉得这个函数的功能太过一目了然呢，还是压根就不想给众开发者去调用。不过呢，API本身相当稳定，从1.5开始起，就没有经历过重大的变化，而且，就该函数本身的思路来看，用在别的项目上，也是很好用工具。

```php

/**
 * {@internal Missing Short Description}}
 *
 * {@internal Missing Long Description}}
 *
 * @since 1.5.0
 *
 * @param unknown_type $queries
 * @param unknown_type $execute
 * @return unknown
 */
function dbDelta( $queries = '', $execute = true ) {

```

如上代码片段，就是用于DB建表的函数，我们看到，接受的参数是一个查询的语句或者数组。然后默认会直接执行查询。这个函数的内容实在是比较长，我就不在这里贴了。这里简要介绍一下这个API的功能。

函数的名字叫做dbDelta，Delta是一个希腊字母，学过高等数学的都会产生一个联想，Delta代表的是差异。这也很好地描述了这个函数的功能。这个函数会自动对比建表语句和现存数据库表的诧异，生成Alter Table语句，从而实现DB结构的升级。

函数首先将传入的建表语句分解成一个个的字段，然后从DB中查询同名表的结构，对比差异，生成Alter语句逐一执行。这样，提供给我们一个很好的能力，就是我们在建表的时候，只要写好Create Table语句，就可以完成任务，如果表结构有更新，没有必要自己写Alter Table语句，只需要改变Create Table语句即可。极大程度地简化了相关建表操作的开发难度，和降低了维护成本。

## 创建DB表的插件开发实例

为了更好地阐述DB建表API的功能，和用法，我特意设计了一个插件，这个插件专门用于教学用途，插件就需要使用到数据库表，所以，相关代码片段，正好可以用在这里做一个示范，希望能给大家一个参考。

插件的主要功能，是为WordPress博客生成索引，包含两部分，正排索引，和倒排索引。正排索引，就是按照文章，查询文章中的关键词，而倒排索引，正好反过来，按照关键词，查询包含该关键词的文章。其实，关键词的抽取是非常困难的，要实现中文关键词抽取，那就难上加难，所以，本插件不会涉及这个部分，而是把博客作者对于文章标注的分类和tag当成是文章的关键词，来创建正排索引和倒排索引。

先是正排索引，我们需要建一张表，包含如下这些字段，文章的ID，标题，摘要，作者ID，类型，然后就是关键词序列，用一个长字符串来存储关键词ID作为索引的内容。倒排索引，我们需要如下字段，关键词ID，关键词，slug，描述，被引用次数，含有该词的文章的ID列表。

于是，我们可以用如下的方法，来在插件中建表：

```php

class WCI {

    public static $db_version = '1.0';

    public static function init() {
        self::upgrade_database();
        
    }

    public static function upgrade_database() {
        global $wpdb, $table_prefix;
        /* @var $wpdb wpdb */

        $installed_version = get_option('wci_db_version');
        if ($installed_version != self::$db_version) {
            if (!empty($wpdb->charset))
                $charset_collate = "DEFAULT CHARACTER SET $wpdb->charset";
            if (!empty($wpdb->collate))
                $charset_collate .= " COLLATE $wpdb->collate";

            include ABSPATH . 'wp-admin/includes/upgrade.php';

            $sqls = array();

            $sqls[] = "CREATE TABLE {$table_prefix}wci_inverted_index (
                        term_taxonomy_id BIGINT( 20 ) NOT NULL ,
                        term_name VARCHAR( 200 ) DEFAULT NULL ,
                        term_slug VARCHAR( 200 ) DEFAULT NULL ,
                        description LONGTEXT,
                        count BIGINT( 20 ) NOT NULL DEFAULT '0',
                        object_ids TEXT,
                        PRIMARY KEY  (term_taxonomy_id)
                        ) {$charset_collate}";

            $sqls[] = "CREATE TABLE {$table_prefix}wci_index (
                        object_id BIGINT( 20 ) NOT NULL ,
                        object_title TEXT NULL ,
                        object_description TEXT NULL ,
                        object_author_id BIGINT( 20 ) NOT NULL ,
                        object_type VARCHAR( 20 ) NOT NULL ,
                        object_permalink VARCHAR( 1024 ) DEFAULT NULL ,
                        term_taxonomy_ids TEXT NULL ,
                        PRIMARY KEY  (object_id)
                        ) {$charset_collate}";

            dbDelta($sqls);
            update_option('wci_db_version', self::$db_version);
        }
    }
}

add_action('plugins_loaded', array('WCI','init'));

```

如上代码片段，将建表语句封装在了一个函数中。首先，读取一个预存的option值，专门记录db的版本，如果版本号码不存在，或者和当前插件中标称的db版本号不相复合，就dbDelta，将表结构更新到与新的建表语句一致。

这样的插件如果放出去到用户那一侧，如果之前装过老版本的用户，就会自动将db升级到新版，而全新安装的用户，就会在其DB中正确建立两张表。

注意点，经过测试发现，此脚本在3.5 alpha中的版本，不兼容backtick，就是数字1键左边那个像单引号的小点，然后最后声明索引的时候，KEY后面要跟两个空格，这应该是bug，所以，实际开发的时候时候，还是要针对不同WordPress的版本，反复测试兼容性才行。说不定以后问题修复了，这里说的注意点，反倒又成了错误的了。

## 结论

WordPress提供了一个简单并且强大的DB表结构维护的API，WordPress自己的十张表，都是用这个函数来维护的。如果插件开发需要用到DB表，那就调用此API创建。但是，希望各位读到此处的插件开发者，能够做到绿色低碳，在用户选择卸载插件的时候，询问用户是否完全清除数据的痕迹，不要让插件的用户谈DB色变。