---
title: 20. 有效的括号
tags:
  - algorithm
  - hash table
  - stack
id: '934'
categories:
  - - 算　　法
date: 2020-08-07 15:59:44
---

先来看题目的描述：

> 给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。
> 
> 有效字符串需满足：
> 
> 1. 左括号必须用相同类型的右括号闭合。
> 
> 2. 左括号必须以正确的顺序闭合。
> 
> 3. 注意空字符串可被认为是有效字符串。
> 
> [20. 有效的括号](https://leetcode-cn.com/problems/valid-parentheses/) <-- 点此传送

主要就是判断这个括号是否配对，麻烦点就是有三种括号，这个题目，直觉上，就是需要用到数据结构——栈（Stack），但是我好像不是很熟悉，在 Python 里，栈这个数据结构怎么写，应该是用个类库或者语言自带的某种数据结构来实现。这里暴露了我不熟悉 Python 的数据结构这件事情。

所以，我想到了，我先用递归算法，把这个问题给解决掉，然后，再看答案学习这个栈怎么用好了。这个题目显然具备某种递归结构，我们在整个串里搜索第一个配对的括号，然后去掉这一对括号后，剩余的字符串，应该仍然是合法的字符串，找不到，或者剩下的字符串不合法，那就一定是不合法的。

另外，如果整个串是合法的，至少有一对连续的两个字符，正好是配对的。于是我的算法就是先找到这一对挨着的，然后去掉，递归判断剩下的。

```python
class Solution:
    def isValid(self, s: str) -> bool:
        if s == "" :
            return True
        mapping, i, l = {'(':')', '{':'}', '[': ']'}, 0, len(s)
        while i < l:
            if i + 1 < l and s[i+1] == mapping.get(s[i], ""):
                left = s[:i]
                right = ""
                if i + 2 <= l:
                    right = s[i+2:]
                return self.isValid(left+right)
            i += 1
        return False
```

做对题目后，我看了题解，原来 Python 的 stack 就是最简单的用 list 实现的，真是方便啊：

```python
class Solution:
    def isValid(self, s: str) -> bool:
        mapping = {')': '(', '}': '{', ']': '['}
        stack = []
        for c in s :
            if c in mapping:
                top = stack.pop() if stack else '#'
                if mapping[c] != top:
                    return False
            else:
                stack.append(c)
        return not stack
```

知识点：

1.  Python 的栈可以用 list 实现，压栈操作是 append，出栈是 pop；
2.  list 变量可以直接在 if 条件中判断是否为空，空 list 为 False；
3.  key in dict 语句，可以直接判断一个字典是否包含某个 key；