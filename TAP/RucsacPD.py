class Object:
    def __init__(self, id, weight, cost):
        self.id = id
        self.weight = weight
        self.cost = cost

    def __repr__(self):
        return "Object " + str(self.id) + ": (" + str(self.weight) + "," + str(self.cost) + ")"

def knapsack(G, n, objects):
    K = [[0 for x in range(G + 1)] for x in range(n + 1)]

    # Build table K[][] in bottom-up manner
    for i in range(1, n+1):
        for j in range(G+1):
            K[i][j] = K[i-1][j]
            if j >= objects[i-1].weight and K[i][j] < K[i-1][j - objects[i-1].weight] + objects[i-1].cost:
                K[i][j] = K[i-1][j - objects[i-1].weight] + objects[i-1].cost

    print("Costul total: ", K[n][G])

    while n != 0:
        if K[n][G] != K[n-1][G]:
            print(objects[n-1])
            G = G - objects[n-1].weight
        n = n - 1

if __name__ == '__main__':
    weights, costs = [], []
    with open("rucsacpd.txt") as fin:
        n, G = [int(x) for x in next(fin).split()]
        weights = [int(x) for x in fin.readline().split()]
        costs = [int(x) for x in fin.readline().split()]
    fin.close()

    objects = [None] * n
    for i in range(n):
        objects[i] = Object(i+1, weights[i], costs[i])

    knapsack(G, n, objects)
