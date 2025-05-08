def series(n):
    if n == 1:
        return 1
    else:
        return series(n-1) + (n**(n-1))/(n-1)
        
