# O(nlogn)
AB = []
input = []
with open('acoperire.txt') as fin:
    for values in fin.readline().split():
        AB.append(int(values))
    N = int(fin.readline())
    for line in fin:
        input.append([int(x) for x in line.split()])
fin.close()

input = sorted(input, key=lambda v:v[0])
solution = []

first_target = AB[0]
count = i = 0
best_right_end = index_best = -1

while first_target <= AB[1] and i < len(input):
    if input[i][1] >= AB[0]:
        if input[i][0] <= first_target:
            if input[i][1] >= best_right_end:
                best_right_end = input[i][1]
                index_best = i
            i = i + 1
        elif best_right_end != -1:
            solution.append(input[index_best])
            count = count + 1
            first_target = best_right_end
            best_right_end = - 1
    else:
        i = i + 1

if count == 0 | first_target < AB[1]:
    print("Nu exista solutie!")
else:
    print("Cardinalul solutiei este", count)
    print(solution)
