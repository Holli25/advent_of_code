from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> Tuple[List[int], int]:
    if testing:
        filename = "Test_inputs/Day17.txt"
    else:
        filename = "Inputs/Day17.txt"

    with open(filename) as file:
        line = file.readline().strip()

    parts = line.split("..")
    xmin = int(parts[0].split("x=")[1])
    xmax = int(parts[1].split(",")[0])
    ymax = int(parts[1].split("y=")[1])
    ymin = int(parts[2])
    return (xmin, xmax, ymin, ymax)

def one_step(position: Tuple[int, int], x_current: int, y_current: int) -> Tuple[Tuple[int, int], int, int]:
    new_position = (position[0] + x_current, position[1] + y_current)
    if x_current > 0:
        x_new = x_current - 1
    elif x_current < 0:
        x_new = x_current + 1
    else:
        x_new = x_current
    y_new = y_current - 1
    return (new_position, x_new, y_new)

def create_target_region(input: Tuple[int, int, int, int]) -> Tuple[List[int], List[int]]:
    return ([x for x in range(input[0], input[1] + 1)], [y for y in range(input[2], input[3] - 1, -1)])

def test_value_pair(target_region: Tuple[List[int], List[int]], x: int, y: int) -> Tuple[bool, int]:
    position = (0,0)
    highest_point: int = 0
    while True:
        position, x, y = one_step(position, x, y)
        if position[1] > highest_point:
            highest_point = position[1]
        # print(f"Current position is: {position} with x-speed of {x} and y-speed of {y}.")
        if position[0] in target_region[0] and position[1] in target_region[1]:
            return True, highest_point
        elif position[0] > max(target_region[0]) or position[1] < min(target_region[1]):
            return False, highest_point

def test_values(target_region: Tuple[List[int], List[int]]) -> int:
    x_distance_to_start = min(target_region[0])
    y_width = target_region[1][0] - target_region[1][-1]
    y_search_start = int(y_width * 2 - y_width)
    y_search_end = int(y_width * 2 + y_width)
    y_max: int = 0
    coords: Tuple[int, int] = (0,0)
    for x in range(x_distance_to_start):
        for y in range(y_search_start, y_search_end):
            successful, height = test_value_pair(target_region, x, y)
            if successful and height > y_max:
                y_max = height
                coords = (x, y)
    return y_max, coords

def count_hits(target_region: Tuple[List[int], List[int]], highest_y: int) -> int:
    x_start: int = find_starting_x(target_region[0])
    x_end: int = find_end_x(target_region[0], x_start)
    hits = 0
    for x in range(x_start, max(target_region[0]) + 1):
        for y in range(highest_y, min(target_region[1]) - 1, -1):
            successful, _ = test_value_pair(target_region, x, y)
            if successful:
                hits += 1
    return hits

def find_starting_x(target_range: List[int]) -> int:
    for x in range(min(target_range)):
        if int((x * (x + 1)) / 2) in target_range:
            return x
    return None

def find_end_x(target_range: List[int], starting_x: int) -> int:
    for x in range(starting_x, min(target_range)):
        if int((x * (x + 1)) / 2) not in target_range:
            return x
    return None

def part_one() -> int:
    input = read_data()
    target_region = create_target_region(input)
    y_max, _ = test_values(target_region)
    return y_max

def part_two() -> int:
    input = read_data()
    target_region = create_target_region(input)
    _, coords = test_values(target_region)
    return count_hits(target_region, coords[1])

print(part_one())
print(part_two())
