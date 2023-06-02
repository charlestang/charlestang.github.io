---
title: Mac OS X上如何实现到Linux主机的ssh免登陆
tags:
  - DIY
  - Linux
  - ssh
  - tips
  - usage
id: '458'
categories:
  - [工作相关, Linux]
date: 2011-09-04 11:53:53
permalink: mac-os-x-ssh-key-pair-login-linux/
---

本文要讲的，就是如何简化从Mac登录Linux主机的操作步骤，提高效率。所谓的“免登陆”其实是不存在的，只是说，从验证密码的登录方式，改为公私钥对的登录验证方式。使用后者的方式，每次会由ssh客户端自动发送验证信息，所以就免去了人工输入密码，看起来好像“免登陆”一样。

关于这么做的原理，大家可以自己去Google，关键词是“非对称加密”，“RSA算法”，“基于ssh密钥对的自动登录”，等等，我就不多解释了。我直接说操作步骤吧：

1.  生成密钥对
2.  用密码登录远程主机，将公钥拷贝过去
3.  done

怎么样，无敌简单吧？

## 生成密钥对

执行命令 ssh-keygen -t rsa
执行结果如下：

> charles@mac:~ > ssh-keygen -t rsa
> Generating public/private rsa key pair.
> Enter file in which to save the key (/Users/charles/.ssh/id_rsa): 
> Created directory '/Users/charles/.ssh'.
> Enter passphrase (empty for no passphrase): 
> Enter same passphrase again: 
> Your identification has been saved in /Users/charles/.ssh/id_rsa.
> Your public key has been saved in /Users/charles/.ssh/id_rsa.pub.
> The key fingerprint is:
> c8:4b:85:87:90:7c:1a:67:b6:71:f5:51:0c:9d:a2:89 charles@TCMBP.local
> The key's randomart image is:
> +--[ RSA 2048]----+
>  ... .. o=.. 
>  +.*o. ...+ 
>  Bo+o. o.. 
>  ...+E o 
>  + S 
>  . . 
>  . 
>  
>  
> +-----------------+

注意：提示enter passphrase的时候，不要输入，因为你本来就想少打一次密码的，这里如果设置了用密码保护私钥，那登录的时候还是要输密码，就白做了。

做完这个步骤后，cd ~/.ssh，你就可以看到你刚才生成的密钥对，id_rsa是私钥，id_rsa.pub是公钥。下一步，就是把公钥拷贝到目标主机上。

## 将公钥拷贝到目标主机

用ssh登录到目标主机，然后cd ~/.ssh目录，如果目录不存在，那么要自己创建mkdir -p ~/.ssh。你今后要用哪个帐户登录主机，就在哪个帐户的home目录下操作，如果要免登陆root，就要去/root下操作。使用~比较好，不用多想了。

有了.ssh目录后，进去，然后把id_rsa.pub传过去，可以用scp命令，这里要做的一个主要操作，就是将id_rsa.pub，的文件内容，写到一个叫authorized_keys的文件中去，如果目标主机的相应用户名下已经有了.ssh目录和authorized_keys文件，那你操作要小心一点，可能别人也做过免登陆的设置，这个时候你要小心不要把别人的设置给覆盖了。如果没有的话，就创建文件touch ~/.ssh/authorized_keys，然后执行cat id_rsa.pub >> authorized_keys，将你的公钥写入到authorized_keys中，公钥文件.pub里面只有一行信息，上面的命令相当于把那一行信息追加到authorized_keys文件最后一行。

如果.ssh目录是你主机刚刚创建的，那么可能还需要改变一下这个目录的权限，将权限放低，chmod -R 0600 ~/.ssh，到此，所有设置就算做完了，你可以退出登录，在自己的主机上试一下了，现在再敲入ssh命令后，不用密码就可以登录主机了。