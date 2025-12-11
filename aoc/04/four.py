def label_grid(grid: list[list[str]]):
    R, C = len(grid), len(grid[0])

    valid_count = 0
    for r in range(R):
        for c in range(C):
            count = 0

            if grid[r][c] == ".":
                continue

            for row_diff in [-1, 0, 1]:
                for col_diff in [-1, 0, 1]:
                    if row_diff == 0 and col_diff == 0:
                        continue

                    new_row, new_col = r + row_diff, c + col_diff
                    if (
                        0 <= new_row < R
                        and 0 <= new_col < C
                        and grid[new_row][new_col] in {"@", "x"}
                    ):
                        count += 1

            if count < 4:
                grid[r][c] = "x"
                valid_count += 1

    return grid, valid_count


def main(text: str):
    rounds = 1

    total_count = 0

    while rounds:
        grid = [list(line) for line in text.split()]
        labeled_grid, count = label_grid(grid)

        labeled_text = "\n".join(["".join(row) for row in labeled_grid])

        print(f"---\n{text}\n--\n{labeled_text}")

        text = labeled_text.replace("x", ".")

        if count == 0:
            break

        total_count += count
        # rounds -= 1

    return total_count
