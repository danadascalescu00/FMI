fin = open("3sum.txt", "r")
vector = []
for value in fin.read().split():
    vector.append(int(value))
fin.close()

vector = sorted(vector)
output = set()
for k in range(len(vector)):
    pivot = -vector[k]
    i , j = k + 1, len(vector) - 1
    while i < j:
        sum_two = vector[i] + vector[j]
        if sum_two < pivot:
            i = i + 1
        elif sum_two > pivot:
            j = j - 1
        else:
            output.add((vector[k], vector[i], vector[j]))
            i = i + 1
            j = j - 1

print(output)
