from ipaddress import *
net=ip_network('154.141.198.190/255.255.192.0', strict=False)
print(net[-1])