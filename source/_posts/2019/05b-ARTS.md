---
title: ARTS
tags:
  - arts
id: '808'
categories:
  - 日　　记
date: 2019-05-29 19:48:48
permalink: arts-no-1/
---

![unpreview](https://static001.geekbang.org/resource/image/53/75/53aa23a64b38291433ab59431bd61075.jpg)

左耳朵耗子，陈皓发起的 ARTS 打卡活动

## Algorithm

给定一个排序数组，你需要在**[原地](http://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)**删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。

不要使用额外的数组空间，你必须在**[原地](https://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)修改输入数组**并在使用 O(1) 额外空间的条件下完成。

**示例 1:**

> 给定数组 _nums_ = **[1,1,2]**, 函数应该返回新的长度 **2**, 并且原数组 _nums_ 的前两个元素被修改为 **`1`**, **`2`**。 你不需要考虑数组中超出新长度后面的元素。

**示例 2:**

> 给定 _nums_ = **[0,0,1,1,1,2,2,3,3,4]**,函数应该返回新的长度 **5**, 并且原数组 _nums_ 的前五个元素被修改为 **`0`**, **`1`**, **`2`**, **`3`**, **`4`**。你不需要考虑数组中超出新长度后面的元素。

```generic
func removeDuplicates(nums []int) int {
    
    l := len(nums)
    
    if l == 0  l == 1 {
        return l
    }
    
    i := 0

    for j := 1; j < l; j ++ {
        if nums[j] == nums[i] {
            continue
        } else {
            nums[i + 1] = nums[j]
            i ++
        }
    }
    
    return i + 1

}
```

这道题目是一道简单的题目，正在恢复对算法的训练，所以从简单的开始吧。以上答案是用 Go 语言完成的，我估计已经是我第四遍或者第五遍的代码了。我之前肯定刷过这道题目，但是今天仍然没有非常流畅自然地写对。还是写错了一次，然后我擦掉重写，发现这次写得比较简洁了。

思路很简单，第一个下标指向第一个位置，然后第二个下标从第二个位置开始起遍历，发现一样就继续往后跳，发现不一样，就把目标拷贝到第一个下标后面一个位置。直到第二个下标遍历完。

第一个下标 i 指向的元素，以及下标小于 i 的元素，是已经去重的。先看初始状态，i 指向 0，第一个元素，显然 i 以及 i 之前所有的元素都是去重的，因为一共只有 1 个元素，必然不会重复。

然后看一下循环，每一轮循环结束，如果 j 指向的元素，与 i 指向的相同，就把下标 j 往后 +1，如果不同，则把 j 指向的元素复制到 i + 1 指向的元素，而下标 i 也向后挪一个，如此循环结束后，仍然满足 i 以及 i 之前的元素都是不重复的。

循环结束后，i 正好指向着不重复的最后一个元素，其实每一轮结束后，i 都指向着不重复的最后一个元素。所以，最后不重复的元素的个数就是 i + 1 个。

以上使用循环不变式的方式分析了算法的正确性这个算法的时间复杂度是 O(n)。

## Review

[Avoiding Double Payments in a Distributed Payments System](https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb)

本周 review 的文章是这一篇《在分布式系统中避免双重支付问题》，这是 Airbnb 技术博客本周的封面文章。介绍了 Airbnb 支付团队在整个系统向 SOA 架构迁移的过程中，如何构建分布式的支付系统。

他们构建了一个类库，名叫 **Orpheus** 这是古希腊的一个神“俄尔浦斯” 的名字。这个类库主要原理，是利用 Java 的 lamda 演算，封装了一个严格要求幂等性的类库，将一次分布式事务拆分成 Pre-RPC，RPC 和 Post-RPC 三个阶段，将分布式事务中，本地数据库事务和 RPC 分隔，并在强幂等性要求下工作，从而保障系统的最终一致性。

文章介绍了这么实现的原因和带有的问题，以及团队如此选择的 trade-off。是一篇高质量的设计思想文章，衷心向大家推荐。

## Tip

想给大家分享的一个技巧点，就是在使用 Mac 的时候，经常需要使用 XCode 的命令行工具，比如 homebrew，比如我现在用 Visual Studio Code 做 Go 语言的 IDE，都需要用到这个命令行工具。怎么安装呢？

```shell
xcode-select --install
```

在 Mac 的 Shell 上执行上述命令，就可以激活 XCode 的 command line tools 的安装过程了。

## Share

这个礼拜分享的文章，是眼前刚遇到的一个问题，虽然不是技术文章，但是也跟技术人息息相关。

[《技术人走上管理岗位的困惑》](https://sexywp.com/tech-leader-worry.htm)