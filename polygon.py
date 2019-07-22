from point import Point
from math import atan2
from vector import Vector

class Polygon:
    def __init__(self):
        self.lista=[]
        self._puntoInicial=Point(0,0)
    def add (self,p):
        self.lista.append(p)
    def boundingBox(self):
        box = Polygon()
        leftop_point = self._leftop_()
        leftbottom_point = self._leftbottom_()
        rightop_point = self._rightop_()
        rightbottom_point = self._rightbottom_()
        print("max_izquierda_ point: ", leftop_point, " min_izquierda_point ", leftbottom_point, " max_derecha_point ", rightop_point,"min_derecha_point", rightbottom_point)
        if (leftbottom_point.x<leftop_point.x):
            leftx = leftbottom_point.x
        else:
            leftx = leftop_point.x
        if (rightbottom_point.x>rightop_point.x):
            rightx = rightbottom_point.x
        else:
            rightx = rightop_point.x
        if (leftop_point.y>rightop_point.y):
            topy = leftop_point.y
        else:
            topy = rightop_point.y
        if (leftbottom_point.y<rightbottom_point.y):
            bottomy = leftbottom_point.y
        else:
            bottomy = rightbottom_point.y

        base1 = Point(leftx, bottomy)
        base2 = Point(rightx, bottomy)
        alt1 = Point(rightx, topy)
        alt2 = Point(leftx, topy)
        box.add(base1)
        box.add(base2)
        box.add(alt1)
        box.add(alt2)
        return box
    def getSides(self):
        sides =[]
        m = len(self.lista)-1
        for i in range(len(self.lista)-1):
            side = Vector(self.lista[i], self.lista[i+1])
            sides.append(side)
        last_side = Vector(self.lista[m], self.lista[0])
        sides.append(last_side)
        #print("These are the vector sides of the polygon: ", sides)
        return sides

    def getPerpendSides(self):
        sides =[]
        perpendiculars = []
        m = len(self.lista)-1
        for i in range(len(self.lista)-1):
            side = Vector(self.lista[i], self.lista[i+1])
            sides.append(side)
        last_side = Vector(self.lista[m], self.lista[0])
        sides.append(last_side)
        #print("These are the vector sides of the polygon: ", sides)
        for i in range(len(sides)):
            perpendicular = (-sides[i].vector[1], sides[i].vector[0])
            perpendiculars.append(perpendicular)
        return perpendiculars

    def _leftbottom_(self):
        miny=100000
        maxx=-100000
        menor=Point(maxx, miny)
        for j in self.lista:
            if j.y<miny:
                if j.x>menor.x:
                    menor = j
                    miny=menor.y
                    maxx=menor.x
                else:
                    menor = j
                    miny=menor.y
        return menor
    def _leftop_(self):
        minx=100000
        maxy=100000
        mayor=Point(minx, maxy)
        for j in self.lista:
            if j.x<minx:
                if j.y<maxy:
                    mayor = j
                    maxy=mayor.y
                    minx=mayor.x
                else:
                    mayor = j
                    maxy=mayor.y
        return mayor
    def ordenaX (self):
        self.lista.sort()
    def popX (self, p):
        self.lista.pop(p)
    def __repr__(self):
        l=""
        for i in self.lista:
            l+= str(i)+"\n"
        return l
    def _rightbottom_(self):
        maxy=100000
        maxx=100000
        mayor = Point(maxx, maxy)
        for j in self.lista:
            if j.y<maxy:
                if j.x>mayor.x:
                    mayor = j
                    maxx=mayor.x
                    maxy=mayor.y
                else:
                    mayor = j
                    miny=mayor.y
        return mayor
    def _rightop_(self):
        miny=-100000
        maxx=100000
        mayor = Point(maxx, miny)
        for j in self.lista:
            if j.y>miny:
                if j.x<mayor.x:
                    mayor = j
                    maxx=mayor.x
                    miny=mayor.y
                else:
                    mayor = j
                    miny=mayor.y
        return mayor
