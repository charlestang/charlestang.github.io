---
title: 死磕 KMP 算法笔记
tags: []
id: '1112'
categories:
  - - 日　　记
updated: 2024-03-24 01:58:19
---

还在读大学时候，就久仰了 KMP 算法的大名，但是无奈智商有限，我就从来没有看懂过 KMP 算法，前几天，遇到一个题目，正好用到了字符串匹配，[第 1044 题](https://leetcode-cn.com/problems/longest-duplicate-substring/)，非常巧妙，二分法 + 哈希 + 字符串匹配。

很搞笑的是，我的记忆出现了偏差，其实 10 个月前，我做题做到 strStr() 这道题目，就遇到了字符串匹配算法，当时就下狠心去看了 KMP，可惜没有看懂。我只记得自己花了努力，没记清楚到底看懂了没有，就把自己的记忆美化成了“当时看懂了”。然后，还跟朋友吹了个牛。结果，我[写了篇博客](https://sexywp.com/28-strstr.htm)记住了这一切。啪啪打脸。

上次是 2 月 24 日，这次是 12 月 24 日，正好时隔 10 个月，看来还是要真正掌握了才行。

### 朴素算法

我看知乎里，有人管这个叫 Brute-Force 算法，中文就是残忍的力量，也就是暴力算法。《算法导论》里面就委婉很多，叫 Naive-String-Matcher，中文就是幼稚算法，还是喜欢这个名字，让我想起了长者。

给定一个较长的字符串，在里面寻找一个重复出现多次的较短的子串。更一般化，可以认为两者的长短并不影响这个搜索的结果。不过还是给我们一个正确的联想。题目里一般管前面那个参数叫 haystack，一大堆干草，后面那个参数叫 needle，针。在一大堆干草里寻找一根针。很形象。

讨论问题时候一般管后面那个字符串叫模式，管这个搜索过程叫模式匹配。我们假设前面一个字符串的长度是 n，后面一个字符串的长度是 m。

那么朴素的算法是怎么在 haystack 里面搜索 needle 的呢？needle 既然是 haystack 的一个潜在的子串，那么必然有一个开始的位置和一个结束的位置，我们穷举每一个可能的开始位置，就是 0 开始，假设这个位置就是 needle 的开始位置，然后逐位比较，如果全部比较完毕，那么搜索成功，否则，就假设下一个位置是 needle 的开始位置，重复这个过程。写成代码是：

```python
def strStr(self, haystack: str, needle: str) -> int:
    n = len(haystack)
    m = len(needle)

    for i in range(n - m + 1):
        for j in range(m):
            if haystack[i + j] != needle[j]:
                break
        else:
            return i
    return -1
```

这个代码确实非常 naive，很好理解。里面用到一个 Python 的编程技巧，我也是刚学会的，点[这里](https://book.pythontips.com/en/latest/for_-_else.html)可以查看细节。这个算法的时间复杂度相当显然，就是 O((n-m+1)*m)，上面我这个写法，在 [LeetCode 28 题](https://leetcode-cn.com/problems/implement-strstr/)里，是无法通过的。80 个用例里过了 78 个，第 79 个会 TLE，超时，因为时间复杂度太高。

### Rabin-Karp 算法

幼稚算法为什么复杂度太高呢？因为穷举每个开始位置，确认是否匹配的过程，计算复杂度需要 O(m)，那么能不能把确认匹配的过程复杂度降下来呢？这个 Rabin-Karp 算法，做出了有益的尝试。

假设，我们搜索的两个字符串，全部都是数字组成的，例如：我们在字符串 234158972413 这个字符串里，检索 1589 这个字符串。如果把 1589 理解成字符，那就是1 、5、8、9，四个。如果我们把它理解成 10 进制数呢？那就是一千五百八十九。

我们还是穷举每一个开始位置，从第 0 位开始，我们第一个比较的是 2341 和 1589，如果理解成十进制数，我们在 O(1) 就可以确定两者不相等，相等也是同理。这是数字的比较，只要一个位运算即可，是常数次，不管数字是什么。

再来看第二个位置，第二个数字是 3415。从 2341 如何变成 3415 呢？去掉开头的 2，增加末尾的 5。写成算式是 (2341 - 2 * 1000) * 10 + 5，注意用了 2 次乘法，一次减法，一次加法。只有 4 次运算，也是常数次。不难想象，这个开始位置每次往后滑动，都只会通过常数次运算，就可以完成匹配与否的检查。我们就通过这个算法把 O(m) 降低到了O(1)，整个字符串匹配算法的复杂度，下降到了 O(n - m + 1)。

接下来的难点是什么呢？就是我们比较的字符串，不是十进制数，而是字符。运用一点抽象思维，其实字符我们完全可以理解成数字。最简单的办法，就是把字符用其 ASCII 码来表达。只是得到的数字不是是十进制。如果比较的字符串是 ASCII 范围内的，那么可能是 95 进制，因为有 95 个可见字符。注意，95 是个例子，显然也可以是 95000 进制，也没什么区别。

另外一个难题是什么呢？如果 needle 非常长，比如 100位，那么无论几进制，一个整型变量都无法容纳这个数字。如果用大整数来表达的话，就得不偿失了。幸好，数学家还有一个法子就是取模。取模可以让一个大数变得很小。不过根据同余定理，两个数对同一个模的余数相等，这两个数字可能相当，也可能相差了模的若干倍。所以，要求我们在选取模的时候，尽量选取一个大的素数，减少模相等的概率。不过一旦遇到了模相等的情况，还是需要通过逐位比较，才能确认匹配。这就导致这个算法在精心构造碰撞的前提下，时间复杂度跌落到跟幼稚算法一样了。

不过实际运行时候，远比最坏情况要好。我依据这个原理，编写算法如下：

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        n = len(haystack)
        m = len(needle)
        if m == 0: return 0
        if n == 0 or n < m: return -1

        mod = 13131
        h = 0
        nums = [ord(c) - ord('a') for c in needle]
        h1 = 0
        nums1 = [ord(c) - ord('a') for c in haystack]
        for i in range(m):
            num = nums[i]
            num1 = nums1[i]
            h = (h * 26 + num) % mod
            h1 = (h1 * 26 + num1) % mod
        if h == h1 and self.check(0, haystack, needle): return 0

        A = pow(26, m, mod)
        for i in range(1, n - m + 1):
            h1 = (h1 * 26 - nums1[i - 1] * A + nums1[i + m - 1]) % mod
            if h1 == h:
                if self.check(i, haystack, needle):
                    return i
        return -1


    def check(self, i: int, haystack: str, needle: str) -> bool:
        for j in range(len(needle)):
            if haystack[i + j] != needle[j]:
                break
        else:
            return True     
        return False
```

上面是我根据原理写的 Rabin-Karp 算法，因为 28 题的限制是只有小写字母，所以我选 26 进制就够了，这是 Magic Number 26 的由来，其实，选取的数字只要大于 26 就行了。模的值，我就随便选了一个素数。这个算法是正确的，可以 AC，beat 65%，可见还是比较快的。

为什么要提及这个算法呢，当然还是为了衬托伟大的 KMP 咯，因为 KMP 的均摊时间复杂度比这个算法还要低的。Rabin-Karp 算法的优势是，关键时刻，这个算法远远比 KMP 容易写出来，并且写正确。因为你知道原理，现场通过自行推导并写正确的可能性还是很高的。

### KMP 算法

终于来到了本文的重头戏，KMP 算法。这个算法的来历，很简单，就是K，M，P 三位牛人，在1977年各自独立提出的，他们可能也是世界上最聪明的人。

该算法突破时间复杂度的桎梏的思路和 Rabin 和 Karp 两位大神不太一样，后者是在提高比较的速度（转化成数字），而前者，是在减少比较的长度（快速移动模式串）。

在幼稚算法里，haystack 上的比较指针，每次都要回到新的开始位置，逐位向后比较，所以，最坏的复杂度是O(n * m)，如果这个指针只往前走，从不回头，那么复杂度就会降低到 O(n)。这就是这个算法带来的一个很厉害的效果。

haystack 上的指针不往后退，只能是把 needle 用更快的速度往前移，怎么移就成了一个很关键的问题。解释这个问题是非常困难的，甚至画一张图，已经很难说清楚了，一般都要画一系列图，甚至连成动画，录制视频来讲解。我随便贴一个我看过的视频吧。[这里。](https://www.bilibili.com/video/BV1jb411V78H?spm_id_from=333.1007.top_right_bar_window_history.content.click) 这是一个 B 站的 Up 主录制的，我觉得动画做的不错，讲解也清楚。我没那个能力就不献丑了。

看过很多文章，很多视频后，我才勉强理解了这个算法的基本原理。概括一下就是，needle 已经匹配过的部分，如果其后缀和前缀相同，那么 needle 可以往前移动到最长相同后缀的位置。这话听起来是很绕的，不过相信你看过很多视频后，你会归纳出和我相同的话。

先展示一下代码：

```python
def strStr(self, haystack: str, needle: str) -> int:
    n = len(haystack)
    m = len(needle)
    if m == 0: return 0

    next = [0] * m

    i, j = 1, 0
    while i < m:
        if needle[i] == needle[j]:
            i += 1
            j += 1
            if i < m:
                next[i] = j
        else:
            if j == 0:
                i += 1
            else:
                j = next[j]
    
    i, j = 0, 0
    while i < n:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if  j == m:
                return i - j
        else:
            if j == 0:
                i += 1
            else:
                j = next[j]
    return -1
```

这个算法有个非常神奇的地方，就是看懂很难，你可能废了千辛万苦才看懂，你发现，当你想写的时候，大脑一片空白，在看懂的前提下，非常难写出来。所以才怀疑自己是不是太笨了，有人能发明出这种算法，但是我连学都学不会。