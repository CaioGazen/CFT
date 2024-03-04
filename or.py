
from __future__ import division  # we need floating division
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path
import pygame

""" demo of using a great python module svg.path by Lennart Regebro
    see site: https://pypi.org/project/svg.path/
    to draw svg in pygame
"""

from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path

svgpath = """m 76,232.24998 c 81.57846,-49.53502 158.19366,-20.30271 216,27 61.26714,
59.36905 79.86223,123.38417 9,156 
-80.84947,31.72743 -125.19991,-53.11474 -118,-91 v 0 """

path = parse_path(svgpath)

# svg.path point method returns a complex number p, p.real and p.imag can pull the x, and y
# # on 0.0 to 1.0 along path, represent percent of distance along path
n = 100  # number of line segments to draw

# pts = []
# for i in range(0,n+1):
#     f = i/n  # will go from 0.0 to 1.0
#     complex_point = path.point(f)  # path.point(t) returns point at 0.0 <= f <= 1.0
#     pts.append((complex_point.real, complex_point.imag))

# list comprehension version or loop above
pts = [ (p.real,p.imag) for p in (path.point(i/n) for i in range(0, n+1))]  

pygame.init()                                  # init pygame
surface = pygame.display.set_mode((700,600))   # get surface to draw on
surface.fill(pygame.Color('white'))            # set background to white

pygame.draw.aalines( surface,pygame.Color('blue'), False, pts)  # False is no closing
pygame.display.update() # copy surface to display

while True:  # loop to wait till window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()