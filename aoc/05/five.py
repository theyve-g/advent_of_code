def merge_intervals(intervals: list[list[int]]):
    intervals = sorted(intervals, key=lambda r: r[0])

    merged = []
    curr_interval = intervals[0]

    for interval in intervals[1:]:
        if interval[0] > curr_interval[1] + 1:
            merged.append(curr_interval)
            curr_interval = interval
        elif curr_interval[0] <= interval[0] <= curr_interval[1] + 1:
            curr_interval = [curr_interval[0], max(interval[1], curr_interval[1])]
        else:
            raise ValueError(f"Curr: {curr_interval}, iter: {interval}")

    merged.append(curr_interval)

    return merged


def check_ingredient(ingredient: int, ranges: list[list[int]]):
    if ingredient < ranges[0][0] or ingredient > ranges[-1][1]:
        return False

    for ing_range in ranges:
        if ing_range[0] <= ingredient <= ing_range[1]:
            return True

    return False


def main(input: str):
    lines = input.split("\n")

    ranges = []
    ingredients = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "-" in line:
            lo, hi = line.split("-")
            ranges.append([int(lo), int(hi)])
        else:
            ingredients.append(int(line))

    ranges = merge_intervals(ranges)

    num_fresh = 0
    for ingredient in ingredients:
        num_fresh += int(check_ingredient(ingredient, ranges))

    num_possible_fresh = sum([r[1] - r[0] + 1 for r in ranges])

    return num_fresh, num_possible_fresh
