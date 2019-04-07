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
import time
import zlib, socket,ssl
import config
from lib.common import print_msg


def masscan(path,rate):
    try:
        path = str(path).translate(None, ';|&')
        rate = str(rate).translate(None, ';|&')
        if not os.path.exists(path):return
        PortScaned = 80
        if config.HTTPS_Support:
            PortScaned = 443
        os.system("%s -p%s -iL target.log -oL tmp.log --randomize-hosts --rate=%s"%(path,PortScaned,rate))
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

    if port == 443:
        sock = ssl.wrap_socket(socket.socket())
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    sock.settimeout(config.timeout)
    sock.connect((host, port))


    data = "GET %s HTTP/1.1\r\nHost: %s\r\nAccept-Encoding: gzip, deflate\r\nConnection: close\r\n\r\n" % (config.path,domain)

    sock.send(data)

    recv_data = ""
    header = None
    body = None
    length = 0

    headers = {}


    html = ""

    while True:
        buf = sock.recv(1024)
        if buf:
            recv_data += buf
        else:
            break

        if header is None:
            index = recv_data.find("\r\n\r\n")
            if index >= 0:
                header = recv_data[0:index]
                recv_data = recv_data[index+4:]
                header_lines = header.split("\r\n")
                status_line = header_lines[0]
                # print status_line
                for line in header_lines[1:]:
                    # print line
                    line = line.strip("\r\n")
                    if len(line) == 0:
                        continue
                    colonIndex = line.find(":")
                    fieldName = line[:colonIndex]
                    fieldValue = line[colonIndex+1:].strip()
                    headers[fieldName] = fieldValue
                if "Content-Length" in headers:
                    length = int(headers['Content-Length'])
        if header is None:
            break

    if 'Content-Encoding' in headers and headers['Content-Encoding'] == 'gzip' :
        html = zlib.decompress(recv_data, 16+zlib.MAX_WBITS)
    else:
        html = recv_data
    sock.close()
    return html

class HttpTest(object):

    def __init__(self,host,keyword,ips,timeout):
        self.threads = 100
        self.queue = PriorityQueue()
        self.host = host
        self.keyword = keyword
        if isinstance(self.keyword,str):
            self.keyword = [self.keyword]
        self.result = []
        for ip in ips:
            self.queue.put(ip)
        self.num = self.queue.qsize()
        self.i = 0
        self.success = 0
        self.timeout = timeout
        self.filename = os.path.join(rootPath,"result",host + ".log")
        self.outfile = open(self.filename, 'w')

    def _in_keyword(self,html):
        ret = True
        for i in self.keyword:
            if html not in i:
                ret = False
                break
        return ret

    def _scan(self,j):
        while not self.queue.empty():
            try:
                item = self.queue.get(timeout=3.0)
                if config.HTTPS_Support:
                    host, domain, port = item, self.host , 443
                else:
                    host, domain, port = item, self.host , 80
                html = httpServer((host, domain, port),self.timeout)
                if html is not None and self._in_keyword(html):
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
    if not config.rate:
        rate = 1000
    else:
        rate = config.rate
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
