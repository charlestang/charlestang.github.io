---
title: 【PHP】监视文件系统变化——inotify
tags:
  - file-system
  - inotify
  - PHP
  - usage
id: '505'
categories:
  - - something-about-daily-work
    - PHP
  - - 工作相关
date: 2012-09-04 00:56:01
---

监控文件系统的变化，不是一个常见的需求，但是随着对PHP使用的深入，不可避免的会碰到这类问题。我所在的公司，在服务器端，使用PHP进程常驻内存，来完成一些任务，甚至伺服服务。我们知道，PHP作为服务器动态语言，是不需要编译的，但是代码的生命周期是仅限于一次请求的，一次请求结束，下次请求，就会重新加载代码，除非安装了Opcode Cache，但是如果PHP常驻进程，这种自动加载更新代码的能力就失去了。这时候，我们有一种弥补方案，就是使用inotify。
<!-- more -->
inotify是系统体层提供的机制，在版本号大于2.6.13的内核中才有提供（之前kernel版本，有dnotify）。PHP官方扩展库[pecl提供了该扩展包](http://pecl.php.net/package/inotify "pecl扩展inotify主页")。关于inotify的基本原理和用法介绍，可以看[IBM的文档](http://www.ibm.com/developerworks/cn/linux/l-inotifynew/index.html "IBM提供的inotify的文档")。

inotify的API接口非常少，只有5个函数，inotify_init，inotifiy_read，inotify_add_watch，inotify_rm_watch，inotify_qeueue_len，这几个函数的含义还是相当直接的，估计比较难理解的，就只有一个init和read函数了。这里简单解释一下，inotify是一个类似队列一样的东西，把需要监控的一批文件和目录，加入到同一个inotify队列中，所以首先要先init一个空队列出来，然后用add_watch函数来添加监控对象。然后，read函数就能大显身手了，read函数可以产生一个（默认）阻塞的操作，查询监控的对象中是否有事件发生，如果有，就会返回数据，否则就一直阻塞。当然，也可以设置成非阻塞的，可以看相关代码范例。

inotify能够监控的文件系统事件罗列如下，基本上涵盖了linux server上的所有的文件事件。根据PHP官方文档和我实际测试，inotify不支持目录递归遍历，所以，如果要监控目录的变化，需要把每一个子目录都加入到watch的列表中去。除此之外，因为我在虚拟机上测试，还发现了一点，就是宿主机编辑共享文件，guest系统中的inotify无法监控到文件的变化。

```null

IN_ACCESS           :1
IN_MODIFY           :2
IN_ATTRIB           :4
IN_CLOSE_WRITE      :8
IN_CLOSE_NOWRITE    :16
IN_OPEN             :32
IN_MOVED_TO         :128
IN_MOVED_FROM       :64
IN_CREATE           :256
IN_DELETE           :512
IN_DELETE_SELF      :1024
IN_MOVE_SELF        :2048
IN_CLOSE            :24
IN_MOVE             :192
IN_ALL_EVENTS       :4095
IN_UNMOUNT          :8192
IN_Q_OVERFLOW       :16384
IN_IGNORED          :32768
IN_ISDIR            :1073741824
IN_ONLYDIR          :16777216
IN_DONT_FOLLOW      :33554432
IN_MASK_ADD         :536870912
IN_ONESHOT          :-2147483648

```

最后，简单写了一个小的目录监控的类，名字叫DirWatcher，就是目录监视器的意思，主要功能，就是可以向一个监视器实例注册监控目录和回调函数，从而实现一个文件系统事件触发动作的目的。特此奉上源代码，供诸君研究相关api的使用方法，也可用于自己的系统实现中。

 

```php


 */
class DirWatcher {

 private $_callbacks = array();
 private $_directories = array();
 private $_inotify = null;

 public function __construct() {
 $this->_inotify = inotify_init();
 }

 public function addDirectory($path, $mask = DIRWATCHER_CHANGED) {
 $key = md5($path);
 if (!isset($this->_directories[$key])) {
 $wd = inotify_add_watch($this->_inotify, $path, $mask);
 $this->_directories[$key] = array(
 'wd' => $wd,
 'path' => $path,
 'mask' => $mask,
 );
 }
 }

 public function removeDirectory($path) {
 $key = md5($path);
 if (isset($this->_directories[$key])) {
 $wd = $this->_directories[$key]['wd'];
 if (inotify_rm_watch($this->_inotify, $wd)) {
 unset($this->_directories[$key]);
 }
 }
 }

 public function addDirectories($directories) {
 foreach ($directories as $dir) {
 if (!is_array($dir)) {
 $this->addDirectory($dir);
 } else {
 $this->addDirectory($dir['path'], $dir['mask']);
 }
 }
 }

 public function addCallback($callback, $params = array(), $priority = 9) {
 $key = md5(var_export($callback, true));
 if (!isset($this->_callbacks[$key])) {
 $this->_callbacks[$key] = array(
 'callable' => $callback,
 'params' => $params,
 'priority' => $priority,
 );

 usort($this->_callbacks, create_function('$a, $b', 'return $a["priority"] > $b["priority"];'));
 }
 }

 public function removeCallback($callback) {
 $key = md5(var_export($callback, true));
 if (isset($this->_callbacks[$key])) {
 unset($this->_callbacks[$key]);
 }
 }

 public function addCallbacks($callbacks) {
 foreach ($callbacks as $callable) {
 if (is_callable($callable)) {
 $callable = array(
 'callable' => $callable,
 'params' => array(),
 'priority' => 9,
 );
 }

 $this->addCallback($callable['callable'], $callable['params'], $callable['priority']);
 }
 }

 public function startWatch() {
 while (TRUE) { //启动一个常驻进程，监视目录的变化，事件触发回调函数
 $event = inotify_read($this->_inotify);

 if (defined('DIRWATCHER_DEBUG') && DIRWATCHER_DEBUG) {
 error_log(vsprintf("[wd:%d][mask:%d][cookie:%s]%s", $event[0]));
 }

 foreach ($this->_callbacks as $callable) {
 call_user_func_array($callable['callable'], array_merge($event, $callable['params']));
 }
 }
 }

 public function stopWatch() {
 //没有实现，可以引入pcntl，优雅退出，退出前记得fclose($this->_inotify)
 }

}

```