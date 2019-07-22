from math import sqrt
from math import atan2
import pygame # necesito instalarlo: desde una linea de comandos -> pip install pygame
import time

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init
        self.angulo=0

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ") ->",str(self.angulo)])
    def __lt__(self,p):
        if self.x<p.x:
            retorno =self
        else:
            if self.x == p.x:
                if self.y<p.x:
                    retorno= self
                else:
                    retorno = p
            else:
                retorno = p
        return retorno

def distance(a, b):
    x1=(a.x-b.x)**2
    x2=(a.y-b.y)**2
    return sqrt(x1+x2)

def angulo (p):
    return p.angulo

class Poligono:
    def __init__(self):
        self.lista=[]
        self._puntoInicial=Point(0,0)

    def add (self,p):
        self.lista.append(p)

    def popX (self, p):
        self.lista.pop(p)

    def __repr__(self):
        l=""
        for i in self.lista:
            l+= str(i)+"\n"
        return l
    def ordenaX (self):
        self.lista.sort()

    def ordenaGraham (self):
        for i in self.lista:
            i.angulo = atan2(i.y-self._puntoInicial.y,i.x-self._puntoInicial.x)
            #print(i.angulo)
        self.lista.sort(key=angulo)
        print("Puntos ordenados por angulos: ","\n",self.lista)
        return self.lista.sort(key=angulo)

    def puntoInicial(self):
        miny=100000
        maxx=-100000
        menor=Point(maxx,miny)
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

    def grahamConvHull(self):
        #Toma los puntos de la lista, ordenados por ángulo y devuelve la orientación
        #>0 left, <0 right, 0 co-linear
        def Area2(a,b,c):
            return (b.x-a.x)*(c.y-a.y)-(c.x-a.x)*(b.y-a.y)
            if (area > 0):
                return True
            if (area < 0):
                return False
            if (area == 0):
               return None

        # array_hull es mi pila de puntos
        array_hull = [self._puntoInicial, self.lista[1]]
        # incluyo en la primera posicion de la pila el punto inicial y el la segunda posición su consecutivo
        for i in self.lista[2:]:
            #Cuando tenga dos puntos iniciales, calculo el área del siguiente punto respecto a los
            #anteriores. Si es <=0, saco del array_hull el último elemento. Sino, lo añado.
            print("Puntos:", array_hull[-2], array_hull[-1], i)
            while Area2(array_hull[-2], array_hull[-1], i)<=0 :
                array_hull.pop()
                if len(array_hull)<2: break
            array_hull.append(i)
            print("Array actualizado:",array_hull)
        #return array_hull
        print("Puntos del Convex Hull:","\n",array_hull)
        pygame.init()
        #Defino la altura y anchura de la ventana
        size = [400, 300]
        screen = pygame.display.set_mode(size)
        BLUE = ( 0, 0, 255) #defino el color en formato RGB
        GREEN = (0, 255, 0)
        #Dibujo mi polígono uniendo con líneas azules de grosor 1 píxel los puntos
        #de lista. closed = True -> uno el último punto de lista con el primero.
        pol_repr=[]
        for i in self.lista:
            i = [i.x,i.y]
            pol_repr.append(i)
        pygame.draw.lines(screen, GREEN, True, pol_repr, 1)
        array_repr=[]
        for i in array_hull:
            i = [i.x,i.y]
            array_repr.append(i)
        pygame.draw.lines(screen, BLUE, True, array_repr, 1)
        pygame.display.flip()
        time.sleep(5.5) #necesario para no cerrar la pantalla inmediatamente
        pygame.quit()

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
a.grahamConvHull()
b.grahamConvHull()
