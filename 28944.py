def deliteli(chislo):
    spisok=[]
    for d in range(2, int(chislo**0.5)+1):
        if chislo%d==0:
            spisok.append(d)
            spisok.append(chislo//d)
    return spisok

amount=0
for x in range(8_996_453, 10**20):
    dividers=deliteli(x)
    prostye=[num for num in dividers if len(deliteli(num))==0 and str(num).count('3')==2]

    if len(prostye)==2:
        if prostye[0]*prostye[1]==x:
            amount+=1
            print(x, max(prostye))

    if amount==5:
        break