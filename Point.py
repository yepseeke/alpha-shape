import numpy as np
import pygame

from typing import Tuple


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0, color: Tuple[int, int, int] = (0, 0, 0), radius: int = 5):
        self._x = x
        self._y = y
        self._color = color
        self._radius = radius

    def __add__(self, other: 'Point'):
        if type(other) is not self.__class__:
            raise Exception(f"other type {type(other)} is not {self.__class__}")
        return Point(self._x + other.x, self._y + other.y)

    def __sub__(self, other: 'Point'):
        if type(other) is not self.__class__:
            raise Exception(f"other type {type(other)} is not {self.__class__}")
        return Point(self._x - other.x, self._y - other.y)

    def __mul__(self, other: int | float):
        if type(other) not in [int, float]:
            raise Exception(f"other type {type(other)} is not {int} or {float}")
        return Point(self._x * other, self._y * other)

    def __rmul__(self, other: int | float):
        if type(other) not in [int, float]:
            raise Exception(f"other type {type(other)} is not {int} or {float}")
        return Point(self._x * other, self._y * other)

    def __truediv__(self, other: int | float):
        if type(other) not in [int, float]:
            raise Exception(f"other type {type(other)} is not {int} or {float}")
        if other == 0:
            raise Exception("Division by zero")
        return Point(self._x / other, self._y / other)

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __str__(self):
        return f"({self._x}, {self._y})"

    def distance(self, other: 'Point') -> float:
        return ((other.x - self._x) ** 2 + (other.y - self._y) ** 2) ** 0.5

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get_color(self):
        return self._color

    def get_radius(self):
        return self._radius

    def set_x(self, x: float):
        self._x = x

    def set_y(self, y: float):
        self._y = y

    def set_color(self, color: Tuple[int, int, int]):
        self._color = color

    def set_radius(self, radius: int):
        self._radius = radius

    def get_array(self) -> np.array:
        return np.array([self._x, self._y])

    def move(self, dx: float, dy: float):
        self._x += dx
        self._y += dy

    def draw(self, surface):
        pygame.draw.circle(surface, self._color, (self._x, self._y), self._radius)
