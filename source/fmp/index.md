---
title: FMP
id: '363'
tags: []
categories:
  - - uncategorized
date: 2010-02-19 20:12:00
---

## Flash MP3 Player

This plugin integrates a powerful music player into WordPress. 

## Features

*   simple to install
*   customizable background
*   playlist include a shuffle feature
*   you can add an album artwork
*   easy to configurate
*   multiple playlists and configuration files
*   sidebar supported
*   you can include it in posts and pages

## Download

[download page](http://wordpress.org/extend/plugins/flash-mp3-player/download/)

## Donate

![](https://www.paypal.com/zh_XC/i/scr/pixel.gif)

## Installation

1.  Upload the directory flash-mp3-player to the `/wp-content/plugins` directory.
2.  Activate the plugin through the `Plugins` menu in WordPress.
3.  Use `Settings/FMP:Config Editor` to create config files.
4.  Use `Settings/FMP:Playlist Editor` to create playlist files.
5.  Add a widget to your sidebar through the `Appearance-->Widgets` menu in WordPress.

## Usage

You can display the mp3 player in several place in your blog:

1.  on your sidebar
2.  in your post or page
3.  other place

### How to put it on your sidebar

[![](http://lh4.ggpht.com/_QYicOeu89Bk/S4ONy8Wd7kI/AAAAAAAAB1Y/VuC2Qk4pHkw/s400/Add-sidebar-widget.png)](http://picasaweb.google.com/lh/photo/JtyQZ107v27_JFpsuwaw_w?feat=embedwebsite)

How to add a sidebar widget. From [illustration](http://picasaweb.google.com/TangChao.ZJU/Illustration?feat=embedwebsite)

1.  Create a configuration for a sidebar widget, for example called "sidebar widget style 1". You can use the `Settings--> FMP:Config Editor` to do this, and it will create a XML config file called sidebar-widget-style-1.xml in your configuration list.
2.  Create a playlist, for example called "playlist in homepage sidebar". You can use the `Settings-->FMP:Playlist Editor` to do this, and it will create a XML playlist called playlist-in-homepage-sidebar.xml in your playlists list.
3.  Go to `Appearance --> Widgets` and drag a "Flash MP3 Player JW" to your sidebar. Then you should set the title, width and height of the widget, choose the config file sidebar-widget-style-1.xml and playlist playlist-in-homepage-sidebar.xml, click save, done!
4.  You can create a lot of different config files and playlists and add a player to every sidebar (if you have more than one), each one with a different config and playlist.

### How to embed it in your post or page

1.  Just like what you do in "put it on your sidebar"
2.  Just like what you do in "put it on your sidebar"
3.  Add a new post. Click the media button, which is a blue "Play" button, to call the wizard panel.
4.  You can either choose config file and playlist or not. If not, just set a single song's url. Click insert button and the short code to call the player will be inserted to your post.

### How to put it in other place of your blog

To put the player in other place of your blog is not so easy as above. You should know something about [template tags of WordPress](http://codex.wordpress.org/Template_tags).

The code to call the player is like this:

```php

$args = array(
  //the entire url of the config file, must
  'config_url' => '', 
  //the entire url of the playlist file (optional)
  'playlist_url' => '', 
  'width' => 230,
  'height' => 350,
  'id' => '',
  'class' => '',
  'transparent' => true,  //this is default
  'autostart' => false,  //this is default
  'file' => '' //the entire url of the MP3 file (optional)
);
//you should set either "playlist_url" or "file"
fmp_tag_print_player($args);

```

### How to backup your playlist files

Now you have just one method to backup your playlist file is to use ftp connect to your server, and download the `/wp-content/fmp-jw-files/playlists` directory. If you want to restore your playlists, just upload the playlists files to the `/wp-content/fmp-jw-files/playlists` directory.

## Other Topics

### The JW Player and FLA File Download

The player embedded in this plugin is so-called [JW Player](http://www.longtailvideo.com/players/jw-flv-player/), which is the same as the player in YouTube. But the player in this plugin is the version 2.3 of JW Player, the reason for this version is because the size of the player file is just 9.5K bytes. It is very fast for the browser to load this player in. The short hand of it is that this player can just play audio. Just as the name of this plugin, it is an mp3 player, so the function of the version 2.3 is suitable. A lot of designer want to customize the look the player, so I give you it here. You can download it by click the link below.

### Player Printer, Config Editor and Playlist Editor

This plugin is composite of three parts. The first is _Player Printer_. This thing is used to put the mp3 player on your page. Its core is a template tag, and extended forms are _sidebar widget_ and _shortcode_. The second and the third is two XML file editors, _Config Editor_ and _Playlist Editor_. They are just two XML file creating helpers. If you know how to edit a XML file, you can edit them, include config file and playlist file, locally and upload them to your server yourself.

### FAQ

1.  where to edit the code to make the song image larger?----You can download the source file of the player and change the size of image yourself if you know how to modify the code.