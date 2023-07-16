#!/usr/bin/python3

# Returns element-wise subtraction of v from u.
def sub(u, v):
    return (u[0]-v[0], u[1]-v[1])

# Returns the Euclidean norm of vector v.
def mag(v):
    return (v[0]**2 + v[1]**2)**0.5

# Returns dot product of vectors u and v.
def dot(u, v):
    return u[0]*v[0] + u[1]*v[1]

# Returns cosine of angle made by ray from v1 to v2 with ray from v2 to v3.
# Assumptions:
# 1. v1 and v2 are distinct (v2 and v3 might not be).
# 2. v3 is counter-clockwise from v2.
def cos(v1, v2, v3):
    if v2 == v3: return 0
    a = sub(v2, v1)
    b = sub(v3, v2)
    return dot(a, b) / (mag(a) * mag(b))

# Returns slope of the ray from u to v. Assumes u != v
def slope(u, v):
    if u[0] == v[0]:
        return float('inf') if u[1] < v[1] else float('-inf')
    return (v[1]-u[1])/(v[0]-u[0])

# Returns True if points v1, v2, v3 are collinear.
def collinear(v1, v2, v3):
    return slope(v1, v2) == slope(v2, v3)

# Returns a new list consisting of points from the input list with collinear
# points removed. Assumes that the points specify a convex hull.
# Example: in [a, b, c, d, e] if a, b, c, d are collinear, then output is
#          [a, d, e].
def delete_collinear_from_convex_hull(points):
    if len(points) < 3:
        return points
    stack = [points[0]]
    for point in points[1:]:
        if len(stack) < 2:
            stack.append(point)
            continue
        if collinear(*stack[-2:], point):
            stack.pop()
        stack.append(point)
    return stack

# Find convex hull of a list of points, each point represented as (x, y).
def jarvis(points):
    # Sort left to right, then top to bottom.
    points.sort(key=lambda x: (x[0], -x[1]))

    # Leftmost, topmost point is guaranteed to be in the hull
    hull = [0]

    # Keep going until the first and last points on the hull are equal
    while not (len(hull) > 1 and hull[0] == hull[-1]):
        a = points[hull[-1]]
        b = sub(a, (0,1))
        avoid = [hull[-1]]
        if len(hull) > 1:
            a = points[hull[-2]]
            b = points[hull[-1]]
            avoid = hull[-2:]

        # Find the least angle between a, b and the other point.
        # Ignore any point that coincides with a point on the hull.
        # Hack: cos is monotonically decreasing with angle from 0 to pi rad
        # so just find max cos. We don't have to worry about angles > pi rad
        # since reflex angles won't occur (TODO: prove this)! 
        best = max_cos = -1
        for j in range(len(points)):
            if j in avoid: continue
            cur_cos = cos(a, b, points[j])
            if cur_cos > max_cos:
                max_cos = cur_cos
                best = j
        # We've closed the loop
        if best == hull[0]:
            break
        hull.append(best)
    result = [points[x] for x in hull]
    return delete_collinear_from_convex_hull(result)
    # return result

tests = [
    # square
    # [(0, 1), (0, 0), (1, 0), (1, 1)]
    [(0, 0), (0, 1), (1, 1), (1, 0)],
    
    # square with an unused centre point
    # [(0, 1), (0, 0), (1, 0), (1, 1)]
    [(0, 0), (0, 1), (1, 1), (1, 0), (0.5, 0.5)],
    
    # square with several unused centre points
    # [(0, 1), (0, 0), (1, 0), (1, 1)]
    [(0, 0), (0, 1), (1, 1), (1, 0)] + [(x/100, x/100) for x in range(1,100)],

    # diamond
    # [(0, 0.5), (0.5, 0), (1, 0.5), (0.5, 1)]
    [(0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5)],

    # square with collinear points.
    # [(0, 1), (0, 0), (1, 0), (1, 1)]
    [(0, 1), (0, 0)] + [(x/100, 0) for x in range(1, 100)] + [(1, 0), (1, 1)]

    # TODO: add more complex testcases, make this a proper unit test with
    # unittest module
]

for test in tests:
    print(jarvis(test))
