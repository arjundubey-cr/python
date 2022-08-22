'''
    Print the following patterns
    1
    22
    333
    4444
    55555
'''


def pattern():
    for i in range(1, 6):
        for _ in range(i):
            print(i, end='')
        print('')


pattern()
