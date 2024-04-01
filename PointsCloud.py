import numpy as np
import random
import copy

from typing import List
from scipy.spatial import Delaunay, Voronoi

from Point import Point


class PointsCloud:
    def __init__(self, points: np.array):
        self._points = []
        for point in points:
            self._points.append(Point(point[0], point[1]))

    def get_matrix(self, by_rows: bool = True) -> np.array:
        to_return = []
        for p in self:
            to_return.append(p.get_array())

        return np.array(to_return) if by_rows else np.array(to_return).T

    def __mul__(self, other: int | float):
        if type(other) not in [int, float]:
            raise Exception(f"other type {type(other)} is not {int} or {float}")
        return PointsCloud([point * other for point in self._points])

    def __rmul__(self, other: int | float):
        if type(other) not in [int, float]:
            raise Exception(f"other type {type(other)} is not {int} or {float}")
        return PointsCloud([point * other for point in self._points])

    def __add__(self, other: Point):
        if type(other) is not Point:
            raise Exception(f"other type {type(other)} is not {Point}")
        return PointsCloud([point + other for point in self._points])

    def __sub__(self, other: Point):
        if type(other) is not Point:
            raise Exception(f"other type {type(other)} is not {Point}")
        return PointsCloud([point - other for point in self._points])

    def __iter__(self):
        for each in self._points:
            yield each

    def __str__(self):
        return "[" + ", ".join(str(point) for point in self._points) + "]"

    def add_point(self, point: Point):
        self._points.append(point)

    def length(self):
        return len(self._points)

    def move_all(self, dx, dy):
        for point in self._points:
            point.move(dx, dy)

    def move_selected(self, index, dx, dy):
        self._points[index].set_x(dx)
        self._points[index].set_y(dy)

    def get_triangulation(self):
        triangles = Delaunay(self.get_matrix())

        return triangles

    def get_voronoi(self):
        vor = Voronoi(self.get_matrix())

        return vor

    def get_points(self):
        return self._points

    def draw(self, surface):
        for point in self._points:
            point.draw(surface)
