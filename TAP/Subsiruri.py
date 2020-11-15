sequence = []
with open('subsiruri.txt') as fin:
    n = int(fin.readline())
    for x in fin.readline().split():
        sequence.append(int(x))
fin.close()

def BinarySearch(a,x):
    i = 0
    j = len(a) - 1
    mid = 0
    while i<j:
        mid = (i+j)//2
        if a[mid-1][1] < x and a[mid][1] >= x:
            i = mid + 1
        else:
            j = mid

    if a[mid][1]>x:
        return a[mid][0]
    else:
        return -1

subsequences = []
search = []
subsequences.append([sequence[0]])
search.append([0,sequence[0]])

for index, item in enumerate(sequence[1:]):
    pos = BinarySearch(search,item)
    if pos == -1:
        subsequences.append([item])
        search.append([len(subsequences), item])
    else:
        subsequences[pos].append(item)
        search[pos][1] = item

print("Numarul subsirurilor: ", len(subsequences))
print(subsequences)