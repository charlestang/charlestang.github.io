---
title: 用好 Python 数据结构解题《347. 前 K 个高频元素》
tags:
  - algorithm
  - python
id: '1062'
categories:
  - 算　　法
date: 2021-05-18 18:07:00
permalink: python-347-most-frequent-k/
---

这道题目意思很简单，给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。本质上就是求，出现频次最高的数组元素，这在日常工作中也很常见。题目见[传送门](https://leetcode-cn.com/problems/top-k-frequent-elements/)。

这道题，很有意思，也很无聊。很有意思是说，如果不让用类库的话，那么涉及到几种基础的数据结构和算法。如果让用类库的话，那么写起来也没什么难的，前提是你对类库足够熟悉的话，60 秒内绝对可以写出来。问题是，你不熟！

解题思路的话是这样的，首先，咱们必须统计出每个元素的出现频率。这里用到的数据结构是哈希表，通过哈希表，我们可以反复在 O(1) 时间内检索一个值。以数组元素作 key，元素的出现频率作 value，用 O(n) 的时间，可以完成对每个元素出现频率的统计。

然后，第二个步骤，方法就比较多了，如何找到频率最高的前 k 个元素呢？因为第一步有了哈希表，我们会有一些 <num, frequency> 的数值对，显然，要找到频次最高的前 k 个元素，最显然的办法，就是按照 frequency 进行排序，降序。然后取前 k 个 num 即可。

第二个方法，我们知道，可以使用到一个数据结构叫堆。我们可以构造一个最小堆，堆的大小是 k，然后，我们把数值对往堆里插，堆满了以后，堆顶就是到目前位置频次最低的元素。如果出现一个比堆顶频次大的元素，我们就把堆顶元素给换掉，最后我们就会得到频次最高的前 k 个元素。

第三个方法，我们可以用快速排序的 partition 方法，快速排序的原理是，找到一个分割点，然后把小于分割点的数字移到分割点前面，把大于分割点的数字移到分割点后面，最后计算出分割点的位置 k，这个就是第 k 大的元素。那么显然，分割点及以前的元素，就是前 k 个（降序原理相同）。

上面三个算法都很基础，都可以经常写写以保持手熟，其实建堆也好，partition 也好，都不是很好写的，知道原理很简单，写起来很不容易写对。

这篇文章想谈谈，用 Python 的类库怎么写，像我刚认真研究 Python 没几个月，就极其不熟练，基本可以说，离开了文档，我就寸步难行，很多基本的 API 都背不出来。就很惭愧。

我们显然可以用最基础的 dict 来统计元素的频次：

```python
d = {}
for n in nums:
    if not d.get(n, False):
        d[n] = 1
    else:
        d[n] += 1
```

这个基础的 dict 的问题是，一开始，字典是空的，没有初始化，所以，每次操作，总要判断字典是否包含当前元素。这就给写代码带来很大的麻烦，如果字典可以初始化好，get 的时候，没有 key 就返回 0，有 key 就返回对应的值就好了。

其实，Python 里给我们提供了一个现成的数据结构，就叫 Counter。

```python
import collections
freq = collections.Counter()
for n in nums:
    freq[n] += 1
```

大家看到，这个数据结构在使用的时候就方便多了。其实，还可以更方便，就是 `freq = collections.Counter(nums)` ，没错，在构造函数里直接搞定。那统计这个步骤就会非常简洁。

第二个步骤，排序，怎么做呢？其实这里有很多的写法。

```python
res = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:k]
return [x[0] for x in res]
```

我们提取哈希表的键值对为一个 list，然后外面用 sorted 进行排序，然后截取前 k 个，最后提取键生成了结果。

其实字典作为 iterateble 类型，本来就可以直接排序，但是，默认情况下，排序一个字典，返回的时候 key 的列表。而且是按照 key 值进行排序的。怎么写才能按照 value 排序呢？

```python
res = sorted(freq, key=freq.get, reverse=True)[:k]
return res
```

于是，这么写比上面又简洁了点。我们直接用字典的值倒序排，然后返回字典的键列表，等于一行答案就出来了。

假如，你想用堆来解决问题，那就不得不用到 heapq 这个包。但是这个包一般的几个 API，heapify 也好，heappop，heappush，都是只接受一个值 item 和一个值的列表。对于这个场景来说，我们要操作的是 <num, frequency> 的数值对，就很麻烦，因为数值对有其默认的比较规则，这比较规则还不符合我们的需要，还要进行一些处理。

```python
import heapq
h = []
l = [(v, k) for k, v in freq.items()]
for ele in l:
    if len(h) < k:
        heapq.heappush(h, ele)
    else:
        if ele[0] > h[0][0]:
            heapq.heappop(h)
            heapq.heappush(h, ele)
return [x[1] for x in h]
```

这里进行了多少种 trick 处理呢？

1.  将<键, 值> 对颠倒过来，因为这个 tuple 在 Python 里是按照前后顺序先后比较排序的；
2.  这里我们只用了 push 和 pop 两种 API，正好用的是最小堆，如果要用最大堆，在 Python 里是没有的，只能给值加 负号。如果我们要用 heapify 对堆进行整理，就要在 v 上加负号。

其实，在 heapq 里有更简单的 API，就是 nlargest：

```python
import operator
heapq.nlargest(k, freq.items(), key=operator.itemgetter(1))
```

其实 heapq，直接就可以求前 K 大元素。这里的 key，我用了 operator.itemgetter 的这个高阶函数，当然，大家知道，这里可以写 lambda 算子的 `lambda x: x[1]` 。这样，我们就算用堆，也可以写得很简洁。

最后，我们回过头去看一眼 Counter 的，其实 Counter 有个 API，是 most_common(k)，那更简单：

```python
return [x[0] for x in collections.Counter(nums).most_common(k)]
```

最后，变成了一行流，用 Counter 以及 most_common 接口，配合列表生成式，直接搞定了。

这就是为什么，人生苦短，我用 Python！其实，这个东西这么写法，这么多等价用法，难道没违背 Python 之禅么？