---
title: 630. 课程表III
tags:
  - algorithm
  - greedy
  - heap
id: '1107'
categories:
  - - 算　　法
date: 2021-12-14 15:21:05
---

好久没有写做题日记了，今天这题目有点意思，我做得蛮开心的。

> 这里有 n 门不同的在线课程，按从 1 到 n 编号。给你一个数组 courses ，其中 courses[i] = [durationi, lastDayi] 表示第 i 门课将会 持续 上 durationi 天课，并且必须在不晚于 lastDayi 的时候完成。
> 
> 你的学期从第 1 天开始。且不能同时修读两门及两门以上的课程。
> 
> 返回你最多可以修读的课程数目。
> 
> 630. 课程表III ---> [传送门](https://leetcode-cn.com/problems/course-schedule-iii)

这个题目意思看得挺绕的。举个生活中的例子来说明这个意思，就比如，你买了一张游戏点卡，一旦激活每天扣 1 点，一共 30 点，但是半年内必须用完。于是，你得到的 [durationi, lastDayi] 是什么呢？[30, 180]。

这里有个显而易见的事情，如果 durationi > lastDayi，那么就是一个不可能值，durationi 不能被消耗完。你买个 30 天的游戏点卡，但是 2 天内必须用完，所以就是你不可能用完。因为两天你只能用掉 2 点。所以，我们做题的时候，只要挑那些 durationi <= lastDayi 的数组就可以了。如果没有满足的数组，那么可以直接返回 0。

接下来就开始思考，怎么挑课了。其实，你要这么想，既然 durationi <= lastDayi 那就说明，每上一门课，都会剩余一些时间，才能到 lastDay，最少会剩余 0 天，一般都或多或少会剩一些。上得课越多，攒得日子越多，越不容易突破 lastDay。那么最简单的做法，就是把所有数组按照 lastDayi 的大小，排序即可。然后，我们用一个变量记录上过一门课后，消耗的日子，如果当前课程消耗的天数，加上消耗的总天数，没有超过 lastDayi，那么就可以修此门课。否则就不行。

可以想见，在lastDayi 相同的课程里，我们上 durationi 持续天数最短的课程，比较有利后面上更多课，于是我们可以把 lastDayi 相同的课程，按照 durationi 顺序排序。优先选择持续天数比较小的课。

```python
class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        def cmp(a: List[int], b: List[int]):
            if a[1] < b[1]:
                return -1
            if a[1] == b[1]:
                if a[0] < b[0]:
                    return -1
                elif a[0] > b[0]:
                    return 1
            return 0

        courses = sorted([c for c in courses if c[0] <= c[1]], key = functools.cmp_to_key(cmp))
        if not courses:
            return 0
        days = 0
        count = 0

        for c in courses:
            if days + c[0] <= c[1]:
                days += c[0]
                count += 1
        return count
```

这是我实现的算法，主体是一个排序。另外，过滤掉 durationi > lastDayi 的不可能数组。这个算法我提交后，97 个用例 过了 80 个。遇到这样一个用例：**[[5,5],[4,6],[2,6]]**，没能通过。

这里我们看到，第一个课，正好把日子用完了，用我的算法再往后，都不能选了。但是这里很凑巧的是，假如我们第一个课不选，正好选后两个课，反而可以多修一门课。

我就意识到了问题，我知道我肯定在一个正确的方向上。只是忽略了一个问题。对于这个没能通过的用例，我们来看看问题在哪里。其实，给出的三门课里，如果我们只选一门课，那么选哪门课更有利呢？显然选持续时间最短的课比较有优势。但是因为我们按照 lastDayi 排序，则我们一定会先遇到 [5,5] 这门课。假如我们已经选了 [5,5] 这门课，那么当我们遇到 [2,6] 这门课，那么如果我们选择把 [5,5] 这门课替换成 [2,6] 这么课，结果是一样的，还是只修一门课，但是后续看到 [4,6] 这门课时候，就会得到不同的答案了。

所以，这里，我们进行这样的优化，还按照刚才的算法，如果我们遇到一门新课，但是总消耗的时间已经超过了，但是新遇到的课比已经选的课消耗时间短，我们就把已经选的课里消耗时间最长的课替换成新遇到的课，这样我们消耗的总时间显然会下降，但是我们选的课的门数却没有变化。这个替换，会优化出更多的空余时间，有可能容纳更多的课程进来。如此，可能得到更优的结果。

我们可以用最大堆来实现这个功能，每次新遇到一门课，如果可以选课，我们就选，如果不能选，就把已经选中的课里，消耗时间最长的课替换成消耗时间更短的课，这样可以在不减少选课数量的同时，空出更多时间来选新课。这样就能得到最终可选的最大课程数。实现如下：

```python
class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        def cmp(a: List[int], b: List[int]):
            if a[1] < b[1]:
                return -1
            if a[1] == b[1]:
                if a[0] < b[0]:
                    return -1
                elif a[0] > b[0]:
                    return 1
            return 0

        courses = sorted([c for c in courses if c[0] <= c[1]], key = functools.cmp_to_key(cmp))
        if not courses:
            return 0
        days = 0
        count = 0
        q = []

        for c in courses:
            if days + c[0] <= c[1]:
                days += c[0]
                count += 1
                heapq.heappush(q, -c[0])
            elif q and -q[0] > c[0]:
                days += q[0] + c[0]
                heapq.heappop(q)
                heapq.heappush(q, -c[0])
        return count
```

以上是我实现的代码，因为 Python 只有最小堆，所以要加个负号不要忘记。

--END--