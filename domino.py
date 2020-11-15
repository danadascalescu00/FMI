#Programare dinamica-complexitate: O(n^2)
def domino(input, N):
    L = [1] * N
    pos = [-1] * N
    max = 1
    p = 0

    for i in range(1, N):
        for j in range(i-1):
            if input[i][0] == input[j][1]:
                L[i] = 1 + L[j]
                pos[i] = j
                if max < L[i]:
                    max = L[i]
                    p = i

    count = L.count(max)

    i = p
    while i != -1:
        print(input[i])
        i = pos[i]

    return count

if __name__ == '__main__':
    input = []
    with open('domino.in') as fin:
        N = int(fin.readline())
        for _ in range(N):
            x, y = [int(val) for val in next(fin).split()]
            input.append([x,y])

    maxi = domino(input, N)

    print("Number of substrings of the maximum lenght: ", maxi)