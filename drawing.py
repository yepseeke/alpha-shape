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

manager = pygame_gui.UIManager((width, height))

alpha = 0.02


def main():
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
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    alpha_shape.move_selected_point(selected_index, event.pos[0] + offset_x, event.pos[1] + offset_y)

        screen.fill(white)

        alpha_shape.update(screen, is_radius)

        pygame.display.flip()


if __name__ == "__main__":
    main()
