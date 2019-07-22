from math import sqrt
from point import Point

class Vector:
    def __init__(self, point_i, point_f):
        self.point_i = point_i
        self.point_f = point_f
        self.vector = (point_f.x - point_i.x, point_f.y - point_i.y)

    #representación
    def __repr__(self):
        return "".join(["Vector(", str(self.vector[0]), ",", str(self.vector[1]), ") Ori: ", str(self.point_i), "Target: ", str(self.point_f)])

    def crescent(self):
        direction = ["v_pos", "v_neg", "crescent", "decrescent", "h_pos", "h_neg"]
        if(self.vector[0]==0 and self.vector[1]>0): return direction[0]
        if(self.vector[0]==0 and self.vector[1]<0): return direction[1]
        if (self.vector[1]>0): return direction[2]
        if (self.vector[1]<0): return direction[3]
        if(self.vector[1]==0 and self.vector[0]>0):return direction[4]
        if(self.vector[1]==0 and self.vector[0]<0): return direction[5]

    def dotProduct(v1, v2):
        return (v1.vector[0]*v2.vector[0])+(v1.vector[1]*v2.vector[1])

    def perpendicular(self):
        return Vector(- self.vector[1], self.vector[0])

    def unit(self):
        unitario = Vector(self.vector[0]/sqrt((self.vector[0])**2+(self.vector[1])**2), self.vector[1]/sqrt((self.vector[0])**2+(self.vector[1])**2))
        return unitario
