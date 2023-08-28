# Personal Blog built on Hexo

This is a technology blog built on Hexo. Below are some operational instructions about this blog system.

When update:

```shell
# update npm globally
npm install -g npm@9.8.1
# update hexo-cli globally
npm install -g hexo-cli
```
Sometimes when executing hexo commands, there may be inexplicable error messages that cannot be resolved, which may be due to the fact that hexo-cli has not been updated. Therefore, the above command is executed to update the hexo-cli global package.

When a build error occurs, try executing the `hexo clean` command, then delete the `node_modules` directory, re-execute `npm install`, and then execute the `hexo g` command to rebuild.

This blog uses a famous theme called 'next' and references it using git submodules. When you need to update the theme, execute the `git pull --rebase` command in the theme's subdirectory.

```shell
# list installed node packages.
npm list
```


