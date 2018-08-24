#coding:utf-8
#author:w8ay

host = "www.hacking8.com" # 需要查找网站的域名

keyword = "Hello World" # 需要查找的关键字 结果没有解码，最好是英文

timeout = 15 # 连接网站时超时IP

HTTPS_Support = False # 此参数为True时，将进行HTTPS访问，masscan将扫描443端口，并且扫描https的网址