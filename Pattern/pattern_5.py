'''
*****
****
***
**
*
'''
def pattern():
    for i in range(5, 0, -1):
        for j in range(i, 0, -1):
            print('*', end='')
        print('')

pattern()