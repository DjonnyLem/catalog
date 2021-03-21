import os
def make_dir():
    a = int(input('Введите месяц: '))
    b = int(input('Введите начальную дату: '))
    c = int(input('Введите конечную дату: ')) + 1

    
    for i in range (b, c):
        if i < 10:
                if a < 10:
                    os.mkdir('2021.' + '0' + str(a) + '.0' + str(i))
                else:
                    os.mkdir('2021.' + str(a) + '.0' + str(i))
        else:
            if a < 10:
                os.mkdir('2021.' + '0' + str(a) + '.' + str(i))
            else:
                os.mkdir('2021.' + str(a) + '.' + str(i))


make_dir()

