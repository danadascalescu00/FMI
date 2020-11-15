from copy import copy
matrix = []
with open('date.in') as fin:
    n, m = [int(val) for val in next(fin).split()]
    for _ in range(n):
        matrix.append([int(val) for val in next(fin).split()])

matrix_values = [[0]*m for i in range(n)]
matrix_position = [[[1, 1]]*m for i in range(n)]
matrix_values[0][0] = matrix[0][0]

for i in range(n):
    for j in range(m):
        v, b = [], []
        if i == 0:
            matrix_values[0][j] = matrix_values[0][j-1] + matrix[0][j] if j != 0 else matrix[0][0]
            matrix_position[0][j] = [1,j] if j != 0 else [1,1]
        if j == 0:
            matrix_values[i][0] = matrix_values[i-1][0] + matrix[i][0]
            matrix_position[i][0] = [i, 1]
        else:
            matrix_values[i][j] = max(matrix_values[i-1][j],matrix_values[i][j-1]) + matrix[i][j]
            matrix_position[i][j] = [i+1,j] if matrix_values[i][j-1] == max(matrix_values[i-1][j], matrix_values[i][j-1]) else [i,j+1]


pos1, pos2 = matrix_position[n-1][m-1][0], matrix_position[n-1][m-1][1]

output = [[n,m]]
while pos1 != 0 or pos2 != 1:
    output.append([pos1,pos2])
    pos1, pos2 = matrix_position[pos1-1][pos2-1][0], matrix_position[pos1-1][pos2-1][1]

print(matrix_values[n-1][m-1])
for i in range(1,len(output)+1):
    print(output[-i])

for i in range(n):
    print(matrix_position[i])