from math import sqrt
from math import atan2
import random
import pygame # necesito instalarlo: desde una linea de comandos -> pip install pygame
import time
from vector import Vector
from point import Point
from polygon import Polygon
from represent import representLine, representPolygon
from graham_CH import Poligono

def checkGap(projection_a, projection_b):
    #Compruebo si B esta a la izq. de A y no colisionan
    if(projection_b[0]<projection_a[0] and projection_b[1]<projection_a[0]):
        gap = [projection_b[1], projection_a[0]]
        print("no collision  - 1", gap)
        return gap, str("no collision")
    #Compruebo si B esta a la izq. de A y colisionan
    if(projection_b[0]<projection_a[1] and projection_b[1]>projection_a[0]):
        gap = [0, 0]
        print("collision - 1")
        return gap, str("collision")
    #Compruebo si colisionan o no cuando A está a la izq. de B
    if (projection_a[0]<projection_b[0] and projection_a[1]<projection_b[0]) :
        gap =[projection_a[1], projection_b[0]]
        print("no collision", gap)
        return  gap, str("no collision")
    if (projection_a[0]<projection_b[0] and projection_a[1]>projection_b[0]):
        gap =[0, 0]
        print("collision")
        return  gap, str("collision")


def projectPolygon(polygon, axis):
    axis_module = sqrt((axis[0])**2+(axis[1])**2)
    vertex_vectors = []
    all_polygon_projections = []
    for v in range(len(polygon.lista)):
        vrx_vector = Vector(Point(0,0), polygon.lista[v])
        vertex_vectors.append(vrx_vector)
    for i in range(len(vertex_vectors)):
        #magnitud = dotProduct/module(axis)
        magnitud = ((vertex_vectors[i].vector[0]*axis[0])+
        (vertex_vectors[i].vector[1] *axis[1]))/axis_module
        #Set the points of the projection segments in order
        all_polygon_projections.append(magnitud)
    projection = [min(all_polygon_projections), max(all_polygon_projections)]
    return projection

def convexHull_SAT(a, b):
# 1- Calculo el convex hull de mis poligonos. Si los puntos del convex hull coinciden
# con los del poligono sé que es convex, sino, el poligno es concavo y mantengo el convex.
    new_a = a.grahamConvHull()
    new_b = b.grahamConvHull()
    pol_a = Polygon()
    pol_b = Polygon()
    for i in range(len(new_a)):
        pol_a.add(new_a[i])
    for i in range(len(new_b)):
        pol_b.add(new_b[i])

# 2- Calculo los ejes perpendiculares a los normales de los lados poligonos
    vectors_axis_a = pol_a.getPerpendSides()
    vectors_axis_b = pol_b.getPerpendSides()
    print("vectors_a", vectors_axis_a)
    print("vectors_b", vectors_axis_b)
    sat_axis_b = pol_b.getSides()
    sat_axis_a = pol_a.getSides()

#3- Aplico SAT para detectar colisiones
#3.1 - Proyeccion de todos los lados de cada poligono sobre los ejes del pol_a
    array_str = [] #Array of collisions
    array_sats = [] #Array of separating axis
    array_projects = [] #Array of projections
    for i in range(len(vectors_axis_a)):
        print("//////////////////////////////////////////")
        print("Axis: ", vectors_axis_a[i])
        projection_a = projectPolygon(pol_a, vectors_axis_a[i])
        projection_b = projectPolygon(pol_b, vectors_axis_a[i])
        print("- - - - - - - - - - - - - - - - - - - - - -")
        print("Projection_a is: ", projection_a)
        print("Projection_b is: ", projection_b)
        array_projects.append([projection_a, projection_b])
        (gap, str) = checkGap(projection_a, projection_b)
        array_str.append(str)
        if(str == "no collision"):
            unitario_x = vectors_axis_a[i][0]/sqrt((vectors_axis_a[i][0])**2+(vectors_axis_a[i][1])**2)
            unitario_y = vectors_axis_a[i][1]/sqrt((vectors_axis_a[i][0])**2+(vectors_axis_a[i][1])**2)
            print("projections_a[1] y b_[0] - 1")
            gapPoint = random.uniform(gap[0], gap[1])
            firstPoint =  Point(gapPoint*unitario_x, gapPoint*unitario_y)
            secondPoint_y = 400
            #Caso Vector vertical u horizontal
            if (sat_axis_a[i].vector[0] == 0 or sat_axis_a[i].vector[1] == 0):
                m = 0
                secondPoint_x = firstPoint.x
            else:
                m = sat_axis_a[i].vector[1]/sat_axis_a[i].vector[0]
                n = firstPoint.y - (firstPoint.x*m)
                secondPoint_x = (secondPoint_y-n)/m
            sAxis = [firstPoint, Point(secondPoint_x, secondPoint_y)]
            print("sAxis", sAxis)
            array_sats.append(sAxis)

#3.2 - Proyeccion de todos los lados de cada poligono sobre los ejes del pol_b
    for i in range(len(vectors_axis_b)):
        print("//////////////////////////////////////////")
        print("Axis: ", vectors_axis_b[i])
        projection_a = projectPolygon(pol_a, vectors_axis_b[i])
        projection_b = projectPolygon(pol_b, vectors_axis_b[i])
        print("- - - - - - - - - - - - - - - - - - - - - -")
        print("Projection_a is: ", projection_a)
        print("Projection_b is: ", projection_b)
        array_projects.append([projection_a, projection_b])
        (gap, str) = checkGap(projection_a, projection_b)
        array_str.append(str)
        if(str == "no collision"):
            unitario_x = vectors_axis_b[i][0]/sqrt((vectors_axis_b[i][0])**2+(vectors_axis_b[i][1])**2)
            unitario_y = vectors_axis_b[i][1]/sqrt((vectors_axis_b[i][0])**2+(vectors_axis_b[i][1])**2)
            print("projections_a[1] y b_[0] - 2")
            gapPoint = random.uniform(gap[0], gap[1])
            firstPoint =  Point(gapPoint*unitario_x, gapPoint*unitario_y)
            secondPoint_y = 400
            if (sat_axis_b[i].vector[0] == 0 or sat_axis_b[i].vector[1] == 0):
                m = 0
                secondPoint_x = firstPoint.x
            else:
                m = sat_axis_b[i].vector[1]/sat_axis_b[i].vector[0]
                n = firstPoint.x - (firstPoint.y*m)
                secondPoint_x = (secondPoint_y-n)/m
            sAxis = [firstPoint, Point(secondPoint_x, secondPoint_y)]
            print("sAxis", sAxis)
            array_sats.append(sAxis)
    return pol_a, pol_b, array_str, array_sats

######## Test ########
#Defino mi box a
a_a = Point(50, 50)
a_b = Point(75, 75)
a_c = Point (100, 50)
a_d = Point(100, 90)
a_e = Point(50, 90)

a=Poligono()
a.add(a_a)
a.add(a_b)
a.add(a_c)
a.add(a_d)
a.add(a_e)

#defino mi box b
b_a = Point(300, 200)
b_b = Point(325, 225)
b_c = Point(350, 200)
b_d = Point(325, 250)
b=Poligono()
b.add(b_a)
b.add(b_b)
b.add(b_c)
b.add(b_d)

#compruebo si los poligonos que he creado colisionan
(pol_a, pol_b, array_str, array_sats) = convexHull_SAT(a, b)
print("List of collisions: ", array_str)
print("Separating Axis are: ", array_sats)

######## Representación polígonos ##########

pygame.init()
#Defino la altura y anchura de la ventana
size = [500, 500]
BLUE = ( 0, 0, 255) #defino el color en formato RGB
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
screen = pygame.display.set_mode(size)
poligono_a = []
for i in a.lista:
    i = [i.x, i.y]
    poligono_a.append(i)
representPolygon(screen, WHITE, poligono_a)
poligono_b = []
for i in b.lista:
    i = [i.x, i.y]
    poligono_b.append(i)
representPolygon(screen, RED, poligono_b)
array_polA = []
for i in pol_a.lista:
    i = [i.x, i.y]
    array_polA.append(i)
representPolygon(screen, PURPLE, array_polA)
array_polB = []
for i in pol_b.lista:
    i = [i.x, i.y]
    array_polB.append(i)
representPolygon(screen, PURPLE, array_polB)
for i in range(len(array_sats)):
    representLine(screen, BLUE, [array_sats[i][0].x, array_sats[i][0].y], [array_sats[i][1].x, array_sats[i][1].y])
pygame.display.flip()
time.sleep(10.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
