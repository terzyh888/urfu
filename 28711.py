def deliteli(chislo):
    spisok=[]
    for d in range(2, int(chislo**0.5)+1):
        if chislo%d==0:
            spisok.append(d)
            spisok.append(chislo//d)
    return spisok

def f(x):
    dividers=deliteli(x)
    prostye=[num for num in dividers if len(deliteli(num))==0 and (str(num).count('4')>=1 or str(num).count('7')>=1)]

    all=[]

    for y in prostye:
        for i in range(1, 30):
            if x%y**i==0:
                all.append(y)
    return all

amount=0
for x in range(2_400_001, 10**20):
    pro=f(x)

    if len(pro)==3:
        if pro[0]*pro[1]*pro[2]==x:
            amount+=1
            print(x, max(pro))

    if amount==5:
        break
