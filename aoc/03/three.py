import numpy as np


def process_bank_(bank: str):
    left, right = bank[0], bank[1]

    for char in bank[2:]:
        if right > left:
            left = right
            right = char
        elif char >= right:
            right = char

    return int(left + right)


def process_bank(bank: str, num: int):
    voltage = []
    digits = list(bank)

    max_idx = len(bank)
    while num > 0:
        best_idx = np.argmax(digits[: max_idx - num + 1])
        voltage.append(digits[best_idx])

        digits = digits[best_idx + 1 :]
        num -= 1
        max_idx = len(digits)

    return int("".join(voltage))


def one(lines: list[str]):
    total_voltage = 0
    for line in lines:
        voltage = process_bank(line, 12)
        print(f"{line}: {voltage}")
        total_voltage += voltage

    return total_voltage
