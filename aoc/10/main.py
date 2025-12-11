"""
--- Day 10: Factory ---
Just across the hall, you find a large factory. Fortunately, the Elves here have plenty of time to decorate. Unfortunately, it's because the factory machines are all offline, and none of the Elves can figure out the initialization procedure.

The Elves do have the manual for the machines, but the section detailing the initialization procedure was eaten by a Shiba Inu. All that remains of the manual are some indicator light diagrams, button wiring schematics, and joltage requirements for each machine.

For example:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The manual describes one machine per line. Each line contains a single indicator light diagram in [square brackets], one or more button wiring schematics in (parentheses), and joltage requirements in {curly braces}.

To start a machine, its indicator lights must match those shown in the diagram, where . means off and # means on. The machine has the number of indicator lights shown, but its indicator lights are all initially off.

So, an indicator light diagram like [.##.] means that the machine has four indicator lights which are initially off and that the goal is to simultaneously configure the first light to be off, the second light to be on, the third to be on, and the fourth to be off.

You can toggle the state of indicator lights by pushing any of the listed buttons. Each button lists which indicator lights it toggles, where 0 means the first light, 1 means the second light, and so on. When you push a button, each listed indicator light either turns on (if it was off) or turns off (if it was on). You have to push each button an integer number of times; there's no such thing as "0.5 presses" (nor can you push a button a negative number of times).

So, a button wiring schematic like (0,3,4) means that each time you push that button, the first, fourth, and fifth indicator lights would all toggle between on and off. If the indicator lights were [#.....], pushing the button would change them to be [...##.] instead.

Because none of the machines are running, the joltage requirements are irrelevant and can be safely ignored.

You can push each button as many times as you like. However, to save on time, you will need to determine the fewest total presses required to correctly configure all indicator lights for all machines in your list.

There are a few ways to correctly configure the first machine:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
You could press the first three buttons once each, a total of 3 button presses.
You could press (1,3) once, (2,3) once, and (0,1) twice, a total of 4 button presses.
You could press all of the buttons except (1,3) once each, a total of 5 button presses.
However, the fewest button presses required is 2. One way to do this is by pressing the last two buttons ((0,2) and (0,1)) once each.

The second machine can be configured with as few as 3 button presses:

[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
One way to achieve this is by pressing the last three buttons ((0,4), (0,1,2), and (1,2,3,4)) once each.

The third machine has a total of six indicator lights that need to be configured correctly:

[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The fewest presses required to correctly configure it is 2; one way to do this is by pressing buttons (0,3,4) and (0,1,2,4,5) once each.

So, the fewest button presses required to correctly configure the indicator lights on all of the machines is 2 + 3 + 2 = 7.

Analyze each machine's indicator light diagram and button wiring schematics. What is the fewest button presses required to correctly configure the indicator lights on all of the machines?
"""

import pulp
import heapq
import re


def get_state(state: str):

    state_val = 0
    for pow, digit in enumerate(state[::-1]):
        state_val += (10 ** pow) * int(digit)

    return state_val


def reverse_state(state: int, count: int):
    state = str(state)
    return "0" * (count - len(state)) + state


def apply(state: str, button: set[int]):
    return "".join([str(1-int(state[i])) if i in button else state[i] for i in range(len(state))])


def dp(buttons: list[set[int]], goal: str):
    queue = [(1, apply(goal, b)) for b in buttons]
    heapq.heapify(queue)

    visited = {goal}

    while queue:
        steps, node = heapq.heappop(queue)

        if node in visited:
            continue
        if node == "0" * len(goal):
            return steps

        visited.add(node)

        for b in buttons:
            new_node = apply(node, b)

            if new_node == "0" * len(goal):
                return steps + 1

            if new_node not in visited:
                heapq.heappush(queue, (steps+1, new_node))



def parse_line(line: str) :
    """
    Parse a line with format: [pattern] (tuple1) (tuple2) ... {set}
    
    Example:
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
    
    Returns:
        ParsedData with pattern, list of sets, and final set of integers
    """
    line = line.strip()
    
    # Extract pattern (content between square brackets)
    pattern_match = re.search(r'\[(.*?)\]', line)
    pattern = pattern_match.group(1) if pattern_match else ""
    pattern = pattern.replace(".", "0").replace("#", "1")
    
    # Extract all tuples and convert to sets
    tuple_matches = re.findall(r'\(([^)]*)\)', line)
    buttons = []
    for match in tuple_matches:
        # Split by comma and convert to set of integers
        numbers = {int(x.strip()) for x in match.split(',') if x.strip()}
        buttons.append(numbers)
    
    # Extract final set (content between curly braces)
    voltage_match = re.search(r'\{([^}]*)\}', line)
    voltages = set()
    if voltage_match:
        numbers_str = voltage_match.group(1)
        voltages = [int(x.strip()) for x in numbers_str.split(',') if x.strip()]
    
    return pattern, buttons, voltages


def part_one(text: str):
    result = []

    for line in text.split("\n"):
        goal, buttons, voltages = parse_line(line)
        res = dp(buttons, goal)
        result.append(res)

    return result, sum(result)



def solve(buttons: list[set[int]], goal: list[int]):

    problem = pulp.LpProblem("min", pulp.LpMinimize)

    variables = [pulp.LpVariable(f"b_{idx}", 0, None, pulp.LpInteger) for idx in range(len(buttons))]

    problem += sum(variables), "Number of pushes"

    for light, val in enumerate(goal):
        relevant_vars = [var for idx, var in enumerate(variables) if light in buttons[idx]]
        problem += sum(relevant_vars) == val, f"light_{light}"

    problem.solve()

    presses = []

    for v in problem.variables():
        print(v.name, "=", v.varValue)
        presses.append(int(v.varValue))

    return presses


def part_two(text: str):
    result = []

    for line in text.split("\n"):
        _, buttons, goal = parse_line(line)
        res = solve(buttons, goal)
        result.append(sum(res))

    return result, sum(result)


