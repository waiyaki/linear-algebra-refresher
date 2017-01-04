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
        return f'Vector{self.__format__()}'

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
        specifier = '{:.3f}'
        specifiers = f'{specifier}, ' * (self.dimension - 1) + specifier
        formatted = specifiers.format(*self.coordinates)
        return f'({formatted})'

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
        except ZeroDivisionError as e:
            # Re-raise with custom message.
            message = 'Cannot normalize a zero vector: {!r}'.format(self)
            raise ValueError(message) from e

    def dot(self, other):
        """Compute the inner product of two Vectors."""
        return sum(a * b for a, b in zip(self.coordinates, other.coordinates))

    def angle(self, other, degrees=False):
        """Compute the angle between two Vectors.

        If v and w are two vectors, the angle theta between them is then:
            theta = math.acos(dot(v, w) / (|v| * |w|))

        If Uv and Uw are the normalizations of v and w respectively, then:
            theta = math.acos(Uv.dot(Uw))
        """
        try:
            uv = self.normalize()
            uw = other.normalize()
        except ValueError as e:
            raise ValueError('Cannot compute an angle with a zero vector') from e
        else:
            rads = math.acos(uv.dot(uw))
            return math.degrees(rads) if degrees else rads

    def is_parallel(self, other):
        """Determine whether a vector is parallel to another vector."""
        chain = list(zip(self.coordinates, other.coordinates))
        divs = {'{:.3f}'.format(b / a) for a, b in chain}
        if len(divs) > 1:
            divs = {'{:.3f}'.format(a / b) for a, b in chain}
        return len(divs) == 1

    def is_orthogonal(self, other, tolerance=1e-10):
        """Determine if a vector is orthogonal to another vector."""
        return abs(self.dot(other)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return abs(self) < tolerance

    def is_parallel_instructor_implementation(self, other):
        """Determine whether a vector is parallel to another vector."""
        return self.is_zero() or v.is_zero() or self.angle(v, degrees=True) in (0, 180)


if __name__ == '__main__':
    v1 = Vector([8.218, -9.341])
    v2 = Vector([-1.129, 2.111])
    print('Addition: {!r}'.format(v1 + v2))

    v3 = Vector([7.119, 8.215])
    v4 = Vector([-8.223, 0.878])
    print('\nSubtraction: {!r}'.format(v3 - v4))

    v5 = Vector([1.671, -1.012, -0.318])
    scalar = 7.41
    print('\nMultiplication: {!r}'.format(scalar * v5))

    v6 = Vector([-0.221, 7.437])
    v7 = Vector([8.813, -1.331, -6.247])
    print('\nMagnitude:')
    print('|{!r}| = {:.3f}'.format(v6, abs(v6)))
    print('|{!r}| = {:.3f}'.format(v7, abs(v7)))

    v8 = Vector([5.581, -2.136])
    v9 = Vector([1.996, 3.108, -4.554])
    print('\nDirection (Normalization):')
    print('{!r}.normalize() => {!r}'.format(v8, v8.normalize()))
    print('{!r}.normalize() => {!r}'.format(v9, v9.normalize()))

    print('\nDot Products:')
    v10 = Vector([7.887, 4.138])
    v11 = Vector([-8.802, 6.776])
    print('{!r} • {!r} = {:.3f}'.format(v10, v11, v10.dot(v11)))

    v12 = Vector([-5.955, -4.904, -1.874])
    v13 = Vector([-4.496, -8.755, 7.103])
    print('{!r} • {!r} = {:.3f}'.format(v12, v13, v12.dot(v13)))

    print('\nAngles:')
    v14 = Vector([3.183, -7.627])
    v15 = Vector([-2.668, 5.319])
    print('{!r}.angle({!r}) = {:.3f} radians'.format(v14, v15, v14.angle(v15)))

    v16 = Vector([7.35, 0.221, 5.188])
    v17 = Vector([2.751, 8.259, 3.985])
    print('{!r}.angle({!r}) = {:.3f} degrees'.format(v16, v17, v16.angle(v17, degrees=True)))

    print('\nparallel and orthogonal:')
    v18s = [
        Vector([-7.579, -7.88]), Vector([-2.029, 9.97, 4.172]),
        Vector([-2.328, -7.284, -1.214]), Vector([2.118, 4.827])
    ]
    v19s = [
        Vector([22.737, 23.64]), Vector([-9.231, -6.639, -7.245]),
        Vector([-1.821, 1.072, -2.94]), Vector([0, 0])
    ]
    for index, (a, b) in enumerate(zip(v18s, v19s)):
        print('{!r} and {!r}'.format(a, b))
        print('\tparallel: {}'.format(a.is_parallel(b)))
        print('\torthogonal: {}'.format(a.is_orthogonal(b)))
