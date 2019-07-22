from math import sqrt
from math import atan2
import pygame # necesito instalarlo: desde una linea de comandos -> pip install pygame
import time
from vector import Vector
from point import Point
from polygon import Polygon
from represent import representLine, representPolygon
from graham_convex_hull_v3 import Poligono

def dotProduct(v1, v2):
    return (v1.x*v2.x)+(v1.y*v2.y)

def projectPolygonOntoAxis(a, axis):
    numerador = dotProduct(a, axis)
    #print("numerador", numerador)
    denominador = sqrt(axis.x**2+axis.y**2)
    #print("denominador", denominador)
    if(denominador !=0 ):
        magnitud = numerador/denominador
    if(denominador ==0):
        magnitud = 0
    unitario = Vector(axis.x/sqrt(axis.x**2+axis.y**2), axis.y/sqrt(axis.x**2+axis.y**2), (0,0))
    projection = (magnitud*unitario.x, magnitud*unitario.y)
    return projection, magnitud


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
    vectors_axis_a = pol_a.getSides()
    vectors_axis_b = pol_b.getSides()
    print("vectors_axis_a", vectors_axis_a)
    print("vectors_axis_b", vectors_axis_b)
    vectors_a = pol_a.getSides()
    vectors_b = pol_b.getSides()
    print("vectors_a", vectors_a)
    print("vectors_b", vectors_b)
#3- Aplico SAT para detectar colisiones
#3.1 - Proyeccion de todos los lados de cada poligono sobre cada eje
    array_ejes = [] #Array de ejes de separacion
    for i in range(len(vectors_axis_a)):
        for j in range(len(vectors_a)):
            (projection_a, magnitud) = projectPolygonOntoAxis(vectors_a[j], vectors_axis_a[i])
        for k in range(len(vectors_b)):
            (projection_b, magnitud) = projectPolygonOntoAxis(vectors_b[k], vectors_axis_a[i])
            print("Axis: ", vectors_axis_a[i])
            print("Projection_a is: ", projection_a[0], projection_a[1], magnitud)
            print("Projection_b is: ", projection_b[0], projection_b[1], magnitud)
            #print("En esta iteracion el eje de sepacion es: ", ejeSeparacion)
            #array_ejes.append(ejeSeparacion)
    for i in range(len(vectors_axis_b)):
        for j in range(len(vectors_a)):
            projection_a = projectPolygonOntoAxis(vectors_a[j], vectors_axis_b[i])
        for k in range(len(vectors_b)):
            projection_b = projectPolygonOntoAxis(vectors_b[k], vectors_axis_b[i])
            print("Axis: ", vectors_axis_b[i])
            print("Projection_a is: ", projection_a[0], projection_a[1])
            print("Projection_b is: ", projection_b[0], projection_b[1])
            #print("En esta iteracion el eje de sepacion es: ", ejeSeparacion[2])
            #array_ejes.append(ejeSeparacion)
    return pol_a, pol_b, array_ejes

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
(pol_a, pol_b, array_ejes) = convexHull_SAT(a, b)
print("Los ejes de separacion estan definidos por los siguientes vectores directores: ", array_ejes)

######## Representación polígonos ##########

pygame.init()
#Defino la altura y anchura de la ventana
size = [400, 300]
BLUE = ( 0, 0, 255) #defino el color en formato RGB
GREEN = (0, 255, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode(size)
poligono_a = []
for i in a.lista:
    i = [i.x, i.y]
    poligono_a.append(i)
representPolygon(screen, BLUE, poligono_a)
poligono_b = []
for i in b.lista:
    i = [i.x, i.y]
    poligono_b.append(i)
representPolygon(screen, BLUE, poligono_b)
array_polA = []
for i in pol_a.lista:
    i = [i.x, i.y]
    array_polA.append(i)
representPolygon(screen, GREEN, array_polA)
array_polB = []
for i in pol_b.lista:
    i = [i.x, i.y]
    array_polB.append(i)
representPolygon(screen, GREEN, array_polB)
pygame.display.flip()
time.sleep(5.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
