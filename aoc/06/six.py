import numpy as np
from numpy import ndarray


def process(input: ndarray, operations: list[str]):
    result = 0
    for idx, operation in enumerate(operations):
        if operation == "*":
            res = np.prod(input[:, idx])
        elif operation == "+":
            res = np.sum(input[:, idx])
        else:
            raise ValueError(operation)

        result += res

    return result


def main(text: str):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    input = np.array([[int(num) for num in line.split()] for line in lines[:-1]])
    operations = lines[-1].split()

    result = process(input, operations)

    return result


def process_operation(operation: str, numbers: list[int]):
    solution = 0
    if operation == "*":
        solution += np.prod(numbers)
    elif operation == "+":
        solution += np.sum(numbers)
    else:
        raise ValueError(operation)

    return solution


def part_two(text: str):
    lines = text.split("\n")
    width = max(len(line) for line in lines)

    solution = 0

    numbers = []
    operation = ""

    for col in range(width):
        if col < len(lines[-1]) and lines[-1][col] in {"*", "+"}:
            if operation != "":
                raise ValueError(operation)
            operation = lines[-1][col]

        vert = "".join(line[col] for line in lines[:-1] if col < len(line)).strip()

        if vert == "":
            solution += process_operation(operation, numbers)

            operation = ""
            numbers = []
        else:
            numbers.append(int(vert))

    solution += process_operation(operation, numbers)

    return solution
