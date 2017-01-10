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

    print('\nProjection:')
    v20 = Vector([3.039, 1.879])
    v21 = Vector([0.825, 2.036])
    print(f'{repr(v20)}.projection({repr(v21)})')
    print(f'\t= {repr(v20.projection(v21))}')

    print('\nPerpendicular Component:')
    v22 = Vector([-9.88, -3.264, -8.159])
    v23 = Vector([-2.155, -9.353, -9.473])
    print(f'{repr(v22)}.orthogonal_component({repr(v23)})')
    print(f'\t= {repr(v22.orthogonal_component(v23))}')

    v24 = Vector([3.009, -6.172, 3.692, -2.51])
    v25 = Vector([6.404, -9.144, 2.759, 8.718])
    print(f'\nFind V|| and V┴ given V = {repr(v24)} and basis B = {repr(v25)}')
    print(f'V|| = {repr(v24.projection(v25))}')
    print(f'V┴ = {repr(v24.orthogonal_component(v25))}')
