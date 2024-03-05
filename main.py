from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path
from xml.dom import minidom
import numpy as np
import pygame



# read the SVG file
doc = minidom.parse('drawing.svg')
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
doc.unlink()

svgpath =  path_strings[0]

path = parse_path(svgpath)

def path_func(t):
    p = path.point(t)
    return p

def calcular_c(n, t):
    return ((path_func(t) * (np.exp(-1* n * 2 *np.pi * 1j *t ))))


def midpoint(func, fn, a, b, n):
    if n % 2 != 0: raise Exception("n não é par")

    soma = 0
    deltaX = (b - a)/n
    pos_atual = a + (deltaX/2)

    for i in range(n):
        soma += deltaX * func(fn, pos_atual)
        pos_atual += deltaX

    return (soma)
    

def vetor_c(n_vetores):
    cn = []
    for n in range((n_vetores // 2) * -1, (n_vetores // 2) + 1, 1):
        cn.append((n, midpoint(calcular_c, n, 0, 1, 1000)))

    return cn

    
def soma_vetores(t, cn, scale):
    soma = 0
    vectors = [(0,0)]
    for n, c in cn:
        vector = c * np.exp(n * 2 * np.pi * 1j * t)
        soma += vector
        vectors.append(((vector.real) + vectors[len(vectors) - 1][0], (vector.imag)  + vectors[len(vectors) - 1][1]))
    
    vectors = (np.array(vectors)*scale) + 500
    return soma, vectors


def main():
    n_vetores = 200

    n = 1000
    pts = [ (p.real + 500,p.imag + 500) for p in (path.point(i/n) for i in range(0, n+1))]

    cn = vetor_c(n_vetores)
    scale = 0.8

    pygame.init()                                  # init pygame
    surface = pygame.display.set_mode((1000,1000))   # get surface to draw on
    surface.fill(pygame.Color('white'))            # set background to white
    points = []
    time = 0
    while True:  # loop to wait till window close
        if time > 1: 
            print("loop")
            time = 0
            surface.fill(pygame.Color('white'))

        surface.fill(pygame.Color('white'))
        
        #pygame.draw.aalines(surface,pygame.Color('black'), False, pts)


        now, vectors = soma_vetores(time, cn, scale)

        pygame.draw.aalines( surface,pygame.Color('blue'), False, vectors, 5)
        points.append(vectors[len(vectors) - 1])
        #pygame.draw.circle(surface, (255, 255, 0), (0,0), 100)
        for point in points:
            pygame.draw.circle(surface, (255, 0, 0), point, 1)
        
        pygame.display.update() # copy surface to display   


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        time += 0.0001


if __name__ == "__main__":
    main()