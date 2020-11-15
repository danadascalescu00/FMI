def divide(dim, i, j):
    #Pentru n = 1
    if dim == 1:
        if i == 1:
            if j == 1:
                return 1
            else:
                return 2
        if i == 2:
            if j == 1:
                return 3
            else:
                return 4

    #Pentru n>=2:
    num = dim ** 2
    restriction = dim // 2
    #Cadranul I:
    if i <= restriction and j <= restriction:
        return divide(restriction, i, j)
    #Cadranul II
    if i <= restriction and j > restriction:
        return num // 4 + divide(restriction, i, j - restriction)
    #Cadranul III
    if i > restriction and j <= restriction:
        return 2 * (num // 4) + divide(restriction, i - restriction, j)
    #Cadranul IV
    if i > restriction and j > restriction:
        return 3 * (num // 4) + divide(restriction, i - restriction, j - restriction)

if __name__ == '__main__':
    fin = open('z.in')
    N, K = [int(x) for x in next(fin).split()]
    dim = 2 ** N
    with open('z.out', 'w') as fout:
        for _ in range(K):
            i, j = [int(x) for x in next(fin).split()]
            result = divide(dim, i, j)
            print(result, file=fout)