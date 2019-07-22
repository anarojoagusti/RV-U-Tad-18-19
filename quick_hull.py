import math
import random
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init
        self.angle = 0

    def __repr__(self):
        return "".join(["[", str(self.x), ", ", str(self.y), "]"])


class Vector:

    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b
        self.vec = [point_b.x - point_a.x, point_b.y - point_a.y]

    def get_angle(self):
        return math.atan2(self.point_b.y - self.point_a.y, self.point_b.x - self.point_a.x)

    def __repr__(self):
        return "".join(["Vector(", str(self.vec[0]), ", ", str(self.vec[1]), ")"])


class Polygon:
    def __init__(self, point_list):
        self.point_list = point_list
        self.init_point = Point(0, 0)

    def getConvexHull(self):
        num_size = len(self.point_list)
        if num_size < 3:
            print("ConvexHull not possible \n")
            return
        polRes = Polygon([])
        min_x = 0
        max_x = 0

        for point_index in range(num_size):
            if self.point_list[point_index].x < self.point_list[min_x].x:
                min_x = point_index
            if self.point_list[point_index].x > self.point_list[max_x].x:
                max_x = point_index

        getQuickHull(self.point_list, num_size,
                     self.point_list[min_x], self.point_list[max_x], 1, polRes.point_list)
        getQuickHull(self.point_list, num_size,
                     self.point_list[min_x], self.point_list[max_x], -1, polRes.point_list)

        polRes.setInitPoint()
        polRes.orderPoints()

        return polRes

    def orderPoints(self):
        for point in self.point_list:
            vector = Vector(self.init_point, point)
            point.angle = vector.get_angle()

        self.point_list = sorted(self.point_list, key=getAngle)

    def setInitPoint(self):
        min_y = 10000
        max_x = -10000
        minor = Point(max_x, min_y)

        for point in self.point_list:
            if point.y < min_y:
                minor = point
                min_y = minor.y
                if point.x > minor.x:
                    max_x = minor.x
        self.init_point = minor

    def __repr__(self):
        return "".join(["Polygon(", str(self.point_list), ")"])


def getAngle(point):
    return point.angle


def getQuickHull(pol, num, pointA, pointB, side, polRes):
    ind = -1
    max_dist = 0

    for point in range(num):
        temp = lineDist(pointA, pointB, pol[point])
        if area2(pointA, pointB, pol[point]) == side:
            if temp > max_dist:
                ind = point
                max_dist = temp

    if ind == -1:
        if notExistPoint(polRes, pointA):
            polRes.append(pointA)
        if notExistPoint(polRes, pointB):
            polRes.append(pointB)
        return

    # Si no encuentra un punto que cumpla la condición de ComvexHull, se hacen las llamadas recursivas
    getQuickHull(pol, num, pol[ind], pointA, -
                 area2(pol[ind], pointA, pointB), polRes)
    getQuickHull(pol, num, pol[ind], pointB, -
                 area2(pol[ind], pointB, pointA), polRes)


def notExistPoint(point_list, point):
    found = True
    for p in point_list:
        if p.x == point.x and p.y == point.y:
            found = False
            return
    return found


def aux(point_a, point_b, point_c):
    return (point_c.y - point_a.y) * (point_b.x - point_a.x) - (point_b.y - point_a.y) * (point_c.x - point_a.x)


def lineDist(point_a, point_b, point_c):
    return abs(aux(point_a, point_b, point_c))


def area2(point_a, point_b, point_c):
    val = aux(point_a, point_b, point_c)
    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0


# ******************** INIT PROGRAM ******************
point_list = []
for x in range(10):
    point = Point(random.randint(-100, 100), random.randint(-100, 100))
    point_list.append(point)


polygon = Polygon(point_list)
convex_hull = polygon.getConvexHull()

print("POLYGON")
print(polygon)
print("CONVEX HULL")
print(convex_hull)

x_coor = []
y_coor = []

for point in polygon.point_list:
    x_coor.append(point.x)
    y_coor.append(point.y)

plt.plot(x_coor, y_coor, "bo")
x_coor = []
y_coor = []

convex_hull.point_list.append(convex_hull.point_list[0])

for point in convex_hull.point_list:
    x_coor.append(point.x)
    y_coor.append(point.y)

plt.plot(x_coor, y_coor, "ro-", linewidth=2, markersize=12)

plt.show()
