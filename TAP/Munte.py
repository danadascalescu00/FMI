#function that returns the peak element of the array based on binary search algorithm
def findMountainPeak(array, low, high):
    mid = low + (high - low) // 2

    if array[mid - 1] <= array[mid] and array[mid + 1] <= array[mid]:
        return mid
    elif array[mid] <= array[mid + 1]:
        return findMountainPeak(array, mid + 1, high)
    else:
        return findMountainPeak(array, low, mid - 1)

if __name__ == '__main__':
    input = []
    with open('munte.txt') as fin:
        input = [int(x) for x in fin.readline().split()]
    fin.close()

    n = len(input)
    index = findMountainPeak(input, 0, n - 1)
    print("Mountain peak: ", input[index])