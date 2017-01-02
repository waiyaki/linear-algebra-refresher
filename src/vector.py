import math


class Vector:
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be iterable')

    def __repr__(self):
        coords = ', '.join(str(c) for c in self.coordinates)
        return 'Vector({})'.format(coords)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.coordinates, other.coordinates)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.coordinates, other.coordinates)])

    def __mul__(self, scalar):
        return Vector([v * scalar for v in self.coordinates])

    def __rmul__(self, scalar):
        return self * scalar

    def __format__(self, format_spec=''):
        specifiers = '{}, ' * (self.dimension - 1) + '{}'
        components = (format(c, format_spec) for c in self.coordinates)
        return '({})'.format(specifiers.format(*components))

    def __abs__(self):
        """Compute the Vector magnitude

        If v = Vector([v1, v2, ..., vn]),
        then
        |v| = math.sqrt(sum(map(lambda x: x ** 2, [v1, v2, ..., vn])))
        """
        return math.sqrt(sum(c ** 2 for c in self.coordinates))

    def normalize(self):
        """Compute the direction of the Vector by normalizing it.

        To normalize a Vector, multiply it with the inverse of its
        magnitude.

        Zero vectors have no direction, hence cannot be normalized.
        """
        try:
            return self * (1 / abs(self))
        except ZeroDivisionError:
            raise Exception('Cannot normalize a zero vector')

if __name__ == '__main__':
    v1 = Vector([8.218, -9.341])
    v2 = Vector([-1.129, 2.111])
    print('Addition: Vector{:.3f}'.format(v1 + v2))

    v3 = Vector([7.119, 8.215])
    v4 = Vector([-8.223, 0.878])
    print('Subtraction: Vector{:.3f}'.format(v3 - v4))

    v5 = Vector([1.671, -1.012, -0.318])
    scalar = 7.41
    print('Multiplication: Vector{:.3f}'.format(scalar * v5))

    v6 = Vector([-0.221, 7.437])
    v7 = Vector([8.813, -1.331, -6.247])
    print('Magnitude:')
    print('|{!r}| = {:.3f}, |{!r}| = {:.3f}'.format(v6, abs(v6), v7, abs(v7)))

    v8 = Vector([5.581, -2.136])
    v9 = Vector([1.996, 3.108, -4.554])
    print('direction:')
    print('{!r} => {:.3f}, {!r} => {:.3f}'.format(v8, v8.normalize(), v9, v9.normalize()))
