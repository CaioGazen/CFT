from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path
import pygame
from xml.dom import minidom
from time import sleep
import numpy as np
from sympy import *
from scipy.integrate import quad


# read the SVG file
doc = minidom.parse('drawing.svg')
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
doc.unlink()

#svgpath =  path_strings[1]
svgpath = """m 76,232.24998 c 81.57846,-49.53502 158.19366,-20.30271 216,27 61.26714,
59.36905 79.86223,123.38417 9,156 
-80.84947,31.72743 -125.19991,-53.11474 -118,-91 v 0 """
path = parse_path(svgpath)

n_vetores = 10

def calcular_c(n, t):
    
    return ((path.point(t) * np.exp(-n * 2 *np.pi * 1j *t )))

def test(x):
    return (np.sqrt((x ** 4) + 1))


def midpoint(func, fn, a, b, n):
    if n % 2 != 0: raise Exception("n não é par")

    soma = 0
    deltaX = (b - a)/n
    pos_atual = a + (deltaX/2)

    for i in range(n):
        soma += deltaX * func(n, pos_atual)
        pos_atual += deltaX

    return (soma)

cn = []
for n in range((n_vetores // 2) * -1, (n_vetores // 2) + 1, 1):
    cn.append((n, midpoint(calcular_c, n, 0, 1, 1000)))

print (cn)
    
def soma_vetores(t):
    soma = 0

    for n, c in cn:
    #n ,c = cn[6]
        soma += c * np.exp(-n * 2 * np.pi * 1j * t)

    return soma




#for n in range(n_vetores//2 * - 1, n_vetores//2 + 1):
#
#
#    x = Symbol('x')
#    print(integrate((f(x)*np.exp(-n*2*np.pi*1j*x)), 0, 1))
n = 1

#print(quad((f(x) * exp(-n*2*np.pi*1j*x)), 0, 1))


pygame.init()                                  # init pygame
surface = pygame.display.set_mode((1000,1000))   # get surface to draw on
surface.fill(pygame.Color('white'))            # set background to white

#pygame.draw.aalines( surface,pygame.Color('blue'), False, pts)  # False is no closing
#pygame.display.update() # copy surface to display

def circulo(t):
    return np.exp(t * 1j)

index = 0
while True:  # loop to wait till window close
    #if index == 100: 
    #    index = 0 
    #    surface.fill(pygame.Color('white'))

    now = soma_vetores(index/100)

    pygame.draw.circle(surface, (255, 0, 0), ((now.real/10) + 500, (now.imag/10) + 500), 1)
    pygame.display.update() # copy surface to display   


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    index += 0.01