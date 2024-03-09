# 个人技术博客

博客地址：https://blog.charlestang.org

This is a technology blog built on Hexo. Below are some operational instructions about this blog system.

When update:

```shell
# update npm globally
npm install -g npm@10.5.0
# update hexo-cli globally
npm install -g hexo-cli
```

Sometimes when executing hexo commands, there may be inexplicable error messages that cannot be resolved, 
which may be due to the fact that hexo-cli has not been updated. Therefore, the above command is executed 
to update the hexo-cli global package.

When a build error occurs, try executing the `hexo clean` command, then delete the `node_modules` 
directory, re-execute `npm install`, and then execute the `hexo g` command to rebuild.

This blog uses a famous theme called 'next' and references it using git submodules. When you need to 
update the theme, execute the `git pull --rebase` command in the theme's subdirectory.

```shell
# list installed node packages.
npm list
```

## Themes

本博客采用 [NexT][hexo-theme-next] 作为皮肤，使用 Git 的 submodule 整合到整个系统里：

```shell
cd themes/next
git fetch
git checkout v8.19.2
```

以上命令切换了皮肤的版本到最新的 v8.19.2。

[hexo-theme-next]: https://github.com/next-theme/hexo-theme-next


