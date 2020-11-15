def Levenshtein_Distance(a, b, weights):
    m, n = len(a), len(b)
    M = [[0 for j in range(n)] for i in range(m)]

    M[0] = [j for j in range(n)] # edit distance from empty string to a

    for i in range(1, m):
        M[i][0] = i # edit distance from empty string to string b
        for j in range(1, n):
            if a[i] == b[j]:
                M[i][j] = M[i-1][j-1]
            else:
                M[i][j] = min(M[i][j - 1] + weights[1], M[i - 1][j - 1] + weights[2] , M[i - 1][j] + weights[0])

    edit = [None] * max(len(a) , len(b) )
    i, j, k = len(a)-1, len(b)-1, len(edit) - 1

    for h in range(n):
        print(M[h])

    while k >=0 and i>0 and j>0:
        if a[i] == b[j]:
            edit[k] = "keep " + a[i]
            i, j, k = i-1, j-1, k-1
        elif M[i][j] == weights[0] + M[i-1][j-1]:
            edit[k] = "replace " + a[i] + " --> " + b[j]
            i, j, k = i-1, j-1, k-1
        elif M[i][j] == weights[1] + M[i-1][j]:
            edit[k] = "delete " + a[i]
            i, k = i-1, k-1
        elif M[i][j] == weights[2] + M[i][j-1]:
            edit[k] = "insert " + b[j]
            j, k = j-1, k-1

    while k>=0 and i>0:
        edit[k] = "delete " + a[i]
        i, k = i-1, k-1

    while k>=0 and j>0:
        edit[k] = "insert " + b[j]
        j, k = j-1, k-1

    return M[m-1][n-1],edit

if __name__ == '__main__':
    weights = []
    with open('levedist.in', 'r') as fin:
        a = fin.readline().replace('\n', '')
        b = fin.readline().replace('\n', '')
        weights = [int(val) for val in fin.read().split()]

    print(a)
    print(b)
    print(weights)

    distance, edit = Levenshtein_Distance(a, b, weights)
    print("Edit distance between", a[1:], "and", b[1:], "is: ", distance)
    for i in range(len(edit)):
        print(edit[i])