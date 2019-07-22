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
    if(projection_a[1]>projection_b[0] or projection_a[1]==projection_b[0]):
        return str("collision")
    if(projection_a[1]<projection_b[0]):
        return str("no collision")

def projectPolygon(polygon, axis):
    axis_module = sqrt((axis.vector[0])**2+(axis.vector[1])**2)
    vertex_vectors = []
    all_polygon_projections = []
    for v in range(len(polygon.lista)):
        vrx_vector = Vector(Point(0,0), polygon.lista[v])
        vertex_vectors.append(vrx_vector)
    for i in range(len(vertex_vectors)):
        #magnitud = producto Escalar
        magnitud = ((vertex_vectors[i].vector[0]*axis.vector[0])+(vertex_vectors[i].vector[1] *axis.vector[1]))/axis_module
        #Set the points of the projection segments in order
        all_polygon_projections.append(magnitud)
    projection = [min(all_polygon_projections), max(all_polygon_projections)]
    return projection

def axisAlignedBoundingBoxes(a, b):
#1- Genero los Boxes para los poligonos
    box_a = a.boundingBox()
    box_b = b.boundingBox()

#2 - Aplico SAT para detectar colisiones
    axis_x = Vector(Point(0,0), Point(400,0))
    axis_y = Vector(Point(0,0), Point(0,300))
#3.1 - Proyeccion de todos los lados de cada poligono sobre los ejes del pol_a
    array_str = [] #Array of collisions
    array_sats = [] #Array of separating axis
    print("////////////////////////////////////////////////////////////")
    print("Axis: ", axis_x)
    projection_a = projectPolygon(box_a, axis_x)
    projection_b = projectPolygon(box_b, axis_x)
    print("Projection_a on OX:", projection_a)
    print("Projection_b on OX:", projection_b)
    gap = checkGap(projection_a, projection_b)
    array_str.append(gap)
    if(gap == "no collision"):
        unitario_x = axis_x.vector[0]/sqrt((axis_x.vector[0])**2+(axis_x.vector[1])**2)
        unitario_y = axis_x.vector[1]/sqrt((axis_x.vector[0])**2+(axis_x.vector[1])**2)
        gapPoint = random.randint(projection_a[1], projection_b[0])
        firstPoint =  Point(gapPoint*unitario_x, gapPoint*unitario_y)
        secondPoint_y = 400
        #Caso Vector vertical u horizontal
        if (axis_x.vector[0] == 0 or axis_x.vector[1] == 0):
            m = 0
            secondPoint_x = firstPoint.x
        sAxis = [firstPoint, Point(secondPoint_x, secondPoint_y)]
        print("sAxis", sAxis)
        array_sats.append(sAxis)
    print("////////////////////////////////////////////////////////////")
    print("Axis: ", axis_y)
    projection_a = projectPolygon(box_a, axis_y)
    projection_b = projectPolygon(box_b, axis_y)
    print("Projection_a on OY:", projection_a)
    print("Projection_b on OY:", projection_b)
    gap = checkGap(projection_a, projection_b)
    array_str.append(gap)
    if(gap == "no collision"):
        unitario_x = axis_y.vector[0]/sqrt((axis_y.vector[0])**2+(axis_y.vector[1])**2)
        unitario_y = axis_y.vector[1]/sqrt((axis_y.vector[0])**2+(axis_y.vector[1])**2)
        gapPoint = random.randint(projection_a[1], projection_b[0])
        firstPoint =  Point(gapPoint*unitario_x, gapPoint*unitario_y)
        secondPoint_x = 400
        #Caso Vector vertical u horizontal
        if (axis_y.vector[0] == 0 or axis_y.vector[1] == 0):
            m = 0
            secondPoint_y = firstPoint.y
        sAxis = [firstPoint, Point(secondPoint_x, secondPoint_y)]
        print("sAxis", sAxis)
        array_sats.append(sAxis)
    return box_a, box_b, array_str, array_sats




############################ Test ##################################

#Defino mi box a
a_a = Point(100, 100)
a_b = Point(150, 100)
a_c = Point (150, 150)
a_d = Point(100, 150)
a_e = Point(130, 130)
a=Polygon()
a.add(a_a)
a.add(a_b)
a.add(a_c)
a.add(a_d)
a.add(a_e)
#defino mi box b
b_a = Point(200, 220)
b_b = Point(175, 245) #(265, 145) concavo
b_c = Point(220, 270)
b_d = Point(225, 245)
b=Polygon()
b.add(b_a)
b.add(b_b)
b.add(b_c)
#b.add(b_d)

#compruebo si los poligonos que he creado colisionan
(box_a, box_b, array_str, array_sats)= axisAlignedBoundingBoxes(a, b)
print("Number of collisions: ", array_str)
print("Separating Axis are: ", array_sats)
print("////////////////////////////////////////////////////////////")

######## Representación polígonos ##########
#Genero una lista de puntos que formarán mis polígonog a y b
poligono_a=[]
poligono_a.append([a_a.x, a_a.y])
poligono_a.append([a_b.x, a_b.y])
poligono_a.append([a_c.x, a_c.y])
poligono_a.append([a_d.x, a_d.y])
poligono_a.append([a_e.x, a_e.y])
#print(poligono_a)
poligono_b=[]
poligono_b.append([b_a.x, b_a.y])
poligono_b.append([b_b.x, b_b.y])
poligono_b.append([b_c.x, b_c.y])
#poligono_b.append([b_d.x, b_d.y])
#print(poligono_b)

pygame.init()
#Defino la altura y anchura de la ventana
size = [400, 400]
BLUE = ( 0, 0, 255) #defino el color en formato RGB
GREEN = (0, 255, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode(size)
representPolygon(screen, GREEN, poligono_a)
representPolygon(screen, GREEN, poligono_b)
array_boxA = []
for i in box_a.lista:
    i = [i.x, i.y]
    array_boxA.append(i)
representPolygon(screen, RED, array_boxA)
array_boxB = []
for i in box_b.lista:
    i = [i.x, i.y]
    array_boxB.append(i)
representPolygon(screen, RED, array_boxB)
for i in range(len(array_sats)):
    representLine(screen, BLUE, [array_sats[i][0].x, array_sats[i][0].y], [array_sats[i][1].x, array_sats[i][1].y])
pygame.display.flip()
time.sleep(5.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
