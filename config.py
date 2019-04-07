#coding:utf-8
#author:w8ay

host = "www.hacking8.com" # 需要查找网站的域名

keyword = ["<h1>Hello World"] # 需要查找的关键字 结果没有解码，最好是英文,列表形式可以多个

path = "/" # WEB扫描路径，/为跟路径

timeout = 15 # 连接网站时超时IP

HTTPS_Support = False # 此参数为True时，将进行HTTPS访问，masscan将扫描443端口，并且扫描https的网址

rate = 1000 # masscan的扫描速度，越大越快，越小越精确