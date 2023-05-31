---
title: 66. 加一
tags:
  - algorithm
id: '944'
categories:
  - - 算　　法
date: 2021-02-19 11:14:23
---

这个问题也是极其的简洁，就是把一个整数，按位拆分到一个 list 里面，然后，在低位加一，然后让你处理好进位问题。学了几次的列表反转，终于可以在这里派上用场了，难得我想起来用一次：

```python
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        digits, carry = digits[::-1], 1
        for i in range(len(digits)):
            digits[i] += carry
            carry, digits[i] = digits[i] // 10, digits[i] % 10
            if carry == 0:
                break
        if carry == 1:
            digits.append(1)
        return digits[::-1]

```

数字的加法，是把 1 加到列表的最右边，但是列表的迭代从最左边比较容易，所以我反转一下，当然这有代价。

然后，我假设现在进位已经有 1 了，原题目正好就是这个意思。然后，迭代处理进位就行了。如果进位最后还剩下 1 ，那么 append 个 1（翻转后的好处），返回的时候，再翻转回去即可。

这样一段代码，不瞒你说，写了三次才写对。你还能写得比我更差么？