from collections import Counter

import numpy as np


def get_distance(coord_a: list[int], coord_b: list[int]):
    return sum((val_a - val_b) ** 2 for val_a, val_b in zip(coord_a, coord_b))


def make_connections(coord_list: list[list[int]], num_connections: int):
    N = len(coord_list)

    groups = [-1] * N
    curr_group = 0

    dist_mat = np.full((N, N), np.inf)

    for i in range(N):
        for j in range(i + 1, N):
            dist_mat[i, j] = get_distance(coord_list[i], coord_list[j])

    while num_connections > 0:
        row, col = np.unravel_index(np.argmin(dist_mat), dist_mat.shape)

        if {groups[row], groups[col]} == {-1}:
            groups[row] = curr_group
            groups[col] = curr_group

            print(f"{coord_list[row]} <> {coord_list[col]}: {curr_group}")

            curr_group += 1
        else:
            group_vals = {groups[row], groups[col]} - {-1}
            group_val = min(group_vals)

            groups[row] = groups[col] = group_val
            for idx, val in enumerate(groups):
                if val in group_vals:
                    groups[idx] = group_val
            print(
                f"{coord_list[row]} <> {coord_list[col]}: {max([groups[row], groups[col]])}"
            )

        dist_mat[row, col] = np.inf

        num_connections -= 1

        if len(set(groups)) == 1:
            print(f"Last connections: {coord_list[row]} <> {coord_list[col]}")
            break

    group_counts = Counter(groups)
    most_common = group_counts.most_common(4)
    sizes = [size for group, size in most_common if group != -1]

    return np.prod(sizes[:3])
