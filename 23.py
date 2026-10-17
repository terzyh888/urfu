def f(num, end):
    if num==end:
        return 1
    if num<end or num==8:
        return 0
    return f(num-1, end)+f(num-4, end)+f(num//2, end)
print(f(30, 12)*f(12, 4))