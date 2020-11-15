cubes , solution = [] , []
with open("cuburi.txt") as fin:
    n , p = [int(value) for value in next(fin).split()]
    for i in range(n):
        input = []
        input.append(i+1)
        input.extend([int(val) for val in fin.readline().split()])
        cubes.append(input)
fin.close()

cubes = sorted(cubes, key = lambda c:c[1], reverse=True)
solution.append(cubes[0])
height = cubes[0][1]

for i in range(n):
    if cubes[i][2] != solution[-1][2]:
        solution.append(cubes[i])
        height += cubes[i][1]

print("Turnul este format din", len(solution), "cuburi")
print("Inaltimea este", height)
print("Au fost alese: ")
for i in range(len(solution)):
    print("Cubul",solution[i][0],"cu inaltimea",solution[i][1],"si culoarea",solution[i][2])