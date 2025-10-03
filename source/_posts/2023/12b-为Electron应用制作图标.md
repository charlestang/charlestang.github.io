---
title: 为 Electron 应用制作图标
permalink: 2023/howto-change-app-icon-for-electron-app/
categories:
  - - 技术
    - 移动端
tags:
  - electron
date: 2023-12-07 10:26:21
updated: 2024-05-06 14:11:37
---
最近在开发博客本地客户端 HexoPress，应用做好后，需要打包，如果不希望打包出来 App 的图标用的是 Electron 默认的星球环绕的图标，那么需要自己制作图标。

<!--more-->

## 制作图标

首先，你需要给各种操作系统制作一个满足要求的图标，根据文档的指引，我建议你直接制作一个 1024 像素见方的 png 图片，作为底稿即可。以此为基础，可以创建适用于 Windows，Mac，Linux 三种系统的图标。这三个系统要求的图标格式各不相同，制作方法也各不相同。

| 系统    | 扩展名 | 尺寸    |
| ------- | ------ | ------- |
| Windows | ico    | 256x256 |
| Mac     | icns   | 512x512 |
| Linux   | png    | 512x512 |

以上只是表面上的尺寸，实际，苹果的图标制作是最麻烦的。苹果因为要适配不同分辨率的屏幕，以及各种不同的显示器，需要一个图标的集合，叫 iconset。

### 苹果 MacOS

如果你像我一样安装过 XCode，那么你会发现，命令行有两个命令 `sips` 和 `iconutil` 这两个正是用来制作图标的工具。

首先是使用 `sips` 命令，将图片转换成多种格式。

```shell
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
cp icon.png iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset
```

将你准备的图标底稿，命名为 icon.png 放在一个目录里，然后建立一个图标目录叫， icon.iconset，然后使用 `sips` 命令将图片格式化成上述各种尺寸，然后输出到 icon.iconset 文件夹。

这个文件夹也是一个苹果系统可以认可的图标格式。可以用 `iconutil` 转换成另一种格式，也就是 icns。上图的最后一个命令做这个。

然后我们就得到了苹果系统的图标。

### Linux 系统

Linux 相对比较简单，只要一个普通 png 即可。从刚才生成的图片中，挑出 256px 的图片，然后重命名成 icon.png，即可。

### Windows 系统

Window 需要的 `ico` 格式，需要专门的工具进行制作，这里推荐网上能直接访问的在线工具。比如：[https://redketchup.io/icon-converter](https://redketchup.io/icon-converter)，将之前准备好的底稿上传，然后，调整好参数，直接 Download，就得到了 256px 的 `ico` 格式图标。

## 配置 electron-forge

Electron 应用的打包方法现在官方主推的是 Electron Forge，另外的 Electron Builder 也很好用，不过我就用官方的了。

制作好的图标，放到一个目录下，文件名相同，扩展名不同，这样打包的时候，forge 会自动选择目标系统合适的图标。
