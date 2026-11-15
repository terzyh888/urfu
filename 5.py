a=[]
for n in range(19, 400):
    s=bin(n)[2:]
    if n%2==0:
        s='10'+s
    if n%2!=0:
        s='1'+s+'01'
    r=int(s, 2)
    a.append(r)
print(min(a))