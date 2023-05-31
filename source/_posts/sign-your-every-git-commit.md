---
title: 签名你的每个 Git Commit
tags:
  - code
  - git
  - GitHub
  - vcs
id: '886'
categories:
  - - 小窍门
  - - 工作相关
date: 2020-03-01 17:11:34
---

![](https://sexywp.com/wp-content/uploads/2020/03/commit_verify_screenshot-1024x464.png)

好久没有写代码提交 GitHub 了，真是惭愧！回到正题，今天提交了一个代码，冷不丁发现，在我的 Commit 记录里面，有一条被打上了 Verified 标记。原来 GitHub 的 Commit 支持签名验证了，我可以对每一个我的 Commit 进行签名（Commit Signature），这样，GitHub 的其他用户就知道这个“提交”来自一个可以信任的来源。我举个例子，如果有人设定了我的头像，我的名字，往我的版本库里 Push 了一个 Commit（我的 WordPress 插件官方仓库，被黑客提交过恶意代码，因为我不小心被钓鱼了，自爆一下黑历史），那么，有没有 Verified 就成为一个识别真伪的依据（虽然，我位微言轻，可能不太会有人假冒我，我也知道，杠头请退散）。

## 给每个 Commit 签名

作为个人开发者，给自己的每个 Commit 签名，可能有点多此一举（或许会有这么想的人），但是在一个多人合作开发的项目里，管理员可以要求所有的项目成员，都必须签名自己的 Commit，不接受未经签名的 PR，那就产生了一定的意义（虽然是什么意义我还没想得太明白）。

上面图里个 Verified 标记，是 GitHub 自动给打上的，因为一个项目的第一个 Commit 是在我生成项目的时候，由 GitHub 的 Web 站点自动提交的，是项目的初始化 Commit。这种情况由 GitHub 方面利用你在网站可信的登录态进行签名。但是我们知道，这是一个分布式版本控制，一般来说，Commit 都是在本地完成的，然后 Push 到云端，所以，要想让每个 Commit 都能够带有签名验证，需要在本地部署签名的过程。怎么做呢？

## 在 GitHub 验证一个邮箱

我们在 git 里面，进行 commit 操作的时候，都需要设定一个 user.name 和 user.email，所以，对 commit 的签名，是基于 email 的。第一个步骤就是在 GitHub 的 Settings 里面，设置一个用于关联签名算法的 email。你可能已经有了多个 email，在本地，需要设置那个关联了 GPG 签名的 email 来提交代码。

## 生成一个 GPG 的 key

刚才已经说了，签名的原理是使用 GPG，其实 GitHub 还支持 S/MIME，我不知道那是什么，所以就选 GPG了。

GitHub 支持的加密算法有：

*   RSA
*   ElGamal
*   DSA
*   ECDH
*   ECDSA
*   EdDSA

如果加密算法不在上述之中，可能无法被 GitHub 所验证。如果，你的环境没有安装 GPG，第一步你可能需要安装一下：

```shell
brew install gpg2 # 我的环境是 Mac 就用 Homebrew 安装了
```

我在 Mac 上安装的是 GPG 2.x，其实有 GPG 1.x 和 2.x 两个版本，显然大一点的更新一些，支持了很多新功能，不过，有可能你所在的系统环境只能选择 1.x。2.1.17 版本以上的可以使用如下命令来生成 key：

```shell
gpg --full-generate-key
```

虽然官方说了支持上面 6 种算法，但是在 GPG 指南这里说，必须选择 RSA，我不知道这个矛盾是为什么，以后再来探究。上面的命令会开启一个命令行交互式创建 key pair 的过程，问及算法的时候，用默认的就行了，我用的 GnuPG 2.2.19，默认选项是 RSA and RSA。当问到 key 的长度的时候，要填写 4096，因为官方指南要求这样，而 GnuPG 的默认值是 2048，这里需要注意。

接下来是过期时间，个人使用选择 does not expire，永不过期就可以了。如果是团队使用，看整个团队的安全策略如何。

接下来要求填写 ID 相关信息，会填写名字，邮箱，注释，这里邮箱是比较关键的，在第 1 步里，咱们预先准备了要关联的邮箱地址。就填上那个。然后是要求键入密码。这个密码的用途是保护你的私钥。如果你自信不会有人入侵你的个人电脑，那么你可以不填写密码，GnuPG 会很贴(fan)心(ren)地走两遍这个要求密码保护的过程，请耐心回车。（注：假如很不幸，一个黑客已经黑到你个人电脑了，用你的身份打开了你的 Term，这时候，如果你的私钥是有密码保护的，每当程序需要使用你的私钥的时候，都必须输入密码，这个情况下，私钥保护密码就是最后一道屏障。）

```shell
gpg --list-secret-keys --keyid-format LONG
/Users/hubot/.gnupg/secring.gpg
------------------------------------
sec   4096R/3AA5C34371567BD2 2016-03-10 [expires: 2017-03-10]
uid                          Hubot (Comment) <Hubot@a.com>
ssb   4096R/42B317FD4BA89E7A 2016-03-10
```

使用上述命令就可以查看你 LONG 格式的私钥了。这个私钥就是要用来对你的每个 Commit 进行签名的。

## 在 GitHub 登记你的公钥

然后，咱们需要在命令行打印出来自己的公钥，使用如下命令：

```shell
gpg --armor --export 3AA5C34371567BD2
# Prints the GPG key ID, in ASCII armor format

-----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBF5bciABEADJ/FQa+ymIuKuZycgtPmLMPHEwOtYY21k7zU9ddDZH6ZGIxeN0
N9ljc6zp8/3cQDRrbrirHv/9WqaqSRb+EFcUog5LOfR/C6NeiGNW8AgUuFxGGFXK
s6VrAmzhIxDmKDkRdX9sHf7myiwBhtkFM0/8AGUdR8pjHKw+vA8IJzMhowWkiX1O
F1ZW81gKUYCLSfkty1HccGr4kFpE6r1R/w18hYH2zcr0dll0ox2LHfSHuuQzamew
hdR7B6S5Xi+EJjv7rujHaRWzLoPXktxUFme9LxdVblp6FD/lP79AkPhqSPAwzee+
ShlO9AScCCbsm8p3/KhmUn2yigbfd0eWvh4wm5HvbTCJ3/SLspMYrsF/VMHAJFRW
pmULevI5bdVR3fm7t/IgkjFasmbOZ9EqZNf43ljVi3SOyTmRX9GbxtvHXKL8tgL1
q7do0cArc/cKigEfssHe6gXChLZ6nDEzj/aNgOEcKo/cPVVCH4yzldEMvCB4aMYW
PET+7Io+FM1b69yOtFvKmJnGNpDbtySn1b6E0gWk/3uqzcspAzZMb6aIdZ6BcaXE
wU8zqRqcMXVnI6s2gvrMYrFCUB71ujzdGO9LWIu/y/FOdrzmrjXofOmdQom9Z+dW
cCo7LaTCE994HhLbqacsUROhjFCSzisH1yi0T0rD6oWSzsjFdewpEtjJGwARAQAB
tENDaGFybGVzIChHUEcga2V5IHVzZWQgZm9yIEdpdEh1YiBjb21taXQuKSA8Y2hh
cmxlc3RhbmdAZm94bWFpbC5jb20+iQJOBBMBCAA4FiEE6zd9skJwGmhOg6epkcp5
trRrrvQFAl5bciACGwMFCwkIBwIGFQoJCAsCBBYCAwECHgECF4AACgkQkcp5trRr
rvQ…… …… ……
-----END PGP PUBLIC KEY BLOCK-----
```

大概长上面那个样子的，很长很长，整段拷贝下来，然后去 GitHub 个人的 Settings 界面 SSH and GPG keys 标签里，登记这个公钥。登记完毕后，你能看到这个 key 关联的 email 地址显示出来了。

## 在 git 里面设定使用签名

咱们的公钥私钥对已经生成了，然后就是需要告诉 git 命令每次 Commit 的时候，都要使用私钥进行签名。

```shell
git config --global user.signingkey 3AA5C34371567BD2
```

上面的命令设定了全局的签名密钥，如果你使用多个身份在多个项目提交代码，那么不要使用 --global 参数，但是，要记得去每个项目里设置单个项目范围的签名私钥。然后，你要告诉 git 命令，以后每次 Commit 都要签名：

```shell
git config commit.gpgsign true
```

也可以手动控制，那么记得执行 git commit 的时候带上 -S 参数。

## 总结

到此，我们需要的设置已经全部设定完毕了，设定完毕后，执行一个 Commit，然后 Push，就可以在你的项目记录里看到，此次的 Commit 是带有 Verified 标记的了。

此外，有个关于隐私保护的话题。你在 GitHub 验证了一个邮箱，只有你的 Commit 关联了这个验证过的邮箱，在你贡献 PR 的时候，GitHub 才能在贡献人清单里显示出来你的帐号 ID。这也意味着，所有人，都可以看到你的这个电子邮箱，即隐私暴露。

在 GitHub 的 Settings 里面的 Emails 面板，有一个 keep my emails private 的选项，如果勾选了的话，那么关联了你的验证邮箱的 Commit 是无法被 Push 的，因为服务器知道你的隐私设定，会保护你不让你暴露你的私人邮箱。

听起来，如果你非要保护自己的隐私，就死锁了一样。不过，你可以选择，使用 GitHub 提供的匿名 noreply 邮箱，只是一个邮箱地址，并不能收发邮件。你在使用 GPG 进行签名的时候，可以把邮箱地址填成 GitHub 后台给你提供的匿名邮箱。这样，才能同时做到，既签名你的每个 Commit，又在你贡献 PR 的时候，追踪到你的 GitHub 帐号。

文首截图里的项目主页在此：[https://github.com/charlestang/trip-table-parser](https://github.com/charlestang/trip-table-parser) 可以去 commits 标签页里看看带验证的 commit 的效果。

全文完。

附：

*   [阮一峰——GPG 入门教程](https://www.ruanyifeng.com/blog/2013/07/gpg.html)
*   [GPG 30分钟简明教程（非原始网址）](https://www.2cto.com/article/201402/280652.html)