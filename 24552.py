from ipaddress import *
net=ip_network('202.71.92.91/255.255.192.0', strict=False)
for x in net:
    if [x[:8]%2!=0, x[8:16]%2!=0, x[16:24]%2!=0, x[24:]%2!=0].count(True)==2:
        print(x)