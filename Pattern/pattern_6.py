'''
   *
  ***
 *****
*******
'''

row=5

for i in range(0,row):
    for _ in range(i, row-1):
        print(' ', end='')
    for _ in range(0, 2*i+1):
        print('*', end="")
    print('')        
