from fnmatch import fnmatch
for x in range(0, 10**9, 107):
    if fnmatch(str(x), '38?375*9'):
        print(x, x//107)