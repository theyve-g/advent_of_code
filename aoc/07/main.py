from multiprocessing import Value

import numpy as np

EMPTY = 0
BEAM = 1
SPLITTER = -2
START = -1

INT_MAP = {".": EMPTY, "|": BEAM, "^": SPLITTER, "S": START}
REVERSE_MAP = {EMPTY: ".", BEAM: "1", SPLITTER: "^", START: "S"}


def label_grid(grid: np.ndarray):
    R, C = grid.shape[0], grid.shape[1]

    splits = 0

    for r in range(R - 1):
        for c in range(C):
            if grid[r][c] in {START, BEAM}:
                if grid[r + 1][c] == EMPTY:
                    grid[r + 1][c] = BEAM
                elif grid[r + 1][c] == SPLITTER:
                    splits += 1
                    if c - 1 >= 0:
                        grid[r + 1][c - 1] = BEAM
                    if c + 1 < C:
                        grid[r + 1][c + 1] = BEAM

    return grid, splits


def label_timelines(grid: np.ndarray):
    R, C = grid.shape[0], grid.shape[1]

    start_pos = np.argmin(grid[0])

    for c in range(C):
        if grid[R - 2][c] == EMPTY:
            grid[R - 1][c] = 1

    for r in range(R - 2, -1, -1):
        for c in range(C):
            if grid[r][c] == SPLITTER:
                continue
            if grid[r][c] not in {EMPTY, START}:
                raise ValueError((r, c))
            if grid[r + 1][c] == SPLITTER:
                grid[r][c] = (grid[r + 1][c - 1] if c > 0 else 0) + (
                    grid[r + 1][c + 1] if c < C - 1 else 0
                )
            else:
                grid[r][c] = grid[r + 1][c]

    return grid, grid[0, start_pos]


def part_one(text: str):
    grid = np.array([[INT_MAP[val] for val in list(line)] for line in text.split("\n")])

    print(f"{grid}\n\n")

    labeled_grid, splits = label_grid(grid)

    labeled_text = "\n".join(
        [
            "".join([REVERSE_MAP.get(val, str(val)) for val in row])
            for row in labeled_grid
        ]
    )

    print(f"{text}\n----\n{labeled_text}")

    return splits


def part_two(text: str):
    grid = np.array([[INT_MAP[val] for val in list(line)] for line in text.split("\n")])

    print(f"{grid}\n\n")

    timelines, count = label_timelines(grid)

    print(count)

    return timelines, count
