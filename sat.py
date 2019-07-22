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
    #print("proys: ", projection_a, projection_b)
    if(projection_a[1].x>projection_b[0].x or projection_a[1].x==projection_b[0].x):
        return str("collision")
    if(projection_a[1].x<projection_b[0].x):
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

def projectPolygonOne(polygon, axis):
    unitario = (axis.vector[0]/sqrt((axis.vector[0])**2+(axis.vector[1])**2), axis.vector[1]/sqrt((axis.vector[0])**2+(axis.vector[1])**2))
    all_polygon_projections_min = []
    all_polygon_projections_max = []
    seg_ini = 0.0
    seg_fin = 0.0
    sides = polygon.getSides()
    for i in range(len(sides)):
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
        #Set the points of the projection segments in order
        arg1 = axis.point_i
        arg2 = Point(magnitud*unitario[0], magnitud*unitario[1])

        if(sides[i].point_i.x>sides[i].point_f.x):
            seg_ini = arg2
            seg_fin = arg1
        else:
            seg_ini = arg1
            seg_fin = arg2
        #Saving all projections (min-max)points
        all_polygon_projections_min.append(seg_ini)
        all_polygon_projections_max.append(seg_fin)
    #print("All polygon projections min", all_polygon_projections_min, "\n", "All polygon projections max", all_polygon_projections_max)
    projection = [getMin(all_polygon_projections_min), getMax(all_polygon_projections_max)]
    return projection

def projectPolygonTwo(polygon, axis):
    unitario = (axis.vector[0]/sqrt((axis.vector[0])**2+(axis.vector[1])**2), axis.vector[1]/sqrt((axis.vector[0])**2+(axis.vector[1])**2))
    all_polygon_projections_min = []
    all_polygon_projections_max = []
    seg_ini = 0.0
    seg_fin = 0.0
    sides = polygon.getSides()
    for i in range(len(sides)):
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
        #Set the points of the projection segments in order
        arg1 = axis.point_i
        arg2 = Point(magnitud*unitario[0], magnitud*unitario[1])

        if(sides[i].point_i.x>sides[i].point_f.x):
            seg_ini = arg2
            seg_fin = arg1
        else:
            seg_ini = arg1
            seg_fin = arg2
        #Saving all projections (min-max)points
        all_polygon_projections_min.append(seg_ini)
        all_polygon_projections_max.append(seg_fin)
    #print("All polygon projections min", all_polygon_projections_min, "\n", "All polygon projections max", all_polygon_projections_max)
    projection = [getMin(all_polygon_projections_min), getMax(all_polygon_projections_max)]
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
    vectors_a = pol_a.getSides()
    vectors_b = pol_b.getSides()
    print("vectors_a", vectors_a)
    print("vectors_b", vectors_b)
    vectors_axis_a=[]
    vectors_axis_b=[]
    for i in vectors_a:
        print("vector", i)
        v = i.perpendicular()
        vectors_axis_a.append(v)
    for i in vectors_b:
        v= i.perpendicular()
        vectors_axis_b.append(v)
    print("vectors_axis_a", vectors_axis_a)
    print("vectors_axis_b", vectors_axis_b)
#3- Aplico SAT para detectar colisiones
#3.1 - Proyeccion de todos los lados de cada poligono sobre los ejes del pol_a
    array_str = [] #Array of collisions
    array_axis = [] #Array of separating axis
    array_projects = [] #Array of projections
    for i in range(len(vectors_axis_a)):
        print("//////////////////////////////////////////")
        print("Axis: ", vectors_axis_a[i])
        projection_a = projectPolygonOne(pol_a, vectors_axis_a[i])
        projection_b = projectPolygonTwo(pol_b, vectors_axis_a[i])
        print("- - - - - - - - - - - - - - - - - - - - - -")
        print("Projection_a is: ", projection_a)
        print("Projection_b is: ", projection_b)
        array_projects.append([projection_a, projection_b])
        gap = checkGap(projection_a, projection_b)
        array_str.append(gap)
        if(gap == "no collision"):
            if(vectors_axis_a[i].vector[1]!=0):
                m = - (vectors_axis_a[i].vector[0]/vectors_axis_a[i].vector[1])
                median = Point(((projection_b[0].x-projection_a[1].x)/2) + projection_a[1].x, vectors_axis_a[i].vector[1])
                n = median.y - m*median.x
                separatingAxis_inf = [(20-n)/m, 20]
                separatingAxis_sup = [(200-n)/m, 200]
            if(vectors_axis_a[i].vector[0]==0 or vectors_axis_a[i].vector[1]==0):
                median = Point(((projection_a[1].x-projection_b[0].x)/2) + projection_a[1].x, vectors_axis_a[i].vector[1])
                separatingAxis_inf = [((projection_a[1].x-projection_b[0].x)/2) + projection_a[1].x, 22]
                separatingAxis_sup = [((projection_a[1].x-projection_b[0].x)/2) + projection_a[1].x, 200]
            print("Median", median, "separatingAxis_inf", separatingAxis_inf, "separatingAxis_sup", separatingAxis_sup)
            sAxis = [separatingAxis_inf, separatingAxis_sup]
            array_axis.append(sAxis)

#3.2 - Proyeccion de todos los lados de cada poligono sobre los ejes del pol_b
    for i in range(len(vectors_axis_b)):
        print("//////////////////////////////////////////")
        print("Axis: ", vectors_axis_b[i])
        projection_a = projectPolygonTwo(pol_a, vectors_axis_b[i])
        projection_b = projectPolygonOne(pol_b, vectors_axis_b[i])
        print("- - - - - - - - - - - - - - - - - - - - - -")
        print("Projection_a is: ", projection_a)
        print("Projection_b is: ", projection_b)
        array_projects.append([projection_a, projection_b])
        gap = checkGap(projection_a, projection_b)
        array_str.append(gap)
        if(gap == "no collision"):
            if(vectors_axis_b[i].vector[1]!=0):
                m = - (vectors_axis_b[i].vector[0]/vectors_axis_b[i].vector[1])
                median = Point(((projection_b[0].x-projection_a[1].x)/2) + projection_a[1].x, vectors_axis_b[i].vector[1])
                n = median.y - m*median.x
                separatingAxis_inf = [(20-n)/m, 20]
                separatingAxis_sup = [(200-n)/m, 200]
            if(vectors_axis_b[i].vector[0]==0 or vectors_axis_b.vector[1]):
                median = Point(((projection_a[1].x-projection_b[0].x)/2) + projection_a[1].x, vectors_axis_b[i].vector[1])
                separatingAxis_inf = [((projection_a[1].x-projection_b[0].x)/2) + projection_a[1].x, 22]
                separatingAxis_sup = [((projection_a[1].x-projection_b[0].x)/2) + projection_a[1].x, 200]
            print("Median", median, "separatingAxis_inf", separatingAxis_inf, "separatingAxis_sup", separatingAxis_sup)
            sAxis = [separatingAxis_inf, separatingAxis_sup]
            array_axis.append(sAxis)
    return pol_a, pol_b, array_str, array_projects, array_axis, long_axis

######## Test ########
#Defino mi box a
a_a = Point(100, 100)
a_b = Point(200, 100)
a_c = Point (150, 150)
a=Poligono()
a.add(a_a)
a.add(a_b)
a.add(a_c)

#defino mi box b
b_a = Point(250, 100)
b_b = Point(300, 100) #(265, 145) concavo
b_c = Point(300, 200)
b_d = Point(250, 200)
b=Poligono()
b.add(b_a)
b.add(b_b)
b.add(b_c)
b.add(b_d)

#compruebo si los poligonos que he creado colisionan
(pol_a, pol_b, array_str, array_projects, array_axis, long_axis) = convexHull_SAT(a, b)
print("Los ejes de separacion estan definidos por los siguientes vectores directores: ", array_str, "\n", array_axis)
print("long_axis", long_axis)
print("proyecciones :", array_projects)

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
representPolygon(screen, PURPLE, poligono_a)
poligono_b = []
for i in b.lista:
    i = [i.x, i.y]
    poligono_b.append(i)
representPolygon(screen, PURPLE, poligono_b)
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
representLine(screen, BLUE, long_axis[0], long_axis[1])
representLine(screen, BLUE, long_axis[2], long_axis[3])
representLine(screen, BLUE, long_axis[4], long_axis[5])
representLine(screen, RED, [array_projects[0][0][0].x,array_projects[0][0][0].y] , [array_projects[0][0][1].x, array_projects[0][0][1].y])
representLine(screen, RED,[array_projects[0][1][0].x,array_projects[0][1][0].y] , [array_projects[0][1][1].x, array_projects[0][1][1].y])
representLine(screen, WHITE, [array_projects[1][0][0].x,array_projects[1][0][0].y] , [array_projects[1][0][1].x, array_projects[1][0][1].y])
representLine(screen, WHITE,[array_projects[1][1][0].x,array_projects[1][1][0].y] , [array_projects[1][1][1].x, array_projects[1][1][1].y])
representLine(screen, GREEN, [array_projects[2][0][0].x,array_projects[2][0][0].y] , [array_projects[2][0][1].x, array_projects[2][0][1].y])
representLine(screen, GREEN,[array_projects[2][1][0].x,array_projects[2][1][0].y] , [array_projects[2][1][1].x, array_projects[2][1][1].y])


pygame.display.flip()
time.sleep(12.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
