---
title: 1006. 笨阶乘
tags:
  - algorithm
  - stack
id: '1051'
categories:
  - - 算　　法
date: 2021-04-20 14:18:22
---

> 通常，正整数 n 的阶乘是所有小于或等于 n 的正整数的乘积。例如，factorial(10) = 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1。
> 
> 相反，我们设计了一个笨阶乘 clumsy：在整数的递减序列中，我们以一个固定顺序的操作符序列来依次替换原有的乘法操作符：乘法(*)，除法(/)，加法(+)和减法(-)。
> 
> 例如，clumsy(10) = 10 * 9 / 8 + 7 - 6 * 5 / 4 + 3 - 2 * 1。然而，这些运算仍然使用通常的算术运算顺序：我们在任何加、减步骤之前执行所有的乘法和除法步骤，并且按从左到右处理乘法和除法步骤。
> 
> 另外，我们使用的除法是地板除法（floor division），所以 10 * 9 / 8 等于 11。这保证结果是一个整数。
> 
> 实现上面定义的笨函数：给定一个整数 N，它返回 N 的笨阶乘。
> 
> 示例 1：  
> 输入：4  
> 输出：7  
> 解释：7 = 4 * 3 / 2 + 1  
> 
> 示例 2：  
> 输入：10  
> 输出：12  
> 解释：12 = 10 * 9 / 8 + 7 - 6 * 5 / 4 + 3 - 2 * 1
> 
> 1006. 笨阶乘 <--- [传送门](https://leetcode-cn.com/problems/clumsy-factorial)
<!-- more -->
这题目是 4 月 1 日的打卡题，难度是“中等”。这道题，看起来又是表达式求值的题目。以前我一看到表达式求值，就会想到逆波兰表达式。其实，不过，刷了一些题我发现，这可能是个误区，因为逆波兰表达式，虽然说具有更好的通用性，可能像左耳朵耗子说的，是工程思维如何如何，但是，说实在的，逆波兰表达式很不好实现的。非常容易写错。

```python
class Solution:
    def clumsy(self, N: int) -> int:
        ops = ['*', '/', '+', '-']
        op_stk = []
        stk = []

        oi = -1

        for i in range(N, 0, -1):
            if oi >= 0:
                next_op = ops[oi % 4]
                while op_stk and (op_stk[-1] in '*/' or (op_stk[-1] in '+-' and next_op in '+-')):
                    stk.append(op_stk.pop())
                op_stk.append(next_op)
            oi += 1
            stk.append(i)
        while op_stk:
            stk.append(op_stk.pop())

        stk = stk[::-1]
        res = []
        while stk:
            op = stk.pop()
            if isinstance(op, int):
                res.append(op)
            else:
                op2 = res.pop()
                op1 = res.pop()
                if op == '*':
                    res.append(op1 * op2)
                elif op == '/':
                    res.append(int(op1 / op2))
                elif op == '+':
                    res.append(op1 + op2)
                else:
                    res.append(op1 - op2)
        return res.pop()
```

这是我写的一个逆波兰表达式的实现。其实，我每次写，都不一定能写对，从动了念头，到完全写对，每次都要耗费一小时以上的时间，关键这个不常用，你不可能总是保持着对这个东西的熟练度。

逆波兰表达式的难点其实有两个，一个是生成后缀表达式，另一个是表达式的求值。生成表达式的时候，主要麻烦是运算符优先级，没有括号会好写一点，有括号稍微麻烦一点，总体差不多。而且，这时候要用到两个栈。

求值的时候，难点在于操作数的顺序，对于除法和减法来说，顺序是有关系的。所以总是容易搞错的。求值的时候其实也要一个额外的栈来辅助。

这个解法的好处是，对加减乘除表达式的计算，一般来说是通吃的，通用性注定了这个东西的复杂。

其实，在解题的环境下，追求的只是答案，完全没必要考虑方法的通用性。所以，我们可以只用一个栈，遇到乘除法，就直接求解，然后压栈，最后统一求加减法。

```python
class Solution:
    def clumsy(self, N: int) -> int:
        op = '*/+-'
        stk = [N]
        N -= 1
        idx = 0

        while N:
            next_op = op[idx % 4]
            idx += 1

            if next_op == '*':
                stk.append(stk.pop() * N)
            elif next_op == '/':
                stk.append(int(stk.pop() / N))
            elif next_op == '+':
                stk.append(N)
            else:
                stk.append(-N)
            N -= 1
        
        res = 0
        while stk:
            res += stk.pop()
        
        return res
```

这个算法里，只利用了一个栈，遇到乘法除法的时候，直接计算结果，最后再计算加减法。虽然没有通用性但是解法简洁清晰。空间复杂度降低，编写也简单了很多，非常容易理解。我觉得，经过训练应该能掌握到写出这种解法的能力。

此外还有一种解法是另辟蹊径。就是通过公式推导或者观察来发现规律。

```generic
N      N % 4    clumsy
1  1  1
2  2  2
3  3  6
4  0  7
5  1  7
6  2  8
7  3  6
8  0  9
9  1  11
10  2  12
11  3  10
12  0  13
13  1  15
14  2  16
15  3  14
16  0  17
17  1  19
18  2  20
19  3  18
20  0  21
……
```

仔细观察这个数列，就可以看到，除了前 4 个，数列后面的数字是很有规律的。当 N % 4 = 0 的时候，clumsy = N + 1，N % 4 = 1 or 2 的时候，clumsy = N + 2，当 N % 4 = 3 的时候，clumsy = N - 1，基于这个规律，可以直接写一个算法：

```python
class Solution:
    def clumsy(self, N: int) -> int:
        if N == 1:
           return 1
        if N == 2:
            return 2
        if N == 3:
            return 6
        if N == 4:
            return 7
        if N % 4 == 0:
            return N + 1
        if N % 4 == 1 or N % 4 == 2:
            return N + 2
        return N - 1 
```

这个算法有着 O(1) 的时间复杂度和 O(1) 的空间复杂度，效率最高，是因为直接看破了后面的规律，所以数学才是最强的工具，不过这个规律是很难看破的。