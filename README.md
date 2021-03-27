# Simple_saya_plugins

## 这是什么
一个使用graia-saya写的模块化垃圾代码(能用就行)

## 开始使用
在`configs.yml`填写
```yaml
account: 1919810 #账号
authKey: ZenBuMuDa #MiraiApiHttp的authKey
miraiHost: http://localhost:8080
load_folder: #加载的文件夹
  - entertain
```

## 他能做什么
注：以下功能的所有用法都在每个模块的'channel.description'变量  
    不知道能不能用(push前都不test的屑)
 
现在他所能做的功能有：

插件名|功能描述|~~从哪抄的~~|require|备注
:--:|:--:|:--:|---|---
dd|DD直播间查看||aiohttp<br/>pillow<br/>pyyaml|
pic|小老弟表情包P图||aiohttp<br/>pillow|
anime_timesche|新番时刻表||aiohttp<br/>pillow|
auto_ban|禁言我|||
baidu|百度百科，百度热点|当年酷Q论坛上的一个帖子|aiohttp<br/>lxml|
bangumi|番剧详细信息|[SAGIRI-kawaii/sagiri-bot](https://github.com/SAGIRI-kawaii/sagiri-bot)|aiohttp|
bar_music|网易云音乐音频||graia-template<br/>graiax-silkcoder<br/>pycryptodome<br/>ujson<br/>aiofiles|需要expand/Netease.py
COVID|新冠疫情查询||matplotlib<br/>numpy<br/>numpy|
video_info|B张视频详细信息||aiohttp|
petpet|petpet图片制作|[SAGIRI-kawaii/sagiri-bot](https://github.com/SAGIRI-kawaii/sagiri-bot)|pillow|
ph|pornhub图片制作|[SAGIRI-kawaii/sagiri-bot](https://github.com/SAGIRI-kawaii/sagiri-bot)|pillow|需要expand/text.py<br/>scr/font
ero|涩图来||aiohttp<br/>pillow<br/>ujson|需要expand/save.py<br/>需要自行设置Lolicon api key<br/>请自行创建一个data文件夹
5000M|5000兆円欲しい! style生成器|[pycabbage/discord5000chobot](https://github.com/pycabbage/discord5000chobot)|pillow<br/>numpy|需要src/font
ghost_tank|幻影坦克生成器|[Aloxaf/MirageTankGo](https://github.com/Aloxaf/MirageTankGo)|pillow<br/>numpy

## 未来要做的功能有：
 - ~~抄其他机器人的功能~~

## 为什么这些功能跟[sagiri的saya_plugins_collection](https://github.com/SAGIRI-kawaii/saya_plugins_collection)几乎一模一样
### ~~为什么呢?我也在寻找原因呢——Decade~~
Sagiri**写插件永远滴神**。速度之快带伙有目共睹，每天都在群里问有没有好玩的插件可以写，一有灵感马上写好  
顺便在这里放上Sagiri的[Saya仓库](https://github.com/SAGIRI-kawaii/saya_plugins_collection)，理论上应该也是可以load的