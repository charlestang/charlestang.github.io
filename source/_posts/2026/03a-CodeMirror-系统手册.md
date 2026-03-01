---
title: CodeMirror 系统导览
permalink: 2026/codemirror-sys-guide/
tags: []
categories:
  - 技术
  - 前端
date: 2025-11-20 01:10:06
updated: 2026-03-01 15:55:20
---
这是 CodeMirror 编辑器的系统导览，它是对系统功能的文字性说明。如果想一项一项看接口的文档，可以查阅参考手册。

<!--more-->

## 架构概览

因为 CodeMirror 的结构与传统的 JavaScript 库（包括它自己的旧版本）有相当大的不同，所以建议在深入使用之前至少阅读本节内容，以免因为预期不符而浪费时间。

### 模块化

CodeMirror 被设计为一组独立的模块，这些模块组合在一起，提供一个功能完备的文本与代码编辑器。好的一面是：这意味着你可以根据需要选择所需的功能模块，甚至可以在有需求时，用自定义实现来替换核心功能。不太好的一面是：要设置一个编辑器，你需要把许多组件拼装在一起。

把这些部分组装起来其实并不困难，但你确实需要安装并导入所需的组件。核心包（缺少它们基本没法构建编辑器）包括：

- **@codemirror/state** —— 定义用于表示 **编辑器状态（Editor State）** 及对其的 **变更（Changes）** 的数据结构。

- **@codemirror/view** —— 一个**显示组件（Display Component）**，负责将编辑器状态展示给用户，并将基本的编辑操作转换成状态更新。

- **@codemirror/commands** —— 提供大量编辑命令，以及一些默认的**快捷键绑定（Key Bindings）**。

下面是一个最小可用的编辑器示例：

```typescript
import {EditorState} from "@codemirror/state"
import {EditorView, keymap} from "@codemirror/view"
import {defaultKeymap} from "@codemirror/commands"

let startState = EditorState.create({
  doc: "Hello World",
  extensions: [keymap.of(defaultKeymap)]
})

let view = new EditorView({
  state: startState,
  parent: document.body
})
```

很多你期望编辑器具备的功能，比如 **行号** 或 **撤销历史**，都是基于核心的扩展机制实现的，因此必须显式添加到配置中才能启用。为方便入门，**codemirror** 包默认引入了大部分你构建基础编辑器所需的功能（但不包括语言支持包）。

```typescript
import {EditorView, basicSetup} from "codemirror"
import {javascript} from "@codemirror/lang-javascript"

let view = new EditorView({
  extensions: [basicSetup, javascript()],
  parent: document.body
})
```

这些软件包是以 ES6 模块的形式发布的。这意味着：在没有某种打包工具（将模块化的程序打包成一个大型 JavaScript 文件）或模块加载器的情况下，目前不能实际直接运行该库。如果你对“打包”还不熟悉，我建议你了解一下 rollup 或 Vite。

### 函数式核心，命令式外壳

指导 CodeMirror 架构设计的一项重要理念是：函数式（纯）代码——用创建新值，而不是修改旧值的方式工作——比命令式代码更容易维护和推理。然而，浏览器的 DOM 本质上是命令式的，CodeMirror 需要与许多强依赖命令式模型的系统集成，这看起来存在矛盾。

为了解决这个矛盾，CodeMirror 的 状态（state）表示完全采用函数式方式：

- 文档（Document）和状态（State）的数据结构都是**不可变**的
- 对这些结构的操作都是**纯函数**（无副作用）
- 相反，视图组件（View Component）和命令接口则把函数式的状态封装成命令式接口供外部使用

这意味着：

- 旧的 state 永远不会被修改，即使编辑器切换到了新的 state
- 在处理状态变化时，同时拥有“旧状态”和“新状态”往往非常有用
- 如果你试图直接修改 state 对象，或命令式地修改扩展（例如 state fields），你想要的效果不会出现，而且可能直接破坏整个系统

TypeScript 接口通过将数组和对象属性标记为 readonly 来明确提醒你这些结构是不可变的。如果你使用的是普通 JavaScript，这可能更容易忘记。但有一个非常重要的通用规则：

> ⚠️ 除非文档明确说明，否则不要修改 CodeMirror 创建的任何对象的属性。

错误用法示例：

```typescript
let state = EditorState.create({doc: "123"})
// ❌ 错误、完全错误的代码 — 不要这样做！
state.doc = Text.of("abc")  // <- 不要这样写
```

### 状态与更新

这个库处理编辑器更新的方式受到了 **Redux** 或 **Elm** 的启发。除了极少数例外（例如输入法组合输入、拖拽处理），**视图的状态完全由其 `state` 属性中的 `EditorState` 决定**。

通过创建一个描述 document，selection 或者 state 的其他字段变化的事务，状态的变化发生在函数式代码里。当你 **dispatch（派发）** 这个事务时，视图就会更新它的状态，并同步 DOM，使其反映最新的编辑器状态。

```typescript
// 假设 view 是一个 EditorView 实例，文档内容是 "123".
let transaction = view.state.update({
  changes: {from: 0, insert: "0"}
})

console.log(transaction.state.doc.toString()) 
// → "0123"

// 此时视图仍然显示旧内容
view.dispatch(transaction)
// 现在视图已经展示新内容了
```

视图会监听事件，比如：文本输入、按键操作，或鼠标交互。然后将这些事件转换为对应的 transaction，并 dispatch 出去，更新编辑器状态，再同步 DOM。

事务当然也可以来自其他地方，但无论事务来自哪里，要真正影响编辑器，都必须 dispatch 到视图。

### 扩展

核心库本身非常 **精简且通用**，大量功能都是通过系统扩展来实现的。扩展可以做各种事情，例如：

* 仅仅配置某些选项
* 在 state 中定义新的状态字段
* 为编辑器添加样式
* 向视图中注入自定义的命令式组件

系统会小心处理扩展之间的组合关系，避免意外冲突。

当前激活的扩展会被存储在 EditorState 中（并且可以通过事务来修改）

扩展可以以以下形式提供给编辑器：

* 一个扩展值（通常从某个包中导入）
* 一个扩展值数组
* 任意层级嵌套的数组（一个数组包含多个数组也是合法的扩展）

扩展在配置过程中会自动去重，因此：如果某个扩展被多个其他扩展间接引用，也不会被重复应用，只会生效一次。

当扩展之间存在冲突时，优先级由两层决定：

1. 显式设置的 precedence 分类（如 `Prec.high(...)`）
2. 在最终扁平化扩展列表中的顺序

示例：

```typescript
import {keymap} from "@codemirror/view"
import {EditorState, Prec} from "@codemirror/state"

function dummyKeymap(tag) {
  return keymap.of([{
    key: "Ctrl-Space",
    run() {
      console.log(tag)
      return true
    }
  }])
}

let state = EditorState.create({
  extensions: [
    dummyKeymap("A"),
    dummyKeymap("B"),
    Prec.high(dummyKeymap("C"))
  ]
})
```

在这个 editor 中按下 Ctrl-Space：

* 尽管 `"C"` 最后出现，但它拥有更高的 precedence，所以它优先执行
* 其次才是 `"A"` 和 `"B"`（按顺序）

本指南的后续部分会进一步介绍各种扩展类型与用法。你也可以参考：配置范例获得与配置和再配置相关的更多的范例代码。

### 文档偏移

CodeMirror 使用**纯数字**来标识文档中的位置。这些数字代表字符计数——更精确地说，是 **UTF-16 code units**：

* 一个普通的 BMP 字符计数为 **1**
* 一个超出 BMP 的字符（如 emoji）计数为 **2**
* 换行符永远计为 **1**（即使你配置了更长的 line separator）

这些位置（offsets）被用于：

* 记录 **selection（选择范围）**
* 定位 **changes（文档变更）**
* **装饰内容**
* 以及其他与文档内容相关的位置操作。

有时候，你需要知道“旧文档中的位置 X”在“应用变更后的文档中变成了哪里”。为此，CodeMirror 提供了：**位置映射（position mapping）机制**，给定一个 **transaction（事务）** 或 **change set**，以及一个旧位置，它能告诉你映射后的新位置。

示例：

```typescript
import {EditorState} from "@codemirror/state"

let state = EditorState.create({doc: "1234"})

// 删除“23”，并在最开始插入 “0”
let tr = state.update({
  changes: [
    {from: 1, to: 3},
    {from: 0, insert: "0"}
  ]
})

// 旧文档中位置 4（即原来的末尾）在新文档中的位置变成 3
console.log(tr.changes.mapPos(4))
```

文档数据结构也支持基于“行号”进行索引，并且这是高效操作，不会遍历全文。

示例：

```javascript
import {Text} from "@codemirror/state"

let doc = Text.of(["line 1", "line 2", "line 3"])

// 获取第 2 行的信息
console.log(doc.line(2)) 
// {from: 7, to: 13, ...}

// 获取包含位置 15 的那一行
console.log(doc.lineAt(15))
// {from: 14, to: 20, ...}
```

返回内容会告诉你：

* 该行在整个文档中的起止 offset（from/to）
* 行文本位置等信息

## 数据模型

作为一个文本编辑器，CodeMirror 将文档视为一个**扁平的字符串（flat string）**。 为了支持文档任意位置的**高效更新**和**高效按行索引**，它将这段字符串按行拆开，并存储为一个**树形结构的 Text 数据结构**（`Text`）。

### 文档变更

文档的**变更**本身也是一个 **值（value）**，由 `ChangeSet` 表示：

* 它精确描述旧文档的哪些范围被替换成了哪些新文本
* 因此扩展可以逐字跟踪文档发生的变化

这使得以下功能可以在扩展中实现，而无需放进核心：

* **撤销/重做（undo history）**
* **协同编辑（collaborative editing）**
* **文档增量分析**
* **语法高亮的局部刷新**

当创建一个 change set 时：

* 所有变更的 `from/to` 坐标都是基于 **原始文档**
* 它们相当于在同一时刻同时发生（逻辑并行）

> 如果你真的需要像“先应用 A 变更，再在变更后的文档上指定 B 的坐标”这种行为，
> 你需要使用 `ChangeSet.compose` 来将多个变更合并。

换句话说：

* **ChangeSet 的坐标永远指向旧文档**
* **state.effects 和 selection 的坐标则指向变更后的新文档**

这是 CodeMirror 数据模型的一个关键规则。

### 选区

除了文档本身，编辑器的 `EditorState` 还会存储一个当前的 **selection（选区）**。

一个选区可以包含 **多个范围（range）**，每个范围可以是：

* 一个 **光标**（即空范围，`empty`）
* 或者一个从 **anchor → head** 的文本区间

示例结构：

```typescript
selection = [
  range(anchor, head),
  range(anchor, head),
  ...
]
```

选区范围具有以下特性：**重叠的范围会自动合并**，范围会按位置 **自动排序**， 因此 `selection.ranges` 始终是一个 **已排序**、**互不重叠**的范围数组。

```typescript
import {EditorState, EditorSelection} from "@codemirror/state"

let state = EditorState.create({
  doc: "hello",
  selection: EditorSelection.create([
    EditorSelection.range(0, 4),   // 选中 "hell"
    EditorSelection.cursor(5)      // 光标在位置 5
  ]),
  extensions: EditorState.allowMultipleSelections.of(true)
})

console.log(state.selection.ranges.length) // 2

// 将所有选区替换为 "!"
let tr = state.update(state.replaceSelection("!"))
console.log(tr.state.doc.toString()) // "!o!"
```

在多个选区中，有一个选区会被标记为 **main（主选区）**：

* 浏览器的 DOM selection 将反映这个主选区
* 其他辅助选区仅由 CodeMirror 绘制与管理，不会进入 DOM selection

默认情况下，一个 state **只允许一个选区范围**。 要启用多选区，需要启用能绘制多选区的扩展（如 `drawSelection`）并且设置选项开启多选。

```javascript
EditorState.allowMultipleSelections.of(true)
```

如果你需要对 **每个选区范围分别执行操作**，可以使用便捷的方法`state.changeByRange`， 示例：

```typescript
import {EditorState, EditorSelection} from "@codemirror/state"

let state = EditorState.create({doc: "abcd", selection: {anchor: 1, head: 3}})

// 将选区内文字转成大写
let tr = state.update(
  state.changeByRange(range => {
    let upper = state.sliceDoc(range.from, range.to).toUpperCase()
    return {
      changes: {from: range.from, to: range.to, insert: upper},
      range: EditorSelection.range(range.from, range.from + upper.length)
    }
  })
)

console.log(tr.state.doc.toString()) // "aBCd"
```

还有一个常用的方法，`replaceSelection`，它可以创建一个事务，把所有选区范围替换成指定文本。

### 配置

每个 editor state 都会持有一个（私有的）配置引用，这个配置由当前启用的扩展决定。在一般的事务（transaction）中，配置不会变化。但你可以通过使用 **compartments** 或 effects 来 **追加** 或 **替换** 当前配置，从而重新配置 state。

配置对一个 state 的直接影响主要体现在两类内容上：

* state 中存储的 **state fields（状态字段）**
* state 上的 **facets（属性面）** 的值

### 属性面（Facets）

Facet（属性面）是一种扩展点。不同的扩展可以向同一个 facet **提供值**（`Facet.of(...)`），任何拥有该 state 和 facet 的代码都可以 **读取**（`state.facet(...)`）由这些输入合成后的输出值。输出可能是提供值的数组，也可能是将它们组合后的某个结果，具体取决于 facet 的定义方式。

Facet 存在的原因是：许多扩展点需要接受来自多个扩展的输入，但最终需要一个统一的结果。不同 facet 的合并方式不同。

* 例如 tab size（缩进宽度）需要一个最终值，因此该 facet 会使用 **具有最高优先级的值** 作为输出。
* 对于事件处理器（event handlers），则需要按优先级顺序收集为一个数组，让系统逐个尝试调用。
* 有时也会需要把输入做逻辑归并，比如 `allowMultipleSelections` 会对输入做逻辑 OR 运算；也可能是取最大值、合并所有过滤器等。

示例：

```typescript
import {EditorState} from "@codemirror/state"

let state = EditorState.create({
  extensions: [
    EditorState.tabSize.of(16),
    EditorState.changeFilter.of(() => true)
  ]
})

console.log(state.facet(EditorState.tabSize))         // 16
console.log(state.facet(EditorState.changeFilter))   // [() => true]
```

Facet 通过 `Facet.define` 创建，返回一个 facet 值。这个值可以 export，也可以保持模块私有（只有当前模块可访问）。后续在“编写扩展”一节会再次提到这一点。

在一个固定配置中，大部分 facet 的值通常都是静态的，直接通过 extension 设置。但 facet 也可以定义为基于其他 state 属性自动重新计算。例如：

```javascript
let info = Facet.define<string>()

let state = EditorState.create({
  doc: "abc\ndef",
  extensions: [
    info.of("hello"),
    info.compute(["doc"], state => `lines: ${state.doc.lines}`)
  ]
})

console.log(state.facet(info))
// → ["hello", "lines: 2"]
```

此类值会在其声明的输入发生变化时自动重新计算。

Facet 只有在必要时才会重新计算，因此你可以通过比较对象 identity（引用是否变化）来高效判断某个 facet 是否发生了改变。

### 事务（Transaction）

通过状态的 update 方法创建的事务，可以组合多种效果（这些效果都是可选的）：

- 它们可以应用文档更改。
- 它们可以显式移动选区。注意，如果存在文档更改，但没有显式指定新的选区，那么选区会根据这些更改被隐式映射。
- 它们可以设置一个标志，指示视图将（主）选区头部滚动到可见区域。
- 它们可以包含任意数量的注解（annotation），用于存储描述该（整个）事务的附加元数据。例如，userEvent 注解可用于识别由某些常见操作（如输入或粘贴）生成的事务。
 - 它们可以包含效果（effects），即一些自包含的附加作用，通常用于影响某个扩展的状态（例如折叠代码或启动自动补全）。
 - 它们可以影响状态的配置：要么提供一整套全新的扩展，要么替换配置中的特定部分。

事务通过 spec 来描述，通常写成对象字面量的形式，不过某些方法（如 changeByRange）也会返回这样的 spec。这些 spec 可以直接传给 EditorView.dispatch，以创建并立即分发一个事务；也可以传给 EditorState.update，仅创建事务而不立即分发。

当向这些方法传入多个 spec 时，它们会被合并为一个单独的事务。这在某些场景下很有用，比如你想在某个辅助函数生成的 spec 基础上，再补充一些额外字段。

更改通过形如 {from, to, insert} 的对象来描述（其中 to 和 insert 是可选的），也可以是这些对象组成的嵌套数组。你也可以传入一个 ChangeSet 对象，这是事务对象中表示这些更改的最终形式。即使存在多个更改，所提供的更改位置也都是基于事务开始时的文档。

新选区或状态效果中使用的位置，则是基于更改后的新文档。

如果要完全重置一个状态——例如加载一个新文档——建议创建一个新的状态，而不是通过事务来实现。这样可以确保不会残留不需要的状态信息（例如撤销历史记录事件）。

## 视图

视图层会尽量作为状态（state）之外的一层透明封装。不幸的是，编辑器的一些工作内容无法仅靠 state 中的数据来纯粹处理。

 - 当需要处理屏幕坐标时（例如确定用户点击了哪里，或者获取某个文档位置对应的屏幕坐标），你就必须访问布局信息，也就需要访问浏览器的 DOM。
- 编辑器会从周围的文档中获取文本方向（如果被覆盖，则使用它自身的 CSS 样式）。
- 光标移动可能依赖于布局和文本方向。因此，视图提供了若干辅助方法，用来计算不同类型的移动。
- 有些状态，例如焦点（focus）和滚动位置（scroll position），不会存储在函数式 state 中，而是留在 DOM 里。

该库并不期望用户代码去操作它所管理的 DOM 结构。当你尝试这么做时，你很可能会看到库马上把你的改动还原回去。要正确影响内容的显示方式，请参见关于 decorations（装饰）的章节。

### Viewport

需要注意的一点是，当文档较大时，CodeMirror 并不会渲染整个文档。为了保持编辑器的响应速度并降低资源消耗，它在更新时会检测当前哪些内容是可见的（没有滚动出视图的部分），只渲染这些内容以及其周围的一小段边距区域。这被称为 viewport（可视区域）。

对于当前 viewport 之外的位置，查询其屏幕坐标是不可行的（因为它们没有被渲染，因此也就没有布局信息）。不过，视图仍会为整个文档跟踪高度信息（最初为估算值，在内容真正绘制时会进行精确测量），包括 viewport 之外的部分。

未换行的长行或被折叠的大块代码仍然可能使 viewport 变得相当庞大。编辑器还提供一个 visible ranges 列表，其中不会包含这些不可见的内容。例如在做代码高亮时，这会很有用，因为你不希望为当前不可见的文本做无意义的处理。

### 更新循环（Update Cycle）

CodeMirror 的视图层会尽力将其引发的 DOM 重排（reflow）次数降到最低。派发一个事务通常只会导致编辑器向 DOM 写入内容，而不会读取布局信息。读取操作（例如检查 viewport 是否仍然有效、是否需要将光标滚动到可见区域等）会在一个单独的测量阶段中完成，该阶段通过 requestAnimationFrame 进行调度。如有必要，这个阶段之后还会再跟随一个写入阶段。

你也可以使用 requestMeasure 方法来调度你自己的测量代码。

为了避免奇怪的重入（reentrancy）情况，当一个更新正在被同步应用的过程中，如果又发起新的更新，视图会抛出错误。而在测量阶段尚未完成时应用多个更新则不会有问题——这些更新的测量阶段会被合并执行。

当你不再需要某个视图实例时，必须调用它的 destroy 方法来销毁它，释放其分配的所有资源（例如全局事件处理器和 mutation observer）。

### DOM 结构

编辑器的 DOM 结构大致如下所示：

```html
<div class="cm-editor [theme scope classes]">
  <div class="cm-scroller">
    <div class="cm-content" contenteditable="true">
      <div class="cm-line">Content goes here</div>
      <div class="cm-line">...</div>
    </div>
  </div>
</div>
```

最外层（包裹）元素是一个纵向的 flexbox。诸如面板（panels）和提示框（tooltips）之类的元素可以由扩展添加到这里。

其内部是 scroller 元素。如果编辑器拥有自己的滚动条，那么这个元素应当设置 overflow: auto 样式。但这不是必须的——编辑器也支持随着内容增长而扩展，或者增长到某个最大高度后再开始滚动。

scroller 是一个横向的 flexbox 元素。当存在 gutter（行号栏等）时，它们会被添加到其起始位置。

在其内部是 content 元素，它是可编辑的。该元素上注册了一个 DOM mutation observer，任何在其中发生的变更都会被编辑器解析为文档变更，并重新绘制受影响的节点。这个容器为 viewport 中的每一行保留一个行元素，这些行元素再包含文档文本（可能附带样式或小部件装饰）。

### 样式和皮肤

为了管理与编辑器相关的样式，CodeMirror 使用一个系统从 JavaScript 中注入样式。样式可以通过 facet 注册，这会使视图确保这些样式可用。

编辑器中的许多元素都会被分配以 cm- 开头的类名。这些类可以直接在你自己的 CSS 中进行样式设置。但它们也可以通过主题（theme）来定制。主题是通过 EditorView.theme 创建的一种扩展。它会生成一个独有的（自动生成的）CSS 类（当该主题扩展激活时，这个类会被添加到编辑器上），并基于该类定义作用域内的样式规则。

一个主题声明可以使用 style-mod 语法定义任意数量的 CSS 规则。下面这段代码创建了一个简单的主题，将编辑器中的默认文本颜色设为橙色：

```typescript
import {EditorView} from "@codemirror/view"

let view = new EditorView({
  extensions: EditorView.theme({
    ".cm-content": {color: "darkorange"},
    "&.cm-focused .cm-content": {color: "orange"}
  })
})
```

为了使自动类名前缀机制正确工作，当规则的第一个选择器目标是编辑器的包裹元素（也就是主题的唯一类会被添加到的那个元素）时，例如示例中的 .cm-focused 规则，必须使用 & 字符来指示包裹元素所在的位置。

扩展也可以定义 base themes（基础主题），为它们创建的元素提供默认样式。基础主题可以使用 &light（默认）和 &dark（当启用深色主题时生效）占位符，这样即使没有被具体主题覆盖，它们看起来也不会显得不协调。

```typescript
import {EditorView} from "@codemirror/view"

// 这同样会产生一个扩展值
let myBaseTheme = EditorView.baseTheme({
  "&dark .cm-mySelector": { background: "dimgrey" },
  "&light .cm-mySelector": { background: "ghostwhite" }
})
```

当在常规 CSS 中定义编辑器样式时，你必须考虑到注入样式规则中额外添加的前缀类选择器，否则你的样式优先级将始终较低。推荐的做法是在你的规则中包含 .cm-editor，这样它会处于与注入样式相同的位置，并具有相同的优先级。

```css
.cm-editor .cm-content { color: purple; }
```

### 命令（Commands）

命令（Commands）是具有特定签名的函数：(view: EditorView) => boolean。它们的主要用途是作为键绑定（key bindings），但也可以用于菜单项或命令面板等场景。一个命令函数代表一次用户操作。它接收一个 view，并返回一个布尔值：返回 false 表示当前情况下不适用，返回 true 表示成功执行。命令的效果通常通过命令式方式产生，通常是通过派发（dispatch）一个事务来实现。

当多个命令被绑定到同一个按键时，它们会按照优先级顺序依次尝试执行，直到有一个返回 true 为止。

只作用于 state 而不依赖整个 view 的命令，可以使用 StateCommand 类型。它是 Command 的一个子类型，只要求参数对象具备 state 和 dispatch 属性。这在测试此类命令时特别有用，因为无需创建完整的 view。

@codemirror/commands 包导出了大量不同的编辑命令，以及一些 keymap。Keymap 是由 KeyBinding 对象组成的数组，通过提供给 keymap facet 来在编辑器中启用。

```typescript
let myKeyExtension = keymap.of([
  {
    key: "Alt-c",
    run: view => {
      view.dispatch(view.state.replaceSelection("?"))
      return true
    }
  }
])
```

## 扩展 CodeMirror

扩展 CodeMirror 有多种不同方式，而在具体场景下选择哪一种方式并不总是显而易见。本节将介绍编写编辑器扩展时需要熟悉的各种概念。

### 状态字段（State Field）

扩展通常需要在 state 中存储额外的信息。例如，撤销历史需要存储可撤销的变更，代码折叠扩展需要跟踪哪些内容已被折叠，等等。

为此，扩展可以定义额外的 state fields。State field 存在于纯函数式的 state 数据结构内部，因此必须存储不可变的值。

State field 通过类似 reducer 的机制与整体 state 保持同步。每当 state 更新时，都会调用一个函数，传入该字段的当前值以及事务对象，然后返回字段的新值。

```typescript
import {EditorState, StateField} from "@codemirror/state"

let countDocChanges = StateField.define({
  create() { return 0 },
  update(value, tr) { return tr.docChanged ? value + 1 : value }
})

let state = EditorState.create({extensions: countDocChanges})
state = state.update({changes: {from: 0, insert: "."}}).state
console.log(state.field(countDocChanges)) // 1
```

你通常会希望使用 annotations 或 effects 来向你的 state field 传达发生了什么。

```typescript
import {StateField, StateEffect} from "@codemirror/state"

let setFullScreenMode = StateEffect.define<boolean>()

let fullScreenMode = StateField.define({
  create() { return false },
  update(value, tr) {
    for (let e of tr.effects)
      if (e.is(setFullScreenMode)) value = e.value
    return value
  }
})
```

你可能会想避免将状态放入真正的 state field——声明一个字段确实有些冗长，而且每次状态变化都需要发起一个完整事务，看起来有些“重量级”。但在几乎所有情况下，将你的状态纳入编辑器整体的 state 更新周期都是一个非常好的做法，因为这样可以更容易地让它与编辑器的其他状态保持同步。

### 影响视图

View 插件为扩展提供了一种在视图内部运行命令式组件的方式。这对于处理事件、添加和管理 DOM 元素，以及执行依赖当前 viewport 的操作非常有用。

下面这个简单的插件会在编辑器角落显示当前文档的大小：

```typescript
import {ViewPlugin} from "@codemirror/view"

const docSizePlugin = ViewPlugin.fromClass(class {
  constructor(view) {
    this.dom = view.dom.appendChild(document.createElement("div"))
    this.dom.style.cssText =
      "position: absolute; inset-block-start: 2px; inset-inline-end: 5px"
    this.dom.textContent = view.state.doc.length
  }

  update(update) {
    if (update.docChanged)
      this.dom.textContent = update.state.doc.length
  }

  destroy() { this.dom.remove() }
})
```

View 插件通常不应持有（非派生的）状态。它们最适合作为编辑器 state 中数据的浅层视图。

当 state 被重新配置时，不在新配置中的 view 插件会被销毁（因此，如果它们对编辑器做过修改，应当定义 destroy 方法来撤销这些修改）。

当某个 view 插件发生崩溃时，它会被自动禁用，以避免影响整个视图。

### 装饰文档

在没有特别说明的情况下，CodeMirror 会将文档绘制为纯文本。Decorations（装饰）是扩展用来影响文档显示方式的机制。它们分为四种类型：

 - Mark decorations 会为指定范围内的文本添加样式或 DOM 属性。

 - Widget decorations 会在文档中的某个位置插入一个 DOM 元素。

 - Replace decorations 会隐藏文档的一部分，或用指定的 DOM 节点替换它。

 - Line decorations 可以为某一行的包裹元素添加属性。

Decorations 通过一个 facet 提供。每当视图更新时，该 facet 的内容都会被用来为可见内容添加样式。

Decorations 存储在集合（sets）中，这同样是不可变的数据结构。这样的集合可以在文档变更后进行映射（调整其中内容的位置以适应变更），也可以在更新时重新构建，具体取决于使用场景。

提供 decorations 有两种方式：直接方式是将 range set 值放入 facet（通常由某个 state field 派生而来）；间接方式是提供一个从 view 到 range set 的函数。

只有直接提供的 decoration 集合才能影响编辑器的垂直块结构；而只有间接提供的 decoration 才能读取编辑器的 viewport（例如，当你只想为可见内容添加装饰时，这会很有用）。之所以有这样的限制，是因为 viewport 是根据块结构计算出来的，因此必须先确定块结构，才能读取 viewport。

文档中提供了一个 decoration 示例，演示了一些常见的使用场景。

### 扩展架构

要实现某个编辑器功能，通常需要组合多种不同类型的扩展：一个 state field 用于保存状态，一个 base theme 提供样式，一个 view 插件负责输入输出处理，一些命令，也可能还需要一个 facet 用于配置。

一种常见模式是导出一个函数，该函数返回实现该功能所需的扩展值。即使这个函数暂时不接收参数，也建议写成函数形式——这样将来可以添加配置选项，而不会破坏向后兼容性。

由于扩展可以引入其他扩展，因此有必要考虑当你的扩展被多次包含时会发生什么。对于某些类型的扩展，例如 keymap，多次执行其逻辑是合理的。但在很多情况下，这样做可能是浪费的，甚至会导致问题。

通常可以依赖相同扩展值的去重机制，使多次使用某个扩展时仍然表现正确——如果你确保静态扩展值（例如 theme、state field、view 插件等）只创建一次，并且在扩展构造函数中始终返回同一个实例，那么编辑器中只会保留它们的一份副本。

但当你的扩展支持配置时，其他逻辑往往需要访问这些配置。如果扩展的不同实例使用了不同的配置，该怎么办？

有时这本身就是错误。但在很多情况下，可以定义一种协调策略来处理这种情况。Facet 在这里非常适合使用。你可以将配置放入一个模块私有的 facet 中，并通过它的合并函数来协调不同配置，或者在无法协调时抛出错误。然后，其他需要访问当前配置的代码可以读取这个 facet。

可以参考 zebra stripes 示例，了解这种做法的具体实现方式。
