---
title: Electron + Vue 开发的时候，在 App 里加载 DevTools
permalink: 2024/electron-vue-load-devtools/
categories:
  - - 工作相关
    - Vue
tags:
  - electron
  - usage
  - vue
date: 2024-02-06 16:42:55
updated: 2024-02-07 16:13:27
---
使用 Electron 开发的时候，因为其原理是 Node.js + Chrome 内核，所以在 Chrome 能用的开发工具，在 Electron 开发的时候也可以用，这就带来了很好的开发体验。

这是一个巨大的优势，可以抵销很多 electron 平台的劣势。

<!--more-->

在 Electron 窗体里，怎么激活开发工具呢？

```js
function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 900,
    titleBarStyle: 'hidden',
    webPreferences: {
      preload: join(__dirname, 'preload.js')
    }
  })

  win.loadFile('dist/index.html')
}
```

以上代码是 main.js 的一个片段，创建了一个窗体实例，然后加载了 index.html 网页。

加载 DevTools 很简单，只要调用 win 的句柄，然后启动开发工具即可。

```js
function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 900,
    titleBarStyle: 'hidden',
    webPreferences: {
      preload: join(__dirname, 'preload.js')
    }
  })

  win.loadFile('dist/index.html')
  win.webContents.openDevTools() //加载开发工具
}
```

我们知道，Vue 开发的时候，是可以实现热更新的，那么在 Electron 开发的时候，也可以实现这一点，只要，我们在 win 句柄加载的时候，选择本地站点的动态网址即可。比如，我们可以将代码：

```js
win.loadFile('dist/index.html')
```

改成这样：

```js
win.loadURL('http://localhost:5173/Users/charles/Projects/HexoPress/dist')
```

当然，这里还有一点小技巧，就是我们要让 Vue 启动后，再让 Electron 也启动，然后 Electron 加载动态的 Vue 网页，就可以了。打开 package.json 在 scripts 区段，增加：

```json
//......
"scripts": {
    "electron:run": "NODE_ENV=dev concurrently -k \"npm run dev\" \"npm run electron:dev\"",
    //......
}
//......
```

这里用到了一个 dev 包就是 `concurrently`，就是并发启动的功能。上面的意思就是，先执行 `npm run dev`，这样就会启动 Vue 的调试模式，然后我们可以得到 Vue 的动态运行网站。

然后启动 electron 的实例。通过上面介绍的 `win.loadURL` 的方法，加载 Vue 的动态地址即可。

上面代码里还有一个 `NODE_ENV` 的设定，就是区分开发环境和线上环境的作用，整合起来就是：

```js
function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 900,
    titleBarStyle: 'hidden',
    webPreferences: {
      preload: join(__dirname, 'preload.js')
    }
  })

  if (process.env.NODE_ENV === 'dev') {
    win.loadURL('http://localhost:5173/Users/charles/Projects/HexoPress/dist')
    win.webContents.openDevTools()
  } else {
    win.loadFile('dist/index.html')
  }
}
```

既然已经打开了 Chrome 的开发工具，我们还可以更近一步，可以给 DevTools 安装扩展，比如，我们使用 Vue 开发，可以增加 DevTools 的 Vue 扩展，这样调试更加方便。

我这里介绍一个手动安装扩展的方法，也有利用包来实现的，我懒得安装了。包名叫 electron-devtools-installer 大家自己搜索学习一下即可。

手动怎么安装呢？首先你要安装在自己的 Chrome 上，这样，扩展就会被下载到磁盘，然后找到这个扩展的路径，用代码指令加载即可。

1. 首先打开 Chrome 浏览器，访问 `chrome://extensions` 网址，在扩展里找到 Vue；
2. 查出来 Vue 的 ID 是 nhdogjmejiglipccpnnnanhbledajbpd；
3. 然后去到 Chrome 保存扩展的路径，比如，在 Mac 上是 `~/Library/Application Support/Google/Chrome`;
4. 在这个路径下搜索刚才的 ID，官网不是这样么写的，不过我发现官网说的路径，对我来说并不正确，说明在不同的电脑上，根据用户登录的 Google 账号数量，目录布局有所不同，最简单还是暴力搜索比较容易找到扩展路径；
5. 最后，在 main.js 里的 `app.whenReady()` 钩子里，调用：

```js
  if (process.env.NODE_ENV === 'dev') {
    const vueDevToolsPath = join(homedir() , '/Library/Application Support/Google/Chrome/Profile 1/Extensions/nhdogjmejiglipccpnnnanhbledajbpd/6.5.1_0')
    await session.defaultSession.loadExtension(vueDevToolsPath)
  }
```

上面代码里的路径是我的电脑上的实际路径，注意最后的版本号。同样用环境变量条件引入一下，这样在生产环境不会引入这个。

注意，值得一提的是，electron 毕竟还不是完整的 Chrome，所以并不是支持所有的扩展加载，只支持那些只使用 `Chrome.*` API的扩展，我们常用的 react，vue，jquery，backbone 等扩展都是支持的，但并不是任意的。参见[官方文档](https://www.electronjs.org/zh/docs/latest/tutorial/devtools-extension)。

注意2，我在实际开发的过程中，发现一个很奇怪的现象：

```js
const setupAll = async () => {

  const app = createApp(App)

  await setupI18n(app)

  setupRouter(app)

  setupStore(app)

  app.mount('#app')

}
```
注意上面的各种模块的引入顺序，这个竟然是重要的，一开始我先引入 setupStore 然后是 setupRouter，结果我的 DevTools 里，只有跟组件有关的 Tab，没有 I18n，Routes 和 Pinia，然后我调整了引入顺序，把 setupStore 调整到最后，发现 DevTools 的各个 tab 都正常了。这个原因是不知道的，不过这么用体验更好。[参见](https://github.com/vuejs/devtools/issues/1839)

总结，在 Electron 开发的时候，可以启动 DevTools 并且也可以安装扩展，大幅提升开发体验。

-- End --
