def getFirst(item):
    return item[0]


a = 8
b = 16

arr = [[3, 9], [4, 9], [8, 9], [9, 12], [11, 12], [15, 16], [12, 16], [150, 163]]
arr = sorted(arr, key=getFirst)
print(arr)
i = 0
max = -1
i_max = 0
while a < b and i < len(arr):
    if arr[i][0] <= a:
        if arr[i][1] >= max:
            if arr[i][1] >= b:
                max = arr[i][1]
                a = max
                print(arr[i])
            max = arr[i][1]
            i_max = i
        i += 1
    elif max != -1:
        a = max
        max = -1
        print(arr[i_max])
    else:
        print("NU se poate asa ceva!")
        break
