import numpy as np

from scipy.spatial import Delaunay, Voronoi

from Point import Point


class PointsCloud:
    def __init__(self, points: np.array, center=(0, 0), radius=10000):
        self._points = [Point(p[0], p[1]) for p in points]
        self.center = np.asarray(center)
        self.radius = radius
        self._rebuild_triangulation()

    def _rebuild_triangulation(self):
        self.coords = [self.center + self.radius * np.array(v)
                       for v in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
        self.coords.extend([p.get_array() for p in self._points])

        self.triangles = {}
        T1, T2 = (0, 1, 3), (2, 3, 1)
        self.triangles[T1] = [T2, None, None]
        self.triangles[T2] = [T1, None, None]

        for i in range(4, len(self.coords)):
            self._add_point(i)

    def get_matrix(self, by_rows: bool = True) -> np.array:
        to_return = []
        for p in self:
            to_return.append(p.get_array())

        return np.array(to_return) if by_rows else np.array(to_return).T

    def _in_circumcircle(self, tri, p):
        a, b, c = [self.coords[i] for i in tri]

        def det(a, b, c, d):
            mat = np.array([
                [a[0] - d[0], a[1] - d[1], (a[0] - d[0]) ** 2 + (a[1] - d[1]) ** 2],
                [b[0] - d[0], b[1] - d[1], (b[0] - d[0]) ** 2 + (b[1] - d[1]) ** 2],
                [c[0] - d[0], c[1] - d[1], (c[0] - d[0]) ** 2 + (c[1] - d[1]) ** 2]
            ])
            return np.linalg.det(mat)

        return det(a, b, c, p) > 1e-12

    def _add_point(self, idx):
        p = self.coords[idx]
        bad_triangles = [T for T in self.triangles if self._in_circumcircle(T, p)]

        if not bad_triangles:
            return

        boundary = []
        T = bad_triangles[0]
        edge = 0
        while True:
            tri_op = self.triangles[T][edge]
            if tri_op not in bad_triangles:
                boundary.append((T[(edge + 1) % 3], T[(edge - 1) % 3], tri_op))
                edge = (edge + 1) % 3
                if boundary[0][0] == boundary[-1][1]:
                    break
            else:
                edge = (self.triangles[tri_op].index(T) + 1) % 3
                T = tri_op

        for T in bad_triangles:
            del self.triangles[T]

        new_triangles = []
        for (e0, e1, tri_op) in boundary:
            new_t = (idx, e0, e1)
            self.triangles[new_t] = [tri_op, None, None]

            if tri_op:
                for i, neigh in enumerate(self.triangles[tri_op]):
                    if neigh and e1 in neigh and e0 in neigh:
                        self.triangles[tri_op][i] = new_t

            new_triangles.append(new_t)

        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            self.triangles[T][1] = new_triangles[(i + 1) % N]
            self.triangles[T][2] = new_triangles[(i - 1) % N]

    def get_triangles(self):
        return [(a - 4, b - 4, c - 4)
                for (a, b, c) in self.triangles
                if a >= 4 and b >= 4 and c >= 4]

    def compute_circumcenter(self, a, b, c):
        A = np.array(self.coords[a], dtype=np.float64)
        B = np.array(self.coords[b], dtype=np.float64)
        C = np.array(self.coords[c], dtype=np.float64)

        ax, ay = A
        bx, by = B
        cx, cy = C

        D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

        if abs(D) < 1e-8:
            return (A + B + C) / 3

        Ux = ((ax ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay) + (cx ** 2 + cy ** 2) * (ay - by)) / D
        Uy = ((ax ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax - cx) + (cx ** 2 + cy ** 2) * (bx - ax)) / D

        return np.array([Ux, Uy], dtype=np.float64)

    def get_voronoi(self):
        use_vertex = {i: [] for i in range(len(self.coords))}
        vor_coords = []
        index = {}

        for tidx, (a, b, c) in enumerate(sorted(self.triangles)):
            center = self.compute_circumcenter(a, b, c)
            vor_coords.append(center)
            use_vertex[a].append((b, c, a))
            use_vertex[b].append((c, a, b))
            use_vertex[c].append((a, b, c))
            index[(a, b, c)] = tidx
            index[(c, a, b)] = tidx
            index[(b, c, a)] = tidx

        regions = {}
        for i in range(4, len(self.coords)):
            if use_vertex[i]:
                v = use_vertex[i][0][0]
                r = []
                visited = set()
                for _ in range(len(use_vertex[i])):
                    t = next((t for t in use_vertex[i] if t[0] == v and t not in visited), None)
                    if t is None:
                        break
                    r.append(index[t])
                    visited.add(t)
                    v = t[1]
                regions[i - 4] = r

        print(regions)

        return vor_coords, regions

    def get_points(self):
        return self._points

    def add_point(self, point: Point):
        self._points.append(point)
        self._rebuild_triangulation()

    def __iter__(self):
        for point in self._points:
            yield point

    def __str__(self):
        return "[" + ", ".join(str(point) for point in self._points) + "]"

    def length(self):
        return len(self._points)

    def move_all(self, dx, dy):
        for point in self._points:
            point.move(dx, dy)
        self._rebuild_triangulation()

    def move_selected(self, index, dx, dy):
        self._points[index].set_x(dx)
        self._points[index].set_y(dy)
        self._rebuild_triangulation()

    def __mul__(self, other: int | float):
        if not isinstance(other, (int, float)):
            raise Exception(f"other type {type(other)} is not {int} or {float}")
        return PointsCloud(np.array([point.get_array() * other for point in self._points]))

    def __rmul__(self, other: int | float):
        return self.__mul__(other)

    def __add__(self, other: Point):
        if not isinstance(other, Point):
            raise Exception(f"other type {type(other)} is not {Point}")
        return PointsCloud(np.array([point.get_array() + other.get_array() for point in self._points]))

    def __sub__(self, other: Point):
        if not isinstance(other, Point):
            raise Exception(f"other type {type(other)} is not {Point}")
        return PointsCloud(np.array([point.get_array() - other.get_array() for point in self._points]))

    def draw(self, surface):
        for point in self._points:
            point.draw(surface)
