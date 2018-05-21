# w8Fuckcdn
> 通过扫描全网绕过CDN获取网站IP地址

## 使用
- target.log 配置扫描的IP段
- config.py 设置要查找的文本以及网站域名
- 运行 `python fuckcdn.py` 

## 程序流程
基于masscan扫描IP端中开放的80端口，程序自动连接每个IP测试，筛选出符合条件的ip保存到result.txt  
后续程序会提供"基于扫描子域名获取IP段"的方法来尽可能减少IP段范围

## 特性
1. 支持winodws/linux
2. gevent 协程IO 最大化利用资源
3. masscan扫描，最快能6分钟扫完全网

## 安装
- pip install gevent

## 问题&答案
1. 如果发现masscan运行出错请编译masscan
2. 如果第一次扫描发现了大量IP可以将IP放到target.log进行第二次扫描并重新设置关键字

## Thanks
- [https://github.com/ysrc/xunfeng](https://github.com/ysrc/xunfeng) 中提供的编译好的masscan
- [https://github.com/Tai7sy/fuckcdn](https://github.com/Tai7sy/fuckcdn) 思路