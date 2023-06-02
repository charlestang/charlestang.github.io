---
title: 【Python】 时间计算
tags:
  - code examples
  - python
id: '525'
categories:
  -   - 工作相关
date: 2012-12-08 15:31:28
permalink: python-date-time/
---

说实在的不喜欢Python，这主要是相对于PHP而言的，Python在Web相关领域里面，缺少了PHP的丰厚家学和积淀，但是有时候没有办法，还是得学一点的。在PHP里，用惯了strtotime这种神奇函数，在Python里面，到底该如何处理时间呢？
<!-- more -->
```python

from datetime import date
from datetime import datetime
from datetime import timedelta

today = date.today()
print today  
#2012-12-08

now = datetime.today()
print now 
#2012-12-08 14:13:28.298156

last_monday = today - timedelta(days=today.weekday())
print last_monday
#2012-12-03

next_monday = today + timedelta(days=-today.weekday(), weeks=1)
print next_monday
#2012-12-10

last_month_end = date(today.year, today.month, 1) - timedelta(days=1)
last_month_start = date(last_month_end.year, last_month_end.month, 1)
print last_month_end
#2012-11-30
print last_month_start
#2012-11-01

```