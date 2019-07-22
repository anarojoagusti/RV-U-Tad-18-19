import pygame # necesito instalarlo: desde una linea de comandos -> pip install pygame
import time

def representPolygon(screen, color, pol_repr):

    BLUE = ( 0, 0, 255) #defino el color en formato RGB
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    PURPLE = (255, 0, 255)
    pygame.draw.lines(screen, color, True, pol_repr, 2)


def representLine(screen, color, point_a, point_b):
    WHITE = (255, 255, 255)
    BLUE = ( 0, 0, 255) #defino el color en formato RGB
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    PURPLE = (255, 0, 255)
    pygame.draw.line(screen, color, point_a, point_b, 2)
