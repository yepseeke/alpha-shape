import pygame
import numpy as np

from PointsCloud import PointsCloud


class AlphaShape:
    def __init__(self, alpha: float, points_cloud: PointsCloud):
        self._alpha = alpha
        self._point_cloud = points_cloud

    def get_points(self):
        return self._point_cloud.get_points()

    def update_alpha(self, alpha):
        self._alpha = alpha

    def move_selected_point(self, index: int, dx: float, dy: float):
        self._point_cloud.move_selected(index, dx, dy)

    def draw_alpha_shape(self, screen):
        points_array = self._point_cloud.get_matrix()
        triangles = self._point_cloud.get_triangulation()

        for point_indexes in triangles.simplices:
            pi1, pi2, pi3 = point_indexes
            distance1 = np.linalg.norm(points_array[pi1] - points_array[pi2])
            distance2 = np.linalg.norm(points_array[pi1] - points_array[pi3])
            distance3 = np.linalg.norm(points_array[pi2] - points_array[pi3])

            if distance1 <= 2 / self._alpha and distance2 <= 2 / self._alpha and distance3 <= 2 / self._alpha:
                pygame.draw.polygon(screen, (173, 216, 230), points_array[point_indexes], 0)

            if distance1 <= 2 / self._alpha:
                pygame.draw.line(screen, (100, 100, 100), points_array[pi1], points_array[pi2], 2)
            if distance2 <= 2 / self._alpha:
                pygame.draw.line(screen, (100, 100, 100), points_array[pi1], points_array[pi3], 2)
            if distance3 <= 2 / self._alpha:
                pygame.draw.line(screen, (100, 100, 100), points_array[pi2], points_array[pi3], 2)

    def update(self, screen, is_radius=True, is_voronoi=False):
        color = (255, 127, 127)

        self.draw_alpha_shape(screen)

        self._point_cloud.draw(screen)

        if is_radius:
            for point in self._point_cloud:
                pygame.draw.circle(screen, color, (point.x, point.y), int(1 / self._alpha), 2)
