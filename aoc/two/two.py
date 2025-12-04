"""
--- Day 2: Gift Shop ---
You get inside and take the elevator to its only other stop: the gift shop. "Thank you for visiting the North Pole!" gleefully exclaims a nearby sign. You aren't sure who is even allowed to visit the North Pole, but you know you can access the lobby through here, and from there you can access the rest of the North Pole base.

As you make your way through the surprisingly extensive selection, one of the clerks recognizes you and asks for your help.

As it turns out, one of the younger Elves was playing on a gift shop computer and managed to add a whole bunch of invalid product IDs to their gift shop database! Surely, it would be no trouble for you to identify the invalid product IDs for them, right?

They've even checked most of the product ID ranges already; they only have a few product ID ranges (your puzzle input) that you'll need to check. For example:

11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
(The ID ranges are wrapped here for legibility; in your input, they appear on a single long line.)

The ranges are separated by commas (,); each range gives its first ID and last ID separated by a dash (-).

Since the young Elf was just doing silly patterns, you can find the invalid IDs by looking for any ID which is made only of some sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.

None of the numbers have leading zeroes; 0101 isn't an ID at all. (101 is a valid ID that you would ignore.)

Your job is to find all of the invalid IDs that appear in the given ranges. In the above example:

11-22 has two invalid IDs, 11 and 22.
95-115 has one invalid ID, 99.
998-1012 has one invalid ID, 1010.
1188511880-1188511890 has one invalid ID, 1188511885.
222220-222224 has one invalid ID, 222222.
1698522-1698528 contains no invalid IDs.
446443-446449 has one invalid ID, 446446.
38593856-38593862 has one invalid ID, 38593859.
The rest of the ranges contain no invalid IDs.
Adding up all the invalid IDs in this example produces 1227775554.
"""

from collections import deque
from math import floor


def get_digits(number: int):
    digits: deque[int] = deque([])
    while number > 0:
        number, digit = number // 10, number % 10
        digits.appendleft(digit)

    return digits


def construct(digits: deque[int] | list):
    number = 0
    multiplier = 1
    index = len(digits) - 1
    while index >= 0:
        digit = digits[index]
        number += multiplier * digit

        multiplier *= 10
        index -= 1

    return number


# PART 1
def get_invalid_ids(min_val: int, max_val: int):
    invalid_ids: list[int] = []

    digits = get_digits(min_val)
    pos = floor(len(digits) / 2)

    left = construct(list(digits)[:pos])
    multiplier = 10**pos

    number = left * multiplier + left

    while number <= max_val:
        if number >= min_val:
            invalid_ids.append(number)

        left += 1
        if left == multiplier:
            multiplier *= 10

        number = left * multiplier + left

    return invalid_ids


def part_one(input: str):
    invalid_id_sum = 0

    ranges = input.split(",")
    for range in ranges:
        min_val, max_val = range.split("-")
        invalid_ids = get_invalid_ids(int(min_val), int(max_val))

        print(f"Range: {range}\n{invalid_ids}")

        invalid_id_sum += sum(invalid_ids)

    return invalid_id_sum


# PART 2
def get_all_repititions(pattern: int, multitipler: int, max_val: int):
    invalid_ids: list[int] = []
    number = pattern * multitipler + pattern
    while number <= max_val:
        invalid_ids.append(number)

        number = number * multitipler + pattern

    return invalid_ids


def process_range(min_val: str, max_val: str):
    multiplier = 10
    pattern = 1

    max_value = int(max_val)

    all_invalid_ids = []

    while True:
        invalid_ids = get_all_repititions(pattern, multiplier, max_value)

        if not invalid_ids:
            break

        invalid_ids = [id for id in invalid_ids if id >= int(min_val)]
        # print(f"{number} x {pattern} x {multiplier}\n{invalid_ids}")

        all_invalid_ids.extend(invalid_ids)
        if set(str(pattern)) == {"9"}:
            multiplier *= 10

        pattern += 1

    return sorted(set(all_invalid_ids))


def part_two(input: str):
    invalid_id_sum = 0

    ranges = input.split(",")
    for range in ranges:
        min_val, max_val = range.split("-")

        invalid_ids = process_range(min_val, max_val)
        print(f"{range}\n{invalid_ids}")

        invalid_id_sum += sum(invalid_ids)

    return invalid_id_sum
