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
    u(string) for string in open('27_B_29076.txt')
]

cluster1=[star for star in table if 10<star[1]<15 and 24<star[0]<30]
cluster2=[star for star in table if 15<star[1]<22.5 and 13<star[0]<18]
cluster3=[star for star in table if 22.5<star[1]<30 and 11<star[0]<16]

def center(cluster):
    min_dist=10**20
    cpoint=[]
    for point1 in cluster:
        sum_dist=sum([mydist(point1, point2) for point2 in cluster])
        if sum_dist<min_dist:
            min_dist=sum_dist
            cpoint=point1
    return cpoint

def red(cluster, count):
    for star in cluster:
        if star[2]=='Y':
            count+=1
    return count

print(red(cluster1, 0), red(cluster2, 0), red(cluster3, 0))

cl1=center(cluster1)
cl2=center(cluster2)
cl3=center(cluster3)

print(int(mydist(cl1, cl2)*10_000))

def maxi(cluster):
    cp=center(cluster)
    max_dist=max([mydist(cp, point) for point in cluster if point[2]=='Y'])
    return max_dist

print(int(max(maxi(cluster1), maxi(cluster2), maxi(cluster3))*10_000))
print(maxi(cluster1), maxi(cluster2), maxi(cluster3))
