import itertools
from collections import defaultdict

import numpy as np


def get_area(point_a: list[int], point_b: list[int]):
    return abs(point_a[0] - point_b[0] + 1) * abs(point_a[1] - point_b[1] + 1)


def get_largest(point_list: list[list[int]]):
    N = len(point_list)
    best_pair = None
    curr_best = -1

    for i in range(N):
        for j in range(i + 1, N):
            area = get_area(point_list[i], point_list[j])
            if area > curr_best:
                curr_best = area
                best_pair = (i, j)

    print(f"Best pair: {point_list[best_pair[0]]}, {point_list[best_pair[1]]}")

    return curr_best


def label_grid(point_list: list[list[int]]):
    C, R = max(p[0] for p in point_list) + 1, max(p[1] for p in point_list) + 1

    grid = np.zeros((R, C))

    x_to_y_max = {}
    x_to_y_min = {}
    for p in point_list:
        x_to_y_max[p[0]] = max(x_to_y_max.get(p[0], p[1]), p[1])
        x_to_y_min[p[0]] = min(x_to_y_min.get(p[0], p[1]), p[1])

    for x in x_to_y_min.keys():
        y_min = x_to_y_min[x]
        y_max = x_to_y_max[x]

        grid[y_min : y_max + 1, x] = 1

    for row in range(grid.shape[0]):
        res = np.where(grid[row] == 1)
        cols = res[0]
        for c in range(len(cols) - 1):
            grid[row, cols[c] : cols[c + 1]] = 1

    # return grid

    N = len(point_list)
    best_pair = None
    curr_best = -1

    for i in range(N):
        for j in range(i + 1, N):
            p_a, p_b = point_list[i], point_list[j]

            if (
                grid[
                    min(p_a[1], p_b[1]) : max(p_a[1], p_b[1]) + 1,
                    min(p_a[0], p_b[0]) : max(p_a[0], p_b[0]) + 1,
                ]
                == 0
            ).any():
                continue

            print(f"Checking {i},{j}")

            area = get_area(p_a, p_b)
            if area > curr_best:
                curr_best = area
                best_pair = (i, j)

    print(
        f"Best pair: {point_list[best_pair[0]]}, {point_list[best_pair[1]]}\nArea: {curr_best}"
    )


def label_grid_(p):
    t = 0
    for (x1, y1), (x2, y2) in itertools.combinations(p, 2):
        bx1, bx2 = min(x1, x2), max(x1, x2)
        by1, by2 = min(y1, y2), max(y1, y2)
        for i, (lx1, ly1) in enumerate(p):
            lx2, ly2 = p[(i + 1) % len(p)]
            if not (
                max(lx1, lx2) <= bx1
                or bx2 <= min(lx1, lx2)
                or max(ly1, ly2) <= by1
                or by2 <= min(ly1, ly2)
            ):
                break
        else:
            t = max(t, (bx2 - bx1 + 1) * (by2 - by1 + 1))
    print(t)
