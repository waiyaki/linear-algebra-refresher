from src.vector import Vector


def main():
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

if __name__ == '__main__':
    main()
