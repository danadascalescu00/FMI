import math

def distance(x1, y1, x2, y2):
    return (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)

def brute_force(points):
    min = 9e16

    for i in range(len(points) - 1):
        for j in range(i+1, len(points)):
            d = distance(points[i][0], points[i][1], points[j][0], points[j][1])
            if d < min:
                min = d
    return min

def cmap(points_Ox, points_Oy):
    delta_q = delta_r = delta_merge = delta_min = 9e16

    numPoints = len(points_Ox)
    if numPoints <= 3:
        return brute_force(points_Ox)
    else:
        mid = numPoints // 2

        Qx = points_Ox[:mid]
        Rx = points_Ox[mid:]

        midpoint = points_Ox[mid][0]
        Qy = list()
        Ry = list()
        for point in points_Oy:
            if point[0] <= midpoint:
                Qy.append(point)
            else:
                Ry.append(point)

        delta_q = cmap(Qx, Qy)
        delta_r = cmap(Rx, Ry)

        delta_min = min(delta_q, delta_r)

        delta_merge = cmap_merge(points_Ox, points_Oy, delta_min)

    return min(delta_min,delta_merge)

def cmap_merge(points_Ox, points_Oy, delta):
    numPoints = len(points_Ox)
    midpoint_Ox = points_Ox[numPoints//2][0]

    s_y = [point for point in points_Oy if midpoint_Ox - delta <= point[0] <= midpoint_Ox + delta]

    d = delta
    len_y = len(s_y)
    for i in range(len_y - 1):
        for j in range(i+1, min(i + 7, len_y)):
            dst = distance(s_y[i][0], s_y[i][1], s_y[j][0], s_y[j][1])
            if dst < d:
                d = dst
    return d

if __name__ == '__main__':
    points = []
    with open('cmap.in') as fin:
        N = int(fin.readline())
        for _ in range(N):
            x, y = [int(val) for val in next(fin).split()]
            points.append([x,y])
    fin.close()

    points = sorted(points, key = lambda p : p[0])
    points_Oy = sorted(points, key = lambda p : p[1])

    minDistance = math.sqrt(cmap(points, points_Oy))

    with open('cmap.out', 'w') as fout:
        print(minDistance, file=fout)