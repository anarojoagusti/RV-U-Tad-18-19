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
    print("Projections: ", projection_a, projection_b)
    if(projection_a[1][0]>projection_b[0][0] or projection_a[1][0]==projection_b[0][0]):
        return str("collision")
    if(projection_a[1][0]<projection_b[0][0]):
        return str("no collision")

def dotProduct(v1, v2):
    return (v1.vector[0]*v2.vector[0])+(v1.vector[1]*v2.vector[1])

def getMin(point_list):
    miny=100000
    maxx=-100000
    menor=Point(maxx, miny)
    for j in range(len(point_list)):
        if point_list[j].y<miny:
            if point_list[j].x>menor.x:
                menor = point_list[j]
                miny=menor.y
                maxx=menor.x
            else:
                menor = point_list[j]
                miny=menor.y
    return menor

def getMax(point_list):
    miny=-100000
    maxx=100000
    mayor = Point(maxx, miny)
    for j in range(len(point_list)):
        if point_list[j].y>miny:
            if point_list[j].x<mayor.x:
                mayor = point_list[j]
                maxx=mayor.x
                miny=mayor.y
            else:
                mayor = point_list[j]
                miny=mayor.y
    return mayor

def projectPolygonOX(polygon, axis):
    polygon_projection = []
    projections = []
    seg_ini = 0.0
    seg_fin = 0.0
    unitario = (axis.vector[0]/sqrt((axis.vector[0])**2+(axis.vector[1])**2), axis.vector[1]/sqrt((axis.vector[0])**2+(axis.vector[1])**2))
    sides = polygon.getSides()
    for i in range(len(sides)):
        #print("Proyectando el ", sides[i].vector)
        #print("El vector del eje de proyeccion es: ", axis.vector, axis.point_ini, axis.point_fin)
        #module of the proyected vector
        c = sqrt(sides[i].vector[0]**2+sides[i].vector[1]**2)
        #module of the resulting vector a-c
        b = sqrt((sides[i].vector[0]-axis.vector[0])**2+(sides[i].vector[1]-axis.vector[1])**2)
        #module of the projection vector
        a = sqrt(axis.vector[0]**2+axis.vector[1]**2)
        if(b==0):
            cosAlfa = 1
        else:
            #Cosine Theorem
            cosAlfa = ((c**2)-(b**2)-(a**2))/(-2*a*b)
        #magnitud = Projection = Module of the proyected vector(c) * cosine of the a-c angle
        magnitud = c*cosAlfa
        print("magnitudes")
        if(sides[i].crescent() == "v_pos" or sides[i].crescent() == "v_neg"):
            sideProj = Point(sides[i].point_i.x, magnitud*unitario[1])
        if(sides[i].crescent() == "h_neg"):
            sideProj = Point((magnitud+sides[i].point_i.x)*unitario[0], magnitud*unitario[1])
        if(sides[i].crescent() == "h_pos"):
            sideProj = Point((sides[i].point_i.x- magnitud)*unitario[0], magnitud*unitario[1])
        projections.append(sideProj)
    print("SideProj", projections)
    for i in range(len(projections)):
        minix = 100000;
        miniy = 0;
        mini = Point(minix, miniy)
        if projections[i].x<mini.x:
            mini = projections[i]
            minix = mini.x
            miniy = mini.y
        return mini
    for i in range(len(projections)):
        maxix = 0;
        maxiy = -100000;
        maxi = Point(maxix, maxiy)
        if projections[i].x>maxi.x:
            maxi = projections[i]
            maxix = maxi.x
            maxiy = maxi.y
        return maxi
    polygon_projection = [mini, maxi]
    print("Polygon_proyection", polygon_projection)
    return polygon_projection

def projectPolygonOY(polygon, axis):
    polygon_projection = []
    projections = []
    seg_ini = 0.0
    seg_fin = 0.0
    unitario = (axis.vector[0]/sqrt((axis.vector[0])**2+(axis.vector[1])**2), axis.vector[1]/sqrt((axis.vector[0])**2+(axis.vector[1])**2))
    sides = polygon.getSides()
    for i in range(len(sides)):
        #print("Proyectando el ", sides[i].vector)
        #print("El vector del eje de proyeccion es: ", axis.vector, axis.point_ini, axis.point_fin)
        #module of the proyected vector
        c = sqrt(sides[i].vector[0]**2+sides[i].vector[1]**2)
        #module of the resulting vector a-c
        b = sqrt((sides[i].vector[0]-axis.vector[0])**2+(sides[i].vector[1]-axis.vector[1])**2)
        #module of the projection vector
        a = sqrt(axis.vector[0]**2+axis.vector[1]**2)
        if(b==0):
            cosAlfa = 1
        else:
            #Cosine Theorem
            cosAlfa = ((c**2)-(b**2)-(a**2))/(-2*a*b)
        #magnitud = Projection = Module of the proyected vector(c) * cosine of the a-c angle
        magnitud = c*cosAlfa
        if(sides[i].crescent() == "h_pos" or sides[i].crescent() == "h_neg"):
            sideProj = Point(magnitud*unitario[0], sides[i].point_i.y)
        if(sides[i].crescent() == "v_pos"):
            sideProj = Point(magnitud*unitario[0], (magnitud+sides[i].point_f.y)*unitario[1])
        if(sides[i].crescent() == "v_neg"):
            sideProj = Point(magnitud*unitario[0], (sides[i].point_i.y- magnitud)*unitario[1])
        projections.append(sideProj)
    print("SideProj", projections)
    for i in range(len(projections)):
        mini = Point(0, 100000)
        if projections[i].y<mini.y:
            mini = projections[i]
    for i in range(len(projections)):
        maxi = Point(0, -100000)
        if projections[i].y>maxi.y:
            maxi = projections[i]
        return mini, maxi
    polygon_projection = [mini, maxi]
    print("Polygon_proyection", polygon_projection)
    return polygon_projection
"""        #Set the points of the projection segments in order
        if (sides[i].crescent() == "crescent"):
            seg_ini = Point((magnitud+axis.point_ini.x)*unitario[0], (magnitud+axis.point_ini.y)*unitario[1])
            seg_fin = Point(sides[i].point_ini.x*unitario[0], sides[i].point_ini.y*unitario[1])
        if (sides[i].crescent() == "decrescent"):
            seg_ini = Point(sides[i].point_ini.x*unitario[0], sides[i].point_ini.y*unitario[1])
            seg_fin = Point((magnitud+axis.point_ini.x)*unitario[0], (magnitud+axis.point_ini.y)*unitario[1])
        if (sides[i].crescent() == "constant_pos"):
            seg_ini = Point(sides[i].point_ini.x*unitario[0], sides[i].point_ini.y*unitario[1])
            seg_fin = Point(sides[i].point_fin.x*unitario[0], sides[i].point_fin.y*unitario[1])
        if (sides[i].crescent() == "constant_neg"):
            seg_fin = Point(sides[i].point_ini.x*unitario[0], sides[i].point_ini.y*unitario[1])
            seg_ini = Point(sides[i].point_fin.x*unitario[0], sides[i].point_fin.y*unitario[1])
        if (sides[i].crescent() == "perpend"):
            seg_ini = Point(sides[i].point_ini.x*unitario[0], sides[i].point_ini.y*unitario[1])
            seg_fin = Point(sides[i].point_ini.x*unitario[0], sides[i].point_ini.y*unitario[1])
        #Saving all projections (min-max)points
        all_polygon_projections_min.append(seg_ini)
        all_polygon_projections_max.append(seg_fin)
    print("All polygon projections min", all_polygon_projections_min, "\n", "All polygon projections max", all_polygon_projections_max)
    projection = (getMin(all_polygon_projections_min), getMax(all_polygon_projections_max))"""

def axisAlignedBoundingBoxes(a, b):
#1- Genero los Boxes para los poligonos
    box_a = a.boundingBox()
    box_b = b.boundingBox()

#2 - Aplico SAT para detectar colisiones
    axis_x = Vector(Point(0,0), Point(400,0))
    axis_y = Vector(Point(0,0), Point(0,300))
#3.1 - Proyeccion de todos los lados de cada poligono sobre los ejes del pol_a
    array_str = [] #Array of collisions
    array_axis = None #Array of separating axis
    print("////////////////////////////////////////////////////////////")
    print("Axis: ", axis_x)
    projection_a_x = projectPolygonOX(box_a, axis_x)
    projection_b_x = projectPolygonOX(box_b, axis_x)
    print("Projection_a on OX:", projection_a_x)
    print("Projection_b on OX:", projection_b_x)
    print("////////////////////////////////////////////////////////////")
    print("Axis: ", axis_y)
    projection_a_y = projectPolygonOY(box_a, axis_y)
    projection_b_y = projectPolygonOY(box_b, axis_y)
    print("Projection_a on OY:", projection_a_y)
    print("Projection_b on OY:", projection_b_y)
    gap = checkGap(projection_a_x, projection_b_x)
    array_str.append(gap)
    """if(gap == "no collision"):
        if(axis.vector[1] ==0 ):
            rand_point = [random.randint(projection_a[1][0], projection_b[0][0]), random.randint(0,10)]
            second_point = [rand_point[0], random.randint(280,300)]
        if(axis.vector[0] ==0 ):
            rand_point = [random.randint(0,10), random.randint(projection_a[1][1], projection_b[0][1])]
            second_point = [random.randint(380,400), rand_point[0]]
        array_axis = [rand_point, second_point]"""
        #return array_str, array_axis
    return box_a, box_b, projection_a, projection_b




############################ Test ##################################

#Defino mi box a
a_a = Point(100, 100)
a_b = Point(150, 100)
a_c = Point (150, 150)
a_d = Point(100, 150)
a=Polygon()
a.add(a_a)
a.add(a_b)
a.add(a_c)
a.add(a_d)
#defino mi box b
b_a = Point(200, 120)
b_b = Point(175, 145) #(265, 145) concavo
b_c = Point(220, 170)
b_d = Point(225, 145)
b=Polygon()
b.add(b_a)
b.add(b_b)
b.add(b_c)
#b.add(b_d)

#compruebo si los poligonos que he creado colisionan
(box_a, box_b, projection_a, projection_b)= axisAlignedBoundingBoxes(a, b)
print("////////////////////////////////////////////////////////////")

######## Representación polígonos ##########
#Genero una lista de puntos que formarán mis polígonog a y b
poligono_a=[]
poligono_a.append([a_a.x, a_a.y])
poligono_a.append([a_b.x, a_b.y])
poligono_a.append([a_c.x, a_c.y])
poligono_a.append([a_d.x, a_d.y])
#print(poligono_a)
poligono_b=[]
poligono_b.append([b_a.x, b_a.y])
poligono_b.append([b_b.x, b_b.y])
poligono_b.append([b_c.x, b_c.y])
#poligono_b.append([b_d.x, b_d.y])
#print(poligono_b)

pygame.init()
#Defino la altura y anchura de la ventana
size = [400, 300]
BLUE = ( 0, 0, 255) #defino el color en formato RGB
GREEN = (0, 255, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode(size)
representPolygon(screen, BLUE, poligono_a)
representPolygon(screen, BLUE, poligono_b)
array_boxA = []
for i in box_a.lista:
    i = [i.x, i.y]
    array_boxA.append(i)
representPolygon(screen, GREEN, array_boxA)
array_boxB = []
for i in box_b.lista:
    i = [i.x, i.y]
    array_boxB.append(i)
representPolygon(screen, GREEN, array_boxB)
"""if (sat_x != None):
    representLine(screen,sat_x[0], sat_x[1])
if (sat_y != None):
    representLine(screen,sat_y[0], sat_y[1])"""
pygame.display.flip()
time.sleep(5.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
