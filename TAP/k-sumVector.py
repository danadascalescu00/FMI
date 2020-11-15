with open("k-sumVector.txt") as fin:
    N, k = [int(val) for val in fin.readline().split()]
    table = [[0]*k for i in range(N)]

input = []
with open("k-sumVector.txt") as fin:
    for i, line in enumerate(fin):
        if i >= 1:
            input.append([int(val) for val in line.split()])
            if i == 1:
                for j in range(len(input[0])):
                    table[i-1][input[0][j] - 1] = j + 1
            elif i >= 2:
                for j in range(len(input[i-1])):
                    for l in range(k):
                        if table[i-2][l] != 0:
                            s = l+1 + input[i-1][j]
                            if s <= k:
                                table[i-1][s-1] = j + 1
    print(input)
    print("")


for i in range(N):
    print(table[i])

if table[N-1][k-1] == 0:
    print(0)
else:
    output = []
    pos = table[N-1][k-1] - 1
    while N>= 1:
        output.append(input[N-1][pos])
        k = k - input[N-1][pos]
        N = N - 1
        pos = table[N-1][k-1] - 1
    output.reverse()
    print("Vectorul creat: ", output)