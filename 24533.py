from itertools import product
k=0
for x in product('АЕКНОТ', repeat=7):
    k+=1
    if k%2!=0:
        if x.count('Е')==1:
            if x.count('К') == 2:
                if x.count('Н') == 1:
                    if x.count('О') == 2:
                        if x.count('Т') == 1:
                            print(k)