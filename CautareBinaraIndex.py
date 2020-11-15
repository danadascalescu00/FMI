# Se consideră un vector a cu n elemente distincte (numerotate de la 0), ordonate crescător.
# Implementaţi un algoritm de complexitate O(log n) pentru a determina, dacă există, un indice i cu
# a[i] = i
#Indexarea incepe de la 0

def BinarySearch(array, left, right):
    mid = left + (right - left) // 2
    if left < right:
        if array[mid] == mid:
            return 1
        elif array[mid] < mid:
            return BinarySearch(array, mid + 1, right)
        else:
            return BinarySearch(array, left, mid)
    else:
        return 0

if __name__ == '__main__':
    input = []
    with open('input.in') as fin:
        N = int(fin.readline())
        input = [int(x) for x in fin.readline().split()]

    if BinarySearch(input, 0, len(input)) == 1:
        print("Da")
    else:
        print("Nu")
