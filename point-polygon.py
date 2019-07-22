from math import atan2, pi, acos, sqrt
from point import Point
from polygon import Polygon
import pygame
import time
from represent import representLine, representPolygon

#MÉTODO 1(Area2) PARA DETERMINAR SI UN PUNTO ESTÁ DENTRO DE UN POLÍGONO
#Aplicable tanto a polígonos convexos
def Area2(a,b,c):
    area = (b.x-a.x)*(c.y-a.y)-(c.x-a.x)*(b.y-a.y)
    if(area>0): return True
    if(area<0): return False
    if(area == 0): return None

#MÉTODO 2(sumRadianAngles) PARA DETERMINAR SI UN PUNTO ESTÁ DENTRO DE UN POLÍGONO
#Aplicable tanto a polígonos cóncavos como convexos.

#Suma de ángulos (con signo). 2Pi = Punto interno; Pi = Punto del perímetro; 0 = Punto externo
def sumRadianAngles(polygon, point):
    #Este método devolverá el valor de angle
    angle = ["vertice","interior", "exterior", "ns"]
    suma = 0 #lista de segmentos punto a vertice del poligono
    m = len(polygon.lista)-1
    for i in polygon.lista:
        #Primero compruebo que el punto no es un vértice del polígono
        if(point.x == i.x and point.y == i.y):
            print("El ", point," es un vertice")
            return angle[0]
    for i in range(m):
        #Calculo los lados del triangulo formado por el punto y dos vertices del triangulo
        #y aplico el teorema del coseno para calcular el ángulo`que forma el punto con cada segmento del poligono
        a = sqrt((point.x-polygon.lista[i].x)**2+(point.y-polygon.lista[i].y)**2)
        b = sqrt((point.x-polygon.lista[i+1].x)**2+(point.y-polygon.lista[i+1].y)**2)
        c = sqrt((polygon.lista[i].x - polygon.lista[i+1].x)**2 + (polygon.lista[i].y-polygon.lista[i+1].y)**2)
        if(b != 0 and a!=0):
            angulo = acos((a**2+b**2-c**2)/(2*a*b))
        else:
            angulo = acos(0)
        #Cambio el signo del ángulo calcula cuando el punto quede a la derecha del segmento para compensar signos
        if(Area2(point, polygon.lista[i], polygon.lista[i+1])==False):
            angulo =-angulo
        #print(angulo)
        suma = suma + angulo
    last_a = sqrt((point.x-polygon.lista[m].x)**2+(point.y-polygon.lista[m].y)**2)
    last_b = sqrt((point.x-polygon.lista[0].x)**2+(point.y-polygon.lista[0].y)**2)
    last_c = sqrt((polygon.lista[m].x - polygon.lista[0].x)**2 + (polygon.lista[m].y-polygon.lista[0].y)**2)
    if(last_a != 0 and last_b != 0):
        last_angulo = acos((last_a**2+last_b**2-last_c**2)/(2*last_a*last_b))
    else:
        last_angulo = acos(0)
    if(Area2(point, polygon.lista[m], polygon.lista[0])== False):
        last_angulo = -last_angulo
    #print(last_angulo)
    suma = suma + last_angulo
    #print("La suma de los angulos es: ", suma)
    if (-0.05< suma <0.05):
        print("El ", point," es exterior")
        return angle[2]
    elif(2*pi-0.05 <suma <2*pi+0.05):
        print("El ", point," es interior")
        return angle[1]
    else:
        print("No estoy calculando bien esta suma de angulos")
        return angle[3]

######################### TEST SUMA RADIAN ANGLES ##########################
b_a = Point(100, 200)
b_b = Point(100, 100)
b_c = Point(200, 100)
b_d = Point(150, 150) #(250, 150) convexo
b_e = Point(200, 200)
b=Polygon()
b.add(b_a)
b.add(b_b)
b.add(b_c)
b.add(b_d)
b.add(b_e)
p1 = Point(235, 115)
p2 = Point(140, 150)
p3 = Point(100, 100)
p4 = Point(100, 150)

angle = sumRadianAngles(b, p1)
angle = sumRadianAngles(b, p2)
angle = sumRadianAngles(b, p3)
angle = sumRadianAngles(b, p4)
############################ REPRESENTACION #################################
pygame.init()
#Defino la altura y anchura de la ventana
size = [400, 300]
BLUE = ( 0, 0, 255) #defino el color en formato RGB
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode(size)
poligono_b = []
for i in b.lista:
    i = [i.x, i.y]
    poligono_b.append(i)
representPolygon(screen, BLUE, poligono_b)
punto1_v1 = [p1.x, p1.y+5]
punto1_v2 = [p1.x, p1.y-5]
punto1_h1 = [p1.x+5, p1.y]
punto1_h2 = [p1.x-5, p1.y]
punto2_v1 = [p2.x, p2.y+5]
punto2_v2 = [p2.x, p2.y-5]
punto2_h1 = [p2.x+5, p2.y]
punto2_h2 = [p2.x-5, p2.y]
punto3_v1 = [p3.x, p3.y+5]
punto3_v2 = [p3.x, p3.y-5]
punto3_h1 = [p3.x+5, p3.y]
punto3_h2 = [p3.x-5, p3.y]
punto4_v1 = [p4.x, p4.y+5]
punto4_v2 = [p4.x, p4.y-5]
punto4_h1 = [p4.x+5, p4.y]
punto4_h2 = [p4.x-5, p4.y]
representLine(screen, RED, punto1_v1, punto1_v2)
representLine(screen, RED, punto1_h1, punto1_h2)
representLine(screen, GREEN, punto2_v1, punto2_v2)
representLine(screen, GREEN, punto2_h1, punto2_h2)
representLine(screen, PURPLE, punto3_v1, punto3_v2)
representLine(screen, PURPLE, punto3_h1, punto3_h2)
representLine(screen, WHITE, punto4_v1, punto4_v2)
representLine(screen, WHITE, punto4_h1, punto4_h2)
pygame.display.flip()
time.sleep(8.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
