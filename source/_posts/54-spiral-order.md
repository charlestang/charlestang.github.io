---
title: 54. 螺旋矩阵 & 59. 螺旋矩阵 II
tags:
  - algorithm
id: '1038'
categories:
  - - 算　　法
date: 2021-03-15 12:38:16
---

好几天没有写题解了，为什么没有写呢？就是我觉得好像这道题没有什么意义：比如，这道题，极其繁琐，没什么巧思；或者，这道题，根本就是脑筋急转弯，想得出来就无比轻易，想不出来就误入歧途，功底无用。

这种状态就是极其危险的状态，所谓的高不成、低不就。非要等一道完美的题目出现，才去认真学习和分析么？这是心飘了。要警惕，深刻地警惕。每道题，都要认真对待，尽量读懂，自己做出来了，要跟别人的做法去比较，自己做不出来，要看懂别人的做法，不能轻视一道题目。

自勉结束，看看今天的打卡题。题目要求是按照顺时针螺旋顺序，打印一个给定的 m×n 的矩阵。也就是字面意思，我不想抄题目了，给个传送门吧。[这里是传送门](https://leetcode-cn.com/problems/spiral-matrix/) 。
<!-- more -->
说起来好笑，虽然我连续练习了三周算法题了，但是我看到没见过的题，大脑就是习惯性一片空白，只能想出来最最朴实的做法。就是从左上角开始，往右套圈，遇到边界就拐弯。唯一要解决的就是避免路径重复问题。我想到的就是记住曾经访问过的边界，如果下标超过了长宽，或者遇到曾经访问过的路径，就转向，如果转向也转不了，就退出循环。

于是，我写出了这样的代码：

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        vi = {}
        vj = {}
        i, j = 0, 0
        res = []
        h = len(matrix)
        w = len(matrix[0])
        while True:
            while not vj.get(j, False) and j < w:
                res.append(matrix[i][j])
                j += 1
                vi[i] = True
            j -= 1
            i += 1
            if i >= h or vi.get(i, False):
                break
            while not vi.get(i, False) and i < h:
                res.append(matrix[i][j])
                i += 1
                vj[j] = True
            i -= 1
            j -= 1
            if j < 0 or vj.get(j, False):
                break
            while not vj.get(j, False) and j >= 0:
                res.append(matrix[i][j])
                j -= 1
                vi[i] = True
            j += 1
            i -= 1
            if i < 0 or vi.get(i, False):
                break
            while not vi.get(i, False) and i >= 0:
                res.append(matrix[i][j])
                i -= 1
                vj[j] = True
            i += 1
            j += 1
            if j >= w or vj.get(j, False):
                break
        return res
```

用两个字典，vi 和 vj，是 visited i 和 visited j 的缩写，代表曾经访问过的下标。我们横向扫描一行的时候，就会导致这个下标 i 所有的值都已经被遍历了，未来都不会再回来了。我们纵向扫描一列的时候，就会导致这一列 j 所有值都遍历了。

因为是从外向内螺旋，i，j 被完全遍历，不是顺序的，是第 0 行，第 j - 1 列，第 i - 1 行，第 0 列这样的顺序，所以我就用了无序的散列来记录曾经访问过的下标。写循环的时候，我一时半会儿意识不到循环终止的条件或者终止条件很复杂，我就先写个 while True 放那里。然后，写三次拐弯的方法。

每次拐弯后，都要判断，拐完毕后，当前这个座标是否有效，没有越界，也未访问过，那就继续遍历。遍历的过程也要不停地判断，是否已经越界或者重复。整个算法基本就是天然思路的算法表达。如果没写错，是可以正确终止的。

遗憾的是，我还是写错了，所以，vi 和 vj 写混了，变量太短，就容易混用，而且不好调试。一眼看不出问题。上面的写法，时间复杂度是 O(m×n)，空间复杂度是O(m+n)。

我这个写法很长，而且，太直白了，缺点也很 明显，就是非常容易写错，而且很难检查，再者就是里面大量的重复。似乎每一段都在重复似的，仔细看吧又有细微差别，确实写得太差了。看完官方解法发现，我这个思路叫模拟法，官方也是用模拟法，怎么写的呢？

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return []
        h = len(matrix)
        w = len(matrix[0])

        # direction 方向
        d = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        # visited 访问记录
        v = [[False] * w for _ in range(h)]
        
        i, j, res = 0, 0, []
        cur_d = 0
        for _ in range(w * h):
            res.append(matrix[i][j])
            v[i][j] = True
            pre_i, pre_j = i + d[cur_d][0], j + d[cur_d][1]
            if not (0 <= pre_i < h and 0 <= pre_j < w and not v[pre_i][pre_j]):
                cur_d = (cur_d + 1) % 4
            i, j = i + d[cur_d][0], j + d[cur_d][1]
        return res
```

这是我根据看懂了官方解法后，默写的。其实原理是一样的，但是优点是，整个代码里没有重复，用四个变量表示了方向，用取模的形式表示转弯，用总数量限制了循环次数，不会像使用 while True 一样战战兢兢担心死循环。

这个写法的时间复杂度是 O(m×n)，空间复杂度是 O(m×n)，似乎比我的写法用了更多内存，不过换来了思路的流畅。

官解之外，我看到了一种解法，很巧妙，就是设定上、下、左、右的边界，每次拐弯后，重新确定上下左右边界，确保迭代不会越界，看懂了他的解法后，我把上面算法改成了：

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return []
        # 上 top，下 bottom，左，右边界
        t, b, l, r = 0, len(matrix), 0, len(matrix[0])
        # direction 方向
        d = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        i, j, res = 0, 0, []
        cur_d, total = 0, b * r
        for _ in range(total):
            res.append(matrix[i][j])
            pre_i, pre_j = i + d[cur_d][0], j + d[cur_d][1]
            if not (t <= pre_i < b and l <= pre_j < r):
                if cur_d % 4 == 0:
                    t += 1
                if cur_d % 4 == 1:
                    r -= 1
                if cur_d % 4 == 2:
                    b -= 1
                if cur_d % 4 == 3:
                    l += 1
                cur_d = (cur_d + 1) % 4
            i, j = i + d[cur_d][0], j + d[cur_d][1]
        return res
```

这个算法是一开始就确定了上下左右边界，然后每次拐弯重新确定边界，这样做的好处是，不用开辟一个 visited 数组了，使得空间复杂度优化到了 O(1)。确实相当巧妙。

没想到，才刚过了一天，又遇到了螺旋矩阵，这天的打卡题是 [59. 螺旋矩阵 II](https://leetcode-cn.com/problems/spiral-matrix-ii/)，跟昨天略微有所不同的是，今天要求，生成一个螺旋方阵，其实昨天的题目已经尝试了写法，今天就正好来复习一下昨天的写法：

```python
class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        length = n * n
        nums = [i for i in range(1, length + 1)]
        res = [[0 for _ in range(n)] for _ in range(n)]
        d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        t, b, l, r = 0, n, 0, n
        i, j, cur_d = 0, 0, 0 
        for k in range(length):
            res[i][j] = nums[k]
            pre_i, pre_j = i + d[cur_d][0], j + d[cur_d][1]
            if not(t <= pre_i < b and l <= pre_j < r):
                if cur_d == 0:
                    t += 1
                elif cur_d == 1:
                    r -= 1
                elif cur_d == 2:
                    b -= 1
                else:
                    l += 1
                cur_d = (cur_d + 1) % 4
            i, j = i + d[cur_d][0], j + d[cur_d][1]
        return res
```