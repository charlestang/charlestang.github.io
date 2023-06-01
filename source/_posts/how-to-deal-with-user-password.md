---
title: 【PHP 最佳实践】如何处理用户的密码
tags:
  - PHP
  - practice
  - security
id: '752'
categories:
  - - something-about-daily-work
    - PHP
  - - 工作相关
date: 2016-12-15 17:38:26
---

哪怕到了最近几年，数据库被黑客完整下载的安全事件，也是层出不穷，程序员世界戏称为“脱裤”，好像光屁股一样羞耻。比如，刚过去不久的 CSDN，小米，多玩，等等事件都还历历在目。所以，程序员写代码决不能抱有侥幸心里，用户的密码，是最最隐私的东西，一定要妥善处理，一旦泄露，会给用户和服务网站都带来不可估量的损失。
<!-- more -->
## 决不能使用明文存储密码

```shell
mysql> select * from user;
+----+----------+-----------+
 id  username  password  
+----+----------+-----------+
  1  charles   123456    
  2  john      p@ssword! 
+----+----------+-----------+
2 rows in set (0.00 sec)

```

（上面是一个明文存储密码的例子，这是反例，不要学习！）关于密码处理的问题，我们都知道一个常识，就是密码是不可以明文存储的，前几年某个网站泄露数据，竟然露出来用户的明文密码，在网上引起轩然大波，大家都怒不可遏，仿佛自己最心底的秘密被人泄露了一样的。密码一定要加密存储，这个事情，是不消多说的。

虽然，我们嘴里称是加密存储，其实，我们谈论的是散列算法，但是我发现很多年轻的程序员，甚至不明白什么是散列，也不明白自己使用的算法的真实性质，大谈特谈 MD5 加密，当我问及怎么解密的时候，都会回答说有库函数，具体忘记了。其实，MD5 是一种摘要算法，其本质是一种散列算法，经过 MD5 处理的字符串不是所谓的加密，因为处理过的字符串，是不可以“解密”的，是单向不可逆的，也就无所谓解密。

```shell
mysql> select * from user;
+----+----------+----------------------------------+
 id  username  password                         
+----+----------+----------------------------------+
  1  charles   *6BB4837EB74329105EE4568DDA7DC67 
  2  john      *BC0CAD86CB7384674820C1603955807 
+----+----------+----------------------------------+
2 rows in set (0.00 sec)

```

（上面是使用一次散列算法存储的密码，这里用的是 MySQL 的 PASSWORD 函数）能知道 MD5 散列存储用户密码，你在这个点上，至少可以得 50 分了。但是，这么处理了，仍然是不及格的，因为黑客的手段也是非常高明的，他们在日复一日，年复一年地积累攻击经验。对付这种简单的散列，最简单的办法，就是使用字典，因为黑客发现，用户往往喜欢使用比较有规律的数字和字母组合来设计自己的密码，而人类的智力都是差不多相似的，能想出来的东西，也非常接近，只要留心去收集用户常用的密码组合就好了，天长日久下来，竟然能积累到上千万的字典条目，一般没有受过训练的用户，能想出来的密码，可以被覆盖 60% 以上。

```shell
mysql> select * from user;
+----+----------+----------------------------------+-----------------------+
 id  username  password                          salt                  
+----+----------+----------------------------------+-----------------------+
  1  charles   *9A5E2BDC06CBCB10B2A27376512829A  4329105EE4568DDA7DC67 
  2  john      *D2B23C464BA1D0773E8B962BA52DBAE  7384674820C1603955807 
+----+----------+----------------------------------+-----------------------+
2 rows in set (0.00 sec)

```

（上面为，在存储散列值的时候，加上盐，即便密码和算法都没变，我们看到密码散列值已经变了）于是，程序员想到了在存储散列值之前，给密码加点“盐”。也即，在计算用户的密码散列值前，先给密码上拼接一个随机字符串，这样，得到的散列值，对应的就不是用户的密码原文串了，而是原文串 + 随机的“盐”值。给使用字典攻击的经典办法增加了巨大的难度，非要找到对应的盐值不可，所以也可以想见，真正安全的“盐”，需要每个用户一个才比较安全。使用平台统一的“盐”，一旦泄露，还是形同虚设。做到这一步，大概可以 60 分了。

## 使用更安全的算法

大部分人做到及格可能就满足了，但是，如果你真这么满足了，那就太天真了，根据最新的一些报道和研究，高性能的计算机运行的[暴力密码破解器](https://www.zhihu.com/question/21558046/answer/18697166)，计算 MD5 的速度，已经达到了每秒 70 亿次，SHA-1 也能达到每秒 20 亿次，而用户并没有因为计算机能力的提升而改变自己设置密码的复杂度，大部分用户至多使用数字+字母的组合，这种组合方式，整个密码空间也就没多少，一旦黑客拖库下来以后，即便有盐，针对每个用户穷举一遍整个密码空间，也不会花太多时间。

为了应对这种暴力碰撞散列值的破解方法，专家专门发明了专门为了保存密码而设计的 bcrypt 算法，而在 PHP 语言里，也直接提供了内置函数来处理这个问题。上文提到的暴力密码破解器，计算 bcrypt 的速度，只能达到 4000 次每秒。

```shell
php > $a = 'my super paasword';
php > echo password_hash($a, PASSWORD_DEFAULT);
$2y$10$DFbAoPRDZbGk1C3sl2ofjeyGpZH4X1PEXgIzGwN32AagWT4WS3rB6
php > echo password_hash($a, PASSWORD_DEFAULT);
$2y$10$7N4lwm8ulVKwZX2NDPek.OKSWkQHvQSXNASKx3LrAqy3NPFosLPm.
php > echo password_hash($a, PASSWORD_DEFAULT);
$2y$10$x3d8nVghO7V1Z.dhi.pu0enMXymVgyoJ9O/LHbi3S5gF8EDB97cAe
php > var_dump(password_verify($a, '$2y$10$x3d8nVghO7V1Z.dhi.pu0enMXymVgyoJ9O/LHbi3S5gF8EDB97cAe'));
bool(true)
php > var_dump(password_verify($a, '$2y$10$7N4lwm8ulVKwZX2NDPek.OKSWkQHvQSXNASKx3LrAqy3NPFosLPm.'));
bool(true)

```

如果大家使用 Yii 框架的 2.x 版本，则框架提供了 Security 类来专门处理各类的加密/解密，密码的 Hash 和 Verify 等问题，比起自己再去封装库函数，更加方便和完善。Security 是 /yii/web/Application 启动后默认加载的组件，所以，可以直接使用，下面是使用的代码范例。

```php
/**
 * Validates password
 *
 * @param string $password password to validate
 * @return boolean if password provided is valid for current user
 */
public function validatePassword($password)
{
    return Yii::$app->security->validatePassword($password, $this->password_hash);
}

/**
 * Generates password hash from password and sets it to the model
 *
 * @param string $password
 */
public function setPassword($password)
{
    $this->password_hash = Yii::$app->security->generatePasswordHash($password);
}

```

## Log 里也不能放松警惕

使用了较为强力的散列算法，还要形成很好的操作规范和实现方法。以前我在腾讯工作的时候，注意到腾讯的网站上使用用户的密码，是在客户端就完成了散列后，再传输到服务器的，也即即使从网络抓包，即使没有 HTTPS 的传输安全，用户的明文密码也不会被嗅探到，基本做到了最高级别的保密措施。所有腾讯的网站上都引用一个算法库，在传输用户的密码前，首先完成三次 MD5 而且还要加一个一次性的“盐”。

如果没有做到这种级别，还有一个常见的泄露用户密码的地方，就是后台程序员为了调试问题方便，经常在磁盘上打印 Log，有很多请求，是带有用户密码提交的，而且这些密码都是原文，如果没有安全意识，把用户的密码打印在 Log 里面，一旦泄露了，那么上述的所有努力，都已经付诸流水了，黑客一旦拿到了你的 Log 文件，那么就可以畅通无阻，完全不用费力去破解你的密码或者碰撞密码的散列值，这个是万万要小心的地方。

## 总结

安全编码，一方面需要程序员积累很多的知识和经验，另一方面，也需要程序员养成很好的习惯，锤炼自己的安全意识，千万不要在小处随便，那样迟早酿成大错。