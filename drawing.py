import numpy as np
import pygame
import pygame_gui
import sys

from scipy.spatial import Delaunay
from typing import List

from PointsCloud import PointsCloud
from Point import Point
from AlphaShape import AlphaShape

pygame.init()

width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Alpha Shapes")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

manager = pygame_gui.UIManager((width, height))

subsurface_width = 200
subsurface_height = 100
subsurface_color = (102, 205, 170)

slider_rect = pygame.Rect(750, 30, 200, 10)

switch_rect = pygame.Rect(800, 80, 50, 20)
font = pygame.font.SysFont('arial', 16)
text = font.render('alpha radius', True, black)
text_rect = text.get_rect()
text_rect.x = switch_rect.right + 20
text_rect.centery = switch_rect.centery

alpha = 0.02


def main():
    global alpha
    points = (np.array(
        [[-2, 2], [2, 2], [2, -2], [-2, -2], [-3, 0], [3, 0], [8, -6], [-8, -6], [-8, 6], [8, 6], [6, -8],
         [-6, -8], [-6, 8], [6, 8], [10, 0], [0, 10], [0, -10], [0, 10], [3, 10], [-3, 10], [3, -10],
         [-3, -10], [10, 3], [-10, 3], [10, -3], [-10, -3], [-10, 0], [-12, 0], [-14, 0]]) + 15) * 20

    points_group = PointsCloud(points)
    points_group.add_point(Point(100, 100))

    dragging = False
    is_radius = True
    selected_index = None
    offset_x = 0
    offset_y = 0

    alpha_shape = AlphaShape(alpha, points_group)

    while True:

        for event in pygame.event.get():
            points_list = alpha_shape.get_points()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(len(points_list)):
                        distance = points_list[i].distance(Point(event.pos[0], event.pos[1]))
                        if distance <= points_list[i].get_radius():
                            selected_index = i
                            dragging = True
                            offset_x = points_list[i].x - event.pos[0]
                            offset_y = points_list[i].y - event.pos[1]
                if switch_rect.collidepoint(event.pos):
                    is_radius = not is_radius

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if slider_rect.collidepoint(event.pos):
                        mouse_x, _ = event.pos
                        alpha = 0.2 * (mouse_x - slider_rect.x) / slider_rect.width
                        alpha = max(alpha, 0.001)
                        print(alpha)

                if dragging:
                    alpha_shape.move_selected_point(selected_index, event.pos[0] + offset_x, event.pos[1] + offset_y)

        screen.fill(white)

        if is_radius:
            pygame.draw.rect(screen, green, switch_rect, 2)
            pygame.draw.circle(screen, green, (switch_rect.x + switch_rect.width, switch_rect.centery), 15)
        else:
            pygame.draw.rect(screen, red, switch_rect, 2)
            pygame.draw.circle(screen, red, (switch_rect.x, switch_rect.centery), 15)
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, black, slider_rect)
        circle_x = int(slider_rect.x + 5 * alpha * slider_rect.width)
        pygame.draw.circle(screen, red, (circle_x, 35), 5)

        alpha_shape.update_alpha(alpha)
        alpha_shape.update(screen, is_radius)

        pygame.display.flip()


if __name__ == "__main__":
    main()
