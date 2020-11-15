def merge_sort(array, sorted_array, left, right):

    countInv = 0
    if left < right:
        mid = (left + right) // 2
        countInv += merge_sort(array, sorted_array, left, mid)
        countInv += merge_sort(array, sorted_array, mid + 1, right)
        countInv += merge(array, sorted_array, left, mid, right)
    return countInv

def merge(array, sorted_array, left, mid, right):
    i = left
    k = left
    j = mid + 1
    countInversions = 0

    while i <= mid and j <= right:
        if array[i] <= 2 * array[j]:
            sorted_array[k] = array[i]
            i = i + 1
            k = k + 1
        else:
            countInversions += (mid - i + 1)
            sorted_array[k] = array[j]
            k = k + 1
            j = j + 1

    while i <= mid:
        sorted_array[k] = array[i]
        i = i + 1
        k = k + 1

    while j <= right:
        sorted_array[k] = array[j]
        j = j + 1
        k = k + 1

    for index in range(left, right):
        array[index] = sorted_array[index]

    return countInversions

if __name__ == '__main__':
    array = []
    with open('inversions.in') as fin:
        array = [int(x) for x in fin.readline().split()]
    fin.close()

    n = len(array)
    sorted_array = [None] * n
    result = merge_sort(array, sorted_array, 0, n - 1)
    print("Number of significant inversions: ", result)