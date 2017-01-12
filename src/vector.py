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
        """Determine whether a vector is parallel to another vector.

        Two vectors are parallel if one is a scalar multiple of the other.
        """
        chain = list(zip(self.coordinates, other.coordinates))
        divs = {'{:.3f}'.format(b / a) for a, b in chain}
        if len(divs) > 1:
            divs = {'{:.3f}'.format(a / b) for a, b in chain}
        return len(divs) == 1

    def is_orthogonal(self, other, tolerance=1e-10):
        """Determine if a vector is orthogonal to another vector.

        A vector is orthogonal to another vector is their dot product is 0.
        """
        return math.isclose(self.dot(other), 0, abs_tol=tolerance)

    def is_zero(self, tolerance=1e-10):
        return math.isclose(abs(self), 0, abs_tol=tolerance)

    def is_parallel_instructor_implementation(self, other):
        """Determine whether a vector is parallel to another vector.

        Two vectors are parallel if one is a scalar multiple of the other.

        Two vectors are parallel if neither of them is a zero vector and the
        angle between them is either 0 or pi radians.
        """
        return self.is_zero() or v.is_zero() or round(self.angle(v, degrees=True), 2) in (0, 180)

    def projection(self, b):
        """Compute the projection of Vector v onto Vector b.

        If V and B are two vectors:
            Taking B to be the basis vector and assuming the
            angle θ between V and B <= 90 degrees and Ub
            is the normalization of Vector b, then the projection
            V|| (V parallel) of V onto B is

                V|| = V.dot(Ub) * Ub
        """
        try:
            norm_b = b.normalize()
        except ValueError as e:
            if 'Cannot normalize a zero vector' in str(e):
                message = f'No unique parallel component to zero vector {repr(b)}'
                raise ValueError(message) from e
            raise
        else:
            return self.dot(norm_b) * norm_b

    def orthogonal_component(self, b):
        """Compute the component orthogonal to a given basis vector

        If V and B are two vectors:
            Taking B to be the basis vector and assuming the
            angle θ between V and B is <= 90 deg, then
            vector V can be expressed as the sum of two vectors
            V|| (V parallel) and V┴ (V perp) where V|| is the projection of
            V onto B and V┴ is the component of V orthogonal to the basis
            vector B.

                V = V|| + V┴
            =>
                V┴ = V - V||
        """
        try:
            return self - self.projection(b)
        except ValueError as e:
            if 'No unique parallel component' in str(e):
                message = f'No unique orthogonal component to zero vector {repr(b)}'
                raise ValueError(message) from e
            raise

    def cross(self, other):
        try:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = other.coordinates
        except ValueError as e:
            raise ValueError('Vector has to a 3 dimensional vector')
        else:
            coordinates = [
                y1 * z2 - y2 * z1,
                -(x1 * z2 - x2 * z1),
                x1 * y2 - x2 * y1
            ]
            return Vector(coordinates)

    def area_parallelogram(self, other):
        return round(abs(self.cross(other)), 3)

    def area_triangle(self, other):
        return 0.5 * self.area_parallelogram(other)
