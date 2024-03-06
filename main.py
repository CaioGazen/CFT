from svg.path import parse_path
from xml.dom import minidom
import numpy as np
import pygame


# read the SVG file
doc = minidom.parse("cube.svg")
path_strings = [path.getAttribute("d") for path in doc.getElementsByTagName("path")]
doc.unlink()

svgpath = path_strings[0]

path = parse_path(svgpath)


def path_func(t):
    p = path.point(t)
    return p


def calcular_c(n, t):
    return path_func(t) * (np.exp(-1 * n * 2 * np.pi * 1j * t))


def midpoint(func, fn, a, b, n):
    if n % 2 != 0:
        raise Exception("n não é par")

    soma = 0
    deltaX = (b - a) / n
    pos_atual = a + (deltaX / 2)

    for i in range(n):
        soma += deltaX * func(fn, pos_atual)
        pos_atual += deltaX

    return soma


def get_coefficients(n_vetores):
    cn = []
    for n in range((n_vetores // 2) * -1, (n_vetores // 2) + 1, 1):
        cn.append((n, midpoint(calcular_c, n, 0, 1, 1000)))

    return cn


def soma_vetores(t, cn, scale, x_offset, y_offset):
    vectors = [(0, 0)]
    for n, c in cn:
        vector = c * np.exp(n * 2 * np.pi * 1j * t)
        vectors.append(
            (
                (vector.real) + vectors[len(vectors) - 1][0],
                (vector.imag) + vectors[len(vectors) - 1][1],
            )
        )

    vectors = (np.array(vectors) * scale) + (x_offset, y_offset)
    return vectors


def main():
    window_size = 600
    x_offset = window_size / 2
    y_offset = window_size / 2
    scale = 15

    n_vectors = 100

    # original svg
    n_lines = 1000
    svg_points = [
        ((p.real * scale) + x_offset, (p.imag * scale) + y_offset)
        for p in (path.point(i / n_lines) for i in range(0, n_lines + 1))
    ]

    coefficients = get_coefficients(n_vectors)

    mag_vectors = []
    for n_lines, c in coefficients:
        x = c * np.exp(n_lines * 2 * np.pi * 1j * 1)
        mag_vectors.append(np.linalg.norm(x) * scale)

    pygame.init()  # init pygame
    surface = pygame.display.set_mode(
        (window_size, window_size)
    )  # get surface to draw on
    surface.fill(pygame.Color("white"))  # set background to white

    drawn_points = []
    time = 0

    while True:  # loop to wait till window close
        if time > 1:
            print("loop")
            time = 0
            surface.fill(pygame.Color("white"))

        surface.fill(pygame.Color("white"))

        pygame.draw.aalines(surface, pygame.Color("black"), False, svg_points)

        vectors = soma_vetores(time, coefficients, scale, x_offset, y_offset)

        pygame.draw.lines(surface, pygame.Color("blue"), False, vectors, 2)
        drawn_points.append(vectors[len(vectors) - 1])

        # print(vectors)

        # pygame.draw.circle(surface, (255, 255, 0), (0,0), 100)

        for i in range(len(vectors)):
            pygame.draw.circle(
                surface, (200, 0, 0), vectors[i - 1], mag_vectors[i - 1], 1
            )

        for point in drawn_points:
            pygame.draw.circle(surface, (255, 0, 0), point, 1)

        pygame.display.update()  # copy surface to display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        time += 0.0001


if __name__ == "__main__":
    main()
