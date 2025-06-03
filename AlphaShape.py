import pygame
import numpy as np

from PointsCloud import PointsCloud
from Point import Point

triangle_color = (173, 216, 230)
circle_color = (255, 127, 127)
voronoi_color = (100, 100, 231)
delaunay_color = (100, 100, 100)


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

    def add_point(self, point: Point):
        self._point_cloud.add_point(point)

    def draw_alpha_shape(self, screen):
        points_array = self._point_cloud.get_matrix()
        triangles = self._point_cloud.get_triangles()

        for point_indexes in triangles:
            pi1, pi2, pi3 = point_indexes
            distance1 = np.linalg.norm(points_array[pi1] - points_array[pi2])
            distance2 = np.linalg.norm(points_array[pi1] - points_array[pi3])
            distance3 = np.linalg.norm(points_array[pi2] - points_array[pi3])

            if distance1 <= 2 / self._alpha and distance2 <= 2 / self._alpha and distance3 <= 2 / self._alpha:
                triangle_points = points_array[pi1], points_array[pi2], points_array[pi3]
                pygame.draw.polygon(screen, triangle_color, triangle_points, 0)

            if distance1 <= 2 / self._alpha:
                pygame.draw.line(screen, delaunay_color, points_array[pi1], points_array[pi2], 2)
            if distance2 <= 2 / self._alpha:
                pygame.draw.line(screen, delaunay_color, points_array[pi1], points_array[pi3], 2)
            if distance3 <= 2 / self._alpha:
                pygame.draw.line(screen, delaunay_color, points_array[pi2], points_array[pi3], 2)

    def update(self, screen, is_radius=True, is_voronoi=False):
        self.draw_alpha_shape(screen)
        self._point_cloud.draw(screen)

        if is_radius:
            for point in self._point_cloud:
                pygame.draw.circle(screen, circle_color, (point.x, point.y), int(1 / self._alpha), 2)

        if is_voronoi:
            self.draw_voronoi(screen, voronoi_color)

    def draw_voronoi(self, screen, voronoi_color):
        vor_coords, regions = self._point_cloud.get_voronoi()

        vor_coords = [np.round(c).astype(int) for c in vor_coords]

        for region in regions.values():
            polygon = [vor_coords[i] for i in region]

            if all(p is not None for p in polygon) and len(polygon) >= 3:
                for i in range(len(polygon)):
                    p1 = polygon[i]
                    p2 = polygon[(i + 1) % len(polygon)]
                    pygame.draw.line(screen, voronoi_color, p1, p2, 2)
