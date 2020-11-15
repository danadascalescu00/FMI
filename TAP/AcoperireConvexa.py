import itertools

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def substract(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def distance(self, point):
        return (point.x - self.x)**2 + (point.y - self.y)**2

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

#calculates the cross product of vector v1 and vector v2.
def cros_product(v1,v2):
    return v1.x*v2.y - v1.y*v2.x

def direction(p1,p2,p3):
    return cros_product(p3.substract(p1),p2.substract(p1))

#Check if point P3 makes left turn at P2
def left(p1,p2,p3):
    return direction(p1,p2,p3) < 0

#Check if point P3 makes right turn at P2
def right(p1,p2,p3):
    return direction(p1,p2,p3) > 0

#Check if points P1, P2, P3 are collinear
def collinear(p1,p2,p3):
    return direction(p1,p2,p3) == 0

def dif_list(list1,list2):
    l_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return l_dif

def Jarvis_March(points):
    convex_hull = []

    #first step: find the "most left" point(The list is initialized with a point we are sure it is on the convex hull)
    a = min(points, key = lambda p : p.x)
    convex_hull.append(a)
    index = points.index(a)

    #The list is updated by determining the successor: "the most right” point.
    point1 = index
    while(True):
        point2 = (point1 + 1) % len(points)
        for i in range(len(points)):
            if i == point1:
                continue
            #find the greatest left turn or, in case of collinearity, the farthest point
            if right(points[point1], points[point2], points[i]) or (collinear(points[point1], points[point2], points[i]) and points[i].distance(points[point1])>points[point2].distance(points[point1])):
                point2 = i
        point1 = point2
        if point1 == index:
            break
        convex_hull.append(points[point2])

    return convex_hull

def main():
    Points = []
    I , J = [] , []

    with open("points.txt") as fin:
        for line in fin:
            x , y= [int(val) for val in line.split()]
            Points.append(Point(x,y))

    Points = sorted(Points, key = lambda p : p.x)
    A, B, C, D = Points[0], Points[1], Points[2], Points[3]

    if collinear(A,B,C) and collinear(B,C,D):
        print("Points A, B, C, D are collinear!")
        print("I = {", A , "," , D, "}")
        print("J = {", B , "," , C, "}")
    else:
        ConvexHull = Jarvis_March(Points)

        if len(ConvexHull) == len(Points):
            print("The convex hull of the four points is an quadrilateral.")
            print("I = {", ConvexHull[0], ",", ConvexHull[3],"}")
            print("J = {", ConvexHull[1], ",", ConvexHull[2],"}")
        else:
            print("The convex hull of the four points is a triangle.")
            print("I = {", ConvexHull[0], ",", ConvexHull[1], ",", ConvexHull[2], "}")
            J = dif_list(Points,ConvexHull)
            print("J = {",J[0],"}")

if __name__ == '__main__':
    main()