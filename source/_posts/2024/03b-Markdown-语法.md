---
title: Markdown 语法
permalink: 2024/markdown-syntax/
categories:
  - - 工作相关
tags:
  - markdown
  - syntax
date: 2024-03-10 11:02:00
updated: 2024-03-10 14:59:35
---

记录一些怎么也记不住写法的 Markdown 语法。

<!--more-->

## 链接

### 基础

```markdown
[链接文字](https://blog.charlestang.org)
```

效果

[Becomin' Charles](https://blog.charlestang.org)


## 表格

### 基础
```markdown
| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
```

效果

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |

### 对齐

```markdown
| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |
```

效果

| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |
