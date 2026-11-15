from math import dist
def mydist(p1, p2):
    return dist([p1[0], p1[1]], [p2[0], p2[1]])

def u(string):
    a, b, c=string.replace(',', '.').split()
    if c=='VII':
        color=''
        l=''
        s=c
    else:
        color=c[0]
        l=c[1]
        s=c[2:]
    return [float(a), float(b), color, l, s]

table=[
    u(string) for string in open('27_A_29076.txt')
]

cluster1=[star for star in table if star[1]<8]
cluster2=[star for star in table if star[1]>8]

def center(cluster):
    min_dist=10**20
    cpoint=[]
    for point1 in cluster:
        sum_dist=sum([mydist(point1, point2) for point2 in cluster])
        if sum_dist<min_dist:
            min_dist=sum_dist
            cpoint=point1
    return cpoint

def z2(cluster, count):
    for zvezda in cluster:
        if zvezda[3]=='2':
            count+=1
    return count

print(z2(cluster1, 0), z2(cluster2, 0))

a=int(center(cluster2)[0]*10_000)
b=int(center(cluster1)[1]*10_000)

print(a, b)
