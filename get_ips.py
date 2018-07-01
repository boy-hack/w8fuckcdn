#coding:utf-8
#author:w8ay
#@date:2018年5月22日 09:43:23
"""
     w8fuckcdn 1.0
     (https://x.hacking8.com)
     获取子域名的IP段
"""
import sys; sys.path.append('./thirdparty/subdomainBrute')
from thirdpart.subdomainBrute import subdomain
from thirdpart.IPy import IP
import argparse
import urlparse
import socket

def get_url_host(url):
    host = urlparse.urlparse(url)[1]
    if ':' in host:
        host = host[:host.find(':')]
    return host

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='powered by w8ay <mail:master@hacking8.com> ')

    parser.add_argument('-d', dest="domain" ,type=str, default='')

    parser.add_argument('-f', metavar='FILE',dest="filename" ,type=str, default='')

    parser.add_argument('-o', dest="output" ,type=str, default='output.txt')

    parser.add_argument('--ips', dest="ips", default=False, action='store_true')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()

    if args.domain:
        host = args.domain
        result =  subdomain.Interface(host)
        if result is None or not len(result):
            print("No vaild IP found")
            exit()

        ips = list(set(result))

        netmask='255.255.255.0'
        ip_range_list = [str(IP(ip).make_net(netmask)) for ip in ips]

        ips = list(set(ip_range_list))
        info = '\n'.join(ips)

        filename = 'target.log'
        with open(filename, 'w') as f:
            f.write(info)
        print '[*] Info is saved into %s'%(filename)
        exit()
    
    filename = args.filename
    output = args.output
    if filename:
        with open(filename) as f:
            flines = f.readlines()
        result = set()
        I = 0
        count = len(flines)
        print "total:%d " % (count)
        for line in flines:
            host = get_url_host(line).strip()
            try:
                ip = socket.gethostbyname(host)
                result.add(ip)
            except Exception,e:
                print e,host
            I = I + 1
            if I%300 == 0:
                print "works 300 ..."
        result = list(result)
        print "process finished,building..."
        if args.ips:
            netmask='255.255.255.0'
            ip_range_list = [str(IP(ip).make_net(netmask)) for ip in result]

            ips = list(set(ip_range_list))
            info = '\n'.join(ips)
        else:
            info = '\n'.join(result)
            
        with open(output, 'w') as f:
            f.write(info)
        print '[*] Info is saved into %s'%(output)


