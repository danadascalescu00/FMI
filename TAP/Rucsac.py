class Object:
    def __init__(self, id, cost, weight):
        self.id = id
        self.cost = cost
        self.weight = weight
    def __repr__(self):
        return "Object " + str(self.id) + ":(" + str(self.cost) + " " + str(self.weight) + ")"

costs, weights = [], []
with open("rucsac.txt") as fin:
    n, G = [int(x) for x in next(fin).split()]
    costs = [int(x) for x in fin.readline().split()]
    weights= [int(x) for x in fin.readline().split()]
fin.close()

objects = [None] * n

for i in range(n):
    objects[i] = Object(i + 1, int(costs[i]), int(weights[i]))

objects = sorted(objects, key = lambda o:o.cost/o.weight, reverse=True)

g, i, Total_Cost = 0, 0, 0

while i < n  and g < G:
    if objects[i].weight + g <= G:
        g += objects[i].weight
        Total_Cost += objects[i].cost
        print(objects[i])
        i = i + 1
    else:
        cost_last = objects[i].cost/objects[i].weight * (G - g)
        Total_Cost += cost_last
        print(Object(objects[i].id, cost_last, G - g))
        g = G

print(Total_Cost)
