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
        triangles = self._point_cloud.get_triangulation()

        for point_indexes in triangles.simplices:
            pi1, pi2, pi3 = point_indexes
            distance1 = np.linalg.norm(points_array[pi1] - points_array[pi2])
            distance2 = np.linalg.norm(points_array[pi1] - points_array[pi3])
            distance3 = np.linalg.norm(points_array[pi2] - points_array[pi3])

            if distance1 <= 2 / self._alpha and distance2 <= 2 / self._alpha and distance3 <= 2 / self._alpha:
                pygame.draw.polygon(screen, triangle_color, points_array[point_indexes], 0)

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
            self.draw_voronoi_diagram(screen)

    def draw_voronoi_diagram(self, screen):
        vor = self._point_cloud.get_voronoi()

        center = vor.points.mean(axis=0)
        ptp_bound = np.ptp(vor.points, axis=0)

        finite_segments = []
        infinite_segments = []
        for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
            simplex = np.asarray(simplex)
            if np.all(simplex >= 0):
                finite_segments.append(np.round(vor.vertices[simplex]))
            else:
                i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

                t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = vor.points[pointidx].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                if (vor.furthest_site):
                    direction = -direction
                far_point = vor.vertices[i] + direction * ptp_bound.max()

                infinite_segments.append([np.round(vor.vertices[i]), np.round(far_point)])

        for [p1, p2] in finite_segments:
            pygame.draw.line(screen, voronoi_color, p1, p2, 2)

        for [p1, p2] in infinite_segments:
            pygame.draw.line(screen, voronoi_color, p1, p2, 2)
