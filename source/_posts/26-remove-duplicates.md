---
title: 26. 删除排序数组中的重复项
tags:
  - algorithm
  - two pointers
id: '936'
categories:
  - - 算　　法
date: 2021-03-07 23:27:58
---

给定一个排序数组，要求把重复项删掉，然后返回新的去重数组的长度。要求空间复杂度 O(1)，其实发现一个重复的，就把后面的挪上来。这个题目直觉上就没有什么特殊的，硬做：

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        l = len(nums)
        if l == 0 or l == 1:
            return l
        r = 0
        p = r + 1
        while p < l:
            if nums[p] != nums[r]:
                nums[r+1] = nums[p]
                r += 1
            p += 1
        return r + 1
```

我写出了这样的方法，就是第一个指针指着开始位置，第二个指针指后面一个，然后往后挪第二个指针，如果遇到不重复的，就拷贝到第一个指针后面一个位置，遇到重复的就一直往后挪第二个指针。

提交后，这个算法通过了。看了题解，这个方法叫双指针。前面一个叫慢指针，后面一个叫快指针。

知识点：

1.  数组；
2.  双指针算法。