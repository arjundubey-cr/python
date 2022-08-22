'''
    Print the following pattern:
    
    *****
    *****
    *****
    *****
    *****
'''


def pattern():
    for _ in range(5):
        for _ in range(5):
            print('*', end='')
        print('')


pattern()
