'''
    Print the following pattern: 

    *
    **
    ***
    ****
    *****
'''


def pattern():
    for i in range(5):
        for _ in range(i+1):
            print('*', end="")
        print('')


pattern()
