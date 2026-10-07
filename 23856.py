from ipaddress import *
net=ip_network('172.95.116.174/255.255.192.0', strict=False)

for x in net:
    s=format(x, 'b')
    if s.count('1')%5==0:
        print(x)
        break