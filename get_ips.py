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


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "[usage] python get_ips baidu.com"
        exit()

    host = sys.argv[1]
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

