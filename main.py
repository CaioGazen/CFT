from xml.dom import minidom
from arrow import draw_arrow
import time
import numpy as np
import pygame
from svg.path import parse_path

# read the SVG file
doc = minidom.parse("cube.svg")
path_strings = [path.getAttribute("d") for path in doc.getElementsByTagName("path")]
doc.unlink()

svgpath = path_strings[0]

path = parse_path(svgpath)


def calc_coefficient(n, t):
    return path.point(t) * (np.exp(-1 * n * 2 * np.pi * 1j * t))


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
    coefficients = []
    for pos in range((n_vetores // 2) * -1, (n_vetores // 2) + 1, 1):
        coefficient = midpoint(calc_coefficient, pos, 0, 1, 1000)
        mag = np.linalg.norm(coefficient * np.exp(pos * 2 * np.pi * 1j * 1))
        coefficients.append((mag, pos, coefficient))
    coefficients.sort(reverse=True)
    return coefficients


def get_vectors(t, coefficients, scale, x_offset, y_offset):
    vectors = [(0, 0)]
    for mag, pos, coeffitient in coefficients:
        vector = coeffitient * np.exp(pos * 2 * np.pi * 1j * t)
        vectors.append(
            (
                (vector.real) + vectors[len(vectors) - 1][0],
                (vector.imag) + vectors[len(vectors) - 1][1],
            )
        )
    return vectors


def get_scale(point, scale, x_offset, y_offset):
    return (np.array(point) * scale) + (x_offset, y_offset)


def main():
    window_size = 600
    x_offset = window_size / 2
    y_offset = window_size / 2

    scale = 60
    scale_2 = 0.005

    speed = 10
    n_vectors = 20

    step_speed = 0.0001
    step_speed_linear = 8

    follow = True
    draw_circles = True
    draw_svg = True
    curr_folow = 0
    last_key_time = 0
    last_move_time = 0
    # original svg
    n_lines = 1000

    t = 0
    drawn_points = [(0, 0), (0, 0)]

    svg_points = [
        (p.real, p.imag)
        for p in (path.point(i / n_lines) for i in range(0, n_lines + 1))
    ]

    pygame.init()  # init pygame
    surface = pygame.display.set_mode(
        (window_size, window_size)
    )  # get surface to draw on

    surface.fill(pygame.Color("white"))

    font = pygame.font.Font('LiberationMono-Regular.ttf', 14)
    text = font.render(f"""
                            time: {t:.4f}\n
                            Numero de vetores:{n_vectors} 
                        """, True, pygame.Color("black"))
    textRect = text.get_rect()
    textRect.topleft = (10,10)
    pygame.display.update()

    coefficients = get_coefficients(n_vectors)

    while True:  # loop to wait till window close
        # limpar a tela
        surface.fill(pygame.Color("white"))
        text = font.render(f"time: {t:.4f}" f"\nNumero de vetores:{n_vectors}" f"\nTime Step {step_speed}", True, pygame.Color("black"))
        surface.blit(text, textRect)

        # resetar tempo
        if t > 1:
            print("loop")
            t = 0

        # calcular posiçoes dos vetores
        vectors = get_vectors(t, coefficients, scale, x_offset, y_offset)

        # seguir um vetor
        if follow:
            curr_folow_pos = vectors[curr_folow]
            x_offset = ((curr_folow_pos[0] * scale) - (window_size / 2)) * -1
            y_offset = ((curr_folow_pos[1] * scale) - (window_size / 2)) * -1

        if draw_svg:
            # desenhar svg original
            pygame.draw.aalines(
                surface,
                pygame.Color("black"),
                False,
                get_scale(svg_points, scale, x_offset, y_offset),
            )

        # desenhar vetores
        for n in range(len(vectors) - 1):
            draw_arrow(
                surface,
                pygame.Vector2(
                    get_scale(vectors[n + 0], scale, x_offset, y_offset).tolist()
                ),
                pygame.Vector2(
                    get_scale(vectors[n + 1], scale, x_offset, y_offset).tolist()
                ),
                pygame.Color("blue"),
                0.005 * scale * coefficients[n][0],
                0.1   * scale * coefficients[n][0],
                0.1   * scale * coefficients[n][0],
            )

        # desenhar circulos
        if draw_circles:
            for i in range(len(vectors)):
                pygame.draw.circle(
                    surface,
                    (200, 0, 0),
                    get_scale(vectors[i - 1], scale, x_offset, y_offset),
                    coefficients[i - 1][0] * scale,
                    1,
                )

        # deenhar todos os pontos
        drawn_points.append(vectors[len(vectors) - 1])

        # for point in drawn_points:
        #    pygame.draw.circle(
        #        surface, (255, 0, 0), get_scale(point, scale, x_offset, y_offset), 1
        #    )

        pygame.draw.aalines(
            surface,
            pygame.Color("red"),
            False,
            get_scale(drawn_points, scale, x_offset, y_offset),
        )

        pygame.display.update()  # update surface

        # Controls
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                scale_2 += event.y/50
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        x_offset -= (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed
        y_offset -= (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed

        scale_2 += (keys[pygame.K_j] - keys[pygame.K_k])/50
        scale = np.exp(scale_2 * -1)

        step_speed_linear += (keys[pygame.K_COMMA] - keys[pygame.K_PERIOD])/10
        step_speed = np.exp(step_speed_linear * -1)

        if keys[pygame.K_c] and time.time() - last_key_time > 0.2:
            draw_circles = not draw_circles
            last_key_time = time.time()

        if keys[pygame.K_f]:
            if time.time() - last_key_time > 0.2:
                follow = not follow
            last_key_time = time.time()

        if keys[pygame.K_m] or keys[pygame.K_n]:
            if time.time() - last_key_time > 0.2:
                curr_folow += keys[pygame.K_m] - keys[pygame.K_n]
                last_key_time = time.time()
            curr_folow = 0 if curr_folow >= len(vectors) else curr_folow

        if keys[pygame.K_b] and time.time() - last_key_time > 0.2:
            draw_svg = not draw_svg
            last_key_time = time.time()

        mouse_keys = pygame.mouse.get_pressed()
        if mouse_keys[0]:
            if time.time() - last_move_time > 0.1:
                pygame.mouse.get_rel()
                print("timed")
            mouse_moved = pygame.mouse.get_rel()
            print(mouse_moved)
            x_offset = x_offset + mouse_moved[0]
            y_offset = y_offset +  mouse_moved[1]
            last_move_time = time.time()



        t += step_speed


if __name__ == "__main__":
    main()
