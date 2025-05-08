def checkSudoku(x):
    for i in x:
        if sum(i) != 45:
            return False
    for i in range(9):
        summ = 0
        for j in range(9):
            summ += x[j][i]
        if summ != 45:
            return False
    return True
        
        
