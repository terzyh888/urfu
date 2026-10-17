def f(n):
    res=''
    while n!=0:
        res=str(n%9)+res
        n//=9
    return res

for n in range(1, 10000):
    s=f(n)
    if s[0]=='7':
        s=s.replace('3', '-').replace('6', '3').replace('-', '6')
        s='34'+s
    else:
        s=s+'45'
        s='3'+s[1:]
    r=int(s, 9)
    if r==2795:
        print(n)
