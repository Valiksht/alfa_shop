def genegate(n):
    sequence = ''
    loop = 1
    while len(sequence) < n:
        sequence += str(loop)*loop
        loop += 1
    return sequence[:n]


n = int(input('Введите длину последовательности:'))
print(genegate(n))
