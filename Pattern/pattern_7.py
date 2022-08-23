row=5

for i in range(row,0,-1):
    for _ in range(i, row):
        print(' ', end='')
    for _ in range(0, 2*i-1):
        print('*', end="")
    print('')        
