#coding:utf-8
#author:w8ay
#@date:2018年5月21日 18:17:22
"""
     w8fuckcdn 1.0
     (https://x.hacking8.com)
"""

import sys,os,platform,gevent
from gevent import monkey
monkey.patch_all()
from gevent.queue import PriorityQueue
import socket,time
import config
from lib.common import print_msg


def masscan(path,rate):
    try:
        path = str(path).translate(None, ';|&')
        rate = str(rate).translate(None, ';|&')
        if not os.path.exists(path):return
        os.system("%s -p80 -iL target.log -oL tmp.log --randomize-hosts --rate=%s"%(path,rate))
        result_file = open('tmp.log', 'r')
        result_json = result_file.readlines()
        result_file.close()
        del result_json[0]
        del result_json[-1]
        open_list = {}
        for res in result_json:
            try:
                ip = res.split()[3]
                port = res.split()[2]
                if ip in open_list:
                    open_list[ip].append(port)
                else:
                    open_list[ip] = [port]
            except:pass
        os.remove('tmp.log')
        return open_list
    except:
        return None

def httpServer(arg,timeout = 5):
    host, domain ,port = arg
    try:
        socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketObj.settimeout(timeout)
        socketObj.connect((host, port))
        socketObj.send("GET / HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n" % domain)
        read = socketObj.recv(1024)
        if read.find("HTTP/1.") == 0 or read.lower().find("<html") > 0:
            return read
        socketObj.close()
    except Exception as e:
        return None

class HttpTest(object):

    def __init__(self,host,keyword,ips,timeout):
        self.threads = 100
        self.queue = PriorityQueue()
        self.host = host
        self.keyword = keyword
        self.result = []
        for ip in ips:
            self.queue.put(ip)
        self.num = self.queue.qsize()
        self.i = 0
        self.success = 0
        self.timeout = timeout
        self.filename = os.path.join(rootPath,"result",host + ".log")
        self.outfile = open(self.filename, 'w')


    def _scan(self,j):
        while not self.queue.empty():
            try:
                item = self.queue.get(timeout=3.0)
                host, domain, port = item, self.host , 80
                html = httpServer((host, domain, port),self.timeout)
                if html  is not None and self.keyword in html:
                    self.outfile.write(item + '\n')
                    self.outfile.flush()
                    self.success += 1
            except:
                pass
            finally:
                self.i += 1
                msg = '[*] %s found, %s scanned , %s groups left'%(self.success,self.i,self.num - self.i)
                print_msg(msg)
            time.sleep(1.0)

    def run(self):
        threads = [gevent.spawn(self._scan, i) for i in range(self.threads)]
        gevent.joinall(threads)

        msg = '[+] All Done. Success:%d Saved in:%s'%(self.success,self.filename)
        print_msg(msg, line_feed=True)


def main():
    system = platform.system()
    rate = 10000
    masscanPath = ""

    if system == "Windows":
        masscanPath = os.path.join(rootPath, "bin", "windows_64", "masscan.exe")
    elif system == "Linux":
        masscanPath = os.path.join(rootPath, "bin", "linux_64", "masscan")

    result = masscan(masscanPath,rate)
    if result is None:
        print("No valid IP address found")
        exit()

    hackhttp = HttpTest(config.host,config.keyword,result.keys(),config.timeout)
    hackhttp.run()

def test(ip):
    html = httpServer((ip, config.host, 80), 10)
    print html

if __name__ == '__main__':
    rootPath = os.path.dirname(os.path.realpath(__file__))
    main()
