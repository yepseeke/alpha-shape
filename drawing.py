import numpy as np
import pygame
import pygame_gui
import sys

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

font = pygame.font.SysFont('arial', 16)


class Slider:
    def __init__(self, x, y, width, height, min_value, max_value):
        self._rect = pygame.Rect(x, y, width, height)  # (750, 30, 200, 10)

        self._min_value = min_value
        self._max_value = max_value

        self._color = (0, 128, 128)
        self._ball_color = (212, 42, 3)

    def get_alpha(self, mouse_position):
        mouse_x, _ = mouse_position
        alpha = max(self._max_value * (mouse_x - self._rect.x) / self._rect.width, self._min_value)

        return alpha

    def update(self, screen, alpha):
        pygame.draw.rect(screen, self._color, self._rect)
        circle_x = int(self._rect.x + 1 / self._max_value * alpha * self._rect.width)
        pygame.draw.circle(screen, self._ball_color, (circle_x, self._rect.height // 2 + self._rect.y), 5)

    def get_rect(self):
        return self._rect


class NamedButton:

    def __init__(self, x, y, width, height, title, font):
        self._rect = pygame.Rect(x, y, width, height)
        self._text = font.render(title, True, black)
        self._text_rect = self._text.get_rect()
        self._text_rect.x = self._rect.right + 20
        self._text_rect.centery = self._rect.centery

        self._text_color = (0, 0, 0)
        self._on_color = (34, 139, 34)
        self._off_color = (128, 0, 0)

    def update(self, screen, is_what: bool):
        if is_what:
            pygame.draw.rect(screen, self._on_color, self._rect, 2)
            pygame.draw.circle(screen, self._on_color, (self._rect.x + self._rect.width, self._rect.centery), 15)
        else:
            pygame.draw.rect(screen, self._off_color, self._rect, 2)
            pygame.draw.circle(screen, self._off_color, (self._rect.x, self._rect.centery), 15)

        screen.blit(self._text, self._text_rect)

    def get_rect(self):
        return self._rect


def run():
    is_dragging = False
    is_radius = True
    is_voronoi = True
    is_adding = False

    selected_index = None
    offset_x = 0
    offset_y = 0
    alpha = 0.1

    points = (np.array(
        [[-2, 2], [2, 2], [2, -2], [-2, -2], [-3, 0], [3, 0], [8, -6], [-8, -6], [-8, 6], [8, 6], [6, -8],
         [-6, -8], [-6, 8], [6, 8], [10, 0], [0, 10], [0, -10], [0, 10], [3, 10], [-3, 10], [3, -10],
         [-3, -10], [10, 3], [-10, 3], [10, -3], [-10, -3], [-10, 0], [-12, 0], [-14, 0]]) + 15) * 20

    points_group = PointsCloud(points)
    points_group.add_point(Point(100, 100))

    alpha_shape = AlphaShape(alpha, points_group)

    radius_button = NamedButton(800, 80, 50, 20, 'alpha radius', font)
    voronoi_button = NamedButton(800, 120, 50, 20, 'voronoi', font)
    point_add_button = NamedButton(800, 720, 50, 20, 'add point', font)

    slider = Slider(750, 30, 200, 10, 0.001, 0.2)

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
                            is_dragging = True
                            offset_x = points_list[i].x - event.pos[0]
                            offset_y = points_list[i].y - event.pos[1]
                if radius_button.get_rect().collidepoint(event.pos):
                    is_radius = not is_radius
                if voronoi_button.get_rect().collidepoint(event.pos):
                    is_voronoi = not is_voronoi
                if point_add_button.get_rect().collidepoint(event.pos):
                    is_adding = not is_adding
                else:
                    if is_adding:
                        x, y = event.pos
                        alpha_shape.add_point(Point(x, y))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if slider.get_rect().collidepoint(event.pos):
                        alpha = slider.get_alpha(event.pos)
                if is_dragging:
                    alpha_shape.move_selected_point(selected_index, event.pos[0] + offset_x, event.pos[1] + offset_y)

        screen.fill(white)

        alpha_shape.update_alpha(alpha)
        alpha_shape.update(screen, is_radius, is_voronoi)

        slider.update(screen, alpha)

        radius_button.update(screen, is_radius)
        voronoi_button.update(screen, is_voronoi)
        point_add_button.update(screen, is_adding)

        pygame.display.flip()


if __name__ == "__main__":
    run()
