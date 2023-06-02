---
title: 使用 Python 自动将数据库备份到 Dropbox 的脚本
tags:
  - Dropbox
  - python
  - usage
id: '766'
categories:
  - [工作相关, 心得体会]
date: 2017-02-06 00:32:32
permalink: use-python-to-backup-database-to-dropbox/
---

最近，正好发生了一件大事，就是 GitLab 的运维同学不小心删除了生产的数据，虽然 GitLab 已经骇人听闻的准备了五种备份机制，但是，仍然导致他们丢失了将近 6 个小时的用户数据，尤其对他们声誉的损失，是根本无法估量的。反思一下，这个博客 Becomin' Charles，也是没有完善的备份的，真是冷汗直冒啊，主要考虑到这是我的个人博客，但是想想已经坚持了快十年了，如果真的丢了的话，还是非常痛心的。
<!-- more -->
正好，老婆最近正在学习 Python 编程，我在教她，其实，我是 PHP 程序员，一点也不喜欢 Python，但是说实在，一个外行学编程的话，Python 确实比 PHP 友好太多了，只能推荐她学 Python 了。正好，借着这个机会，我决定自己也学学 Python 编程吧，于是，我决定要用 Python 做一个数据库的自动备份脚本。备份的位置，就用 Dropbox 来做吧，因为我的服务器是 Linode 提供的，美国 fremont 机房，选择美国的存储服务，比较合适。以下是我写得代码，Python 小白，敬请指教：

```python
#!/usr/bin/python
#coding:utf-8

import sys
import os
from yaml import load
from datetime import datetime
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

if len(sys.argv) < 2:
    print >>sys.stderr, "Usage: %s <config_file>" % sys.argv[0]
    sys.exit(0)

conf = load(file(sys.argv[1], 'r'))

# config file is a YAML looks like
# ---
# server-name: 127.0.0.1
# local-backup-path: /tmp
# remote-backup-path: /backup
# dropbox-token: jdkgjdkjg
# databases:
#   - host:    localhost
#     port:    3306
#     user:    user
#     pass:    password
#     name:    database1
#     charset: utf8
#   - host:    localhost
#     port:    3306
#     user:    user2
#     pass:    password2
#     name:    database2
#     charset: utf8

for db in conf['databases'] :
    filename = "%s_%s.sql" % (db['name'], datetime.now().strftime("%Y%m%d-%H-%M-%S")) 
    filepath = "%s/%s" % (conf['local-backup-path'], filename)
    cmd = "mysqldump -h%s -u%s -p%s -P%s --single-transaction %s > %s" % (
            db['host'],
            db['user'], 
            db['pass'], 
            db['port'], 
            db['name'], 
            filepath
            )
    os.system(cmd)
    cmd = "gzip %s" % filepath
    os.system(cmd)
    filepath = filepath + '.gz'
    dbx = dropbox.Dropbox(conf['dropbox-token'])
    backuppath = "%s/%s/%s/%s" % (
            conf['remote-backup-path'],        # remote path
            datetime.now().strftime("%Y%m%d"), # date string
            conf['server-name'],               # server name
            filename + '.gz')
    with open(filepath, 'rb') as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        print(time + "Uploading " + filepath + " to Dropbox as " + backuppath)
        try:
            dbx.files_upload(f.read(), backuppath, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
```

简单描述下这个代码的思路，这个程序应该满足这个几个要求：

*   使用 mysqldump 备份数据库到本地
*   应该支持配置文件，允许配置多个数据库
*   可以上传到 Dropbox

为了完成这些要求，首先碰到的难题是怎么支持配置文件，一搜，原来 Python 下有个默认的 ConfigParser，可以完成这个任务，但是正常东西比较恶心的是，配置文件必须是以 [Section] 为单位组织的。其实我的配置显然有些全局配置，还有就是数据库的各种信息是多次重复的，这种配置文件，嵌套能力简直糟糕，必须两层的结构，就很恶心。于是我去网上搜配置文件的格式，好多文章比较了各种配置文件的优劣，其实这文章挺多的，我想了想，以后或许我也可以写文章讲讲我自己的感受了。反正就是很多文章最后都公认 YAML 是配置文件里最完美的。于是我也决定用这个，果然也有现成的类库，就是 PyYAML，特方便，就俩函数 load 和 dump，直接就把文件变成 dict 格式了。

第二个难题，就是上传 Dropbox，后来发现，官方提供了很丰富的 API，而且直接就有 SDK，（让我眼红的是，官方竟然没有 PHP 的 SDK，这么不受待见么？），研究 SDK 用法，发现直接就有代码范例，于是直接抄到我的代码里，瞬间完成了 50% 的代码，爽！

整个代码完成后，我发现，写代码一共也没花多少时间，而且，我学会的 Python 的方式，我以前一直抱怨 Python 的文档难用，我发现，其实，最好的方式其实是在交互式的 Shell 里，用 help 来查询 API，再辅佐以官方文档，才是比较正确的方式。这是刷新了一个我以前的认识的地方。实践下来感觉还不错的。Python 的包管理器 pip 也很好用。

```shell
pip install PyYAML
pip install dropbox
```

以上代码我已经提交到了[我的 GitHub](https://github.com/charlestang)，如果大家感兴趣，可以使用[这个连接来 tracking](https://github.com/charlestang/env/blob/master/scripts/db_backup/backup.py)，也可以在这里留言和我讨论。

Update：2023-05-29

执行这个代码，需要数据库的用户拥有 Reload 或者 Flush_tables 权限。这两个权限是 Mysql Global 级别的权限，使用下面的语句赋权：

`grant reload, flush_tables on *.* to user@localhost;`

注意里面 `*.*` 不要写错了，global 级的权限，只能用这个才能赋权成功。