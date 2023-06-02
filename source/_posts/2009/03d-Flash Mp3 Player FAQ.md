---
title: Flash Mp3 Player FAQ
tags:
  - documents
  - FAQ
  - plugins
  - WordPress
id: '326'
categories:
  -   - WordPress
date: 2009-03-13 12:05:09
permalink: flash-mp3-player-faq/
---

Author of this document: [Snowblink](http://www.magicsnowblink.com/)

Actually, I'm lazy, and I hate paper work. My dear friend, Snowblink, created this document. Thank her very much!

非常感谢snowblink的辛勤工作，我不知道如何才能用英语表达对你的感谢。所以用中文再说一遍！
<!-- more -->
If the following answers do not solve your problem, please contact the author via the [Contact Form](http://sexywp.com/contact).

Please describe your problem, the PHP and wordpress version you use, and what you have already tried in detail.

**Q1: Which version of the PHP do I need to make the flash mp3 player work?**

A: This plugin requires PHP version 4 or higher.

**Q2: Which version of wordpress does the plugin require?**

A: WordPress 2.5 or newer recommended.

**Q3: When I use your plugin, I got the following error message:**

Warning: domdocument() expects parameter 2 to be long, string given in /home/8099/domains/funkshoppe.com/html/wp-content/plugins/flash-mp3-player/flash-player-widget.php on line 120
Fatal error: Call to undefined function: loadxml() in /home/8099/domains/funkshoppe.com/html/wp-content/plugins/flash-mp3-player/flash-player-widget.php on line 121 
**My WP version is 2.6. What can I do?**
A: This error may result from using PHP prior to version 5. Maybe you could edit the "playllist.xml" by hand. The file is in folder"flash-mp3-player". **Now, this plugin support PHP 4**.

**Q4: I'm not able to see the plugin in the options panel, where I can change the playlist. Although I can configure the widget, I see nothing where I can change the playlist. What can I do? I try already to reinstall it, but nothing changes.**

A: Maybe the options panel does not work under PHP prior to version 4.2. But you can edit the playlist manually instead of using options panel. The playlist file is a XML file in the plugin directory called playlist.xml. You can edit it using Notepad or something like that. There are some samples in this file originally.

**Q5: I want to get rid of the title "Flash MP3 Player" which appears above the player and the bar that appears below the player. What can I do?**

A: To get rid of the title "Flash MP3 Player", you should go to the widgets admin page, find the Flash MP3 Player widget, and edit its title.

I don't know exactly what the bar you talked about. If you mean the playlist part of the player, you can go to the options->MP3 player page, and input the answer "no" to the question "Show play list,yes or no?"

**Q6: When I try to change my playlist, it doesn't change in the player. I changed the song titles and locations in the player settings, and those changes were written to the playlist xml file, but the widget in the side bar is still playing the old playlist. I've tried refreshing the webpage and cleared my temporary Internet files and cookies. I've tried it in Firefox 3 and Internet Explored 7. I've removed and replaced the widget. I've deactivated and reactivated the plugin. I just can't get it to update and use the new list. Any suggestions?**

A: It seems that you have tried every method I can find to fix this problem. I still think the real problem is that the browser does not download the playlist xml file, but still use the old one. Maybe you could try another version. Its location is at....(此处有附件，没包括）

**Q7: Every time I try to put in my own songs and press save, none of the options save. Actually, I cannot change the default options. Please help me.**

A: You could try to edit the playlist manually, it is in the /wp-content/fmp_my_playlist directory. If the playlist is not there, maybe you could try to update the plugin. I hope this could help.

**Q8: Is it possible to extend the playlist to approx.15 songs? Is there a way to order playlist into albums?**

A: If you want to insert more than 10 songs to your playlist, the only way currently is to edit the playlist.xml manually.This file is in directory "wp-content/fmp_my_playlist".
I am sorry that you cannot manage the playlist by albums, since the player itself does not have this feature. 

**Q9:I've just tried installing your flash player on my WP 2.6 site.
However, I got the following error when turning the plugin on:
Warning: copy(/home/staff_hosting/vgames_beta/public_html/minisites/blogs.vgames.co.il/public_html/h2/wp-content/fmp_my_playlist/playlist.xml) [function.copy]: failed to open stream: No such file or directory in /home/staff_hosting/vgames_beta/public_html/minisites/blogs.vgames.co.il/public_html/h2/wp-content/plugins/flash-mp3-player/flash-player-widget.php on line 49
In addition, when trying edit the player configuration, I got this error:
Fatal error: Class 'DOMDocument' not found in /home/staff_hosting/vgames_beta/public_html/minisites/blogs.vgames.co.il/public_html/h2/wp-content/plugins/flash-mp3-player/flash-player-widget.php on line 147
What to do?**

A:It seems that the copy function fails in your site. You could try this:
First, create a directory "fmp_my_playlist" in "/wp-content".
Second, copy the file "playlist.xml" which is under the plugin directory to the new directory.
Third, try to edit the playlist in admin panel again.
If all of the above don't work, you could edit the playlist.xml mannually.

**Q10:When accessing the player configuration menu, I get the following error:**
Fatal error: Class 'DOMDocument' not found in /home/staff_hosting/vgames_beta/public_html/minisites/blogs.vgames.co.il/public_html/h2/wp-content/plugins/flash-mp3-player/flash-player-widget.php on line 147
I guess this means I won't be able to use the configuration menu?
I tried editing the XML file manually and uploading it via FTP, but it seems to have no effect.
EDIT: It seems my browser was simply displaying the cached version of the site.
This keeps happening whenever I edit the play list - in both IE and FireFox. Any thoughts on how to make it refresh?
I don't want to require the users to clean their cache every time to see the updated play list.

A:It seems that the PHP on your host does not support the DOMDocument class, so you have to edit the playlist manually.
In fact, there is a way to force browsers to download the new version of the playlist:
First, find this line in the source code(line 69)
 $datafield = $base_name . '/mp3player.swf?playlist=' . $fmp_listfile_url;
Second, change it to:
 $datafield = $base_name . '/mp3player.swf?playlist=' . $fmp_listfile_url . '?' . rand();
This is a little trick. The random query string will tell the browser, "this playlist is not the same one with you have downloaded last time, and you must download it again." (此处有附件，没包括）

**Q11:Would it be possible to make track names right-alighned and right-to-left in direction?Does that require a code change or just an addition to the playlist XML?**

A:Sorry,you can not make the player right-align the track name through the configure xml file, and me too. I'm not the author of the mp3 player, I'm just the one who make it a WP plugin.