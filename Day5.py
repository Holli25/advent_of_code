from typing import List, Tuple

def read_data(test:bool) -> List[List[List[int]]]:
    input: List[List[List[int]]] = []
    if test:
        input_file = "Test_inputs/Day5.txt"
    else:
        input_file = "Inputs/Day5.txt"
    with open(input_file) as file:
        for line in file:
            start, end = split_line_into_components(line)
            direction = get_direction(start, end)
            input.append([start, end, direction])
    return input

def split_line_into_components(line: str) -> Tuple[List[int], List[int]]:
    start, end = line.rstrip().split(" -> ")
    start = [int(number) for number in start.split(",")]
    end = [int(number) for number in end.split(",")]
    return start, end

def get_direction(start: List[int], end: List[int]) -> int:
    if start[0] == end[0]:
        return 1
    elif start[1] == end[1]:
        return 0
    else:
        return -1

def trim_diagonal_vents(inputs) -> List[List[List[int]]]:
    return [vent for vent in inputs if vent[2] >= 0]

def map_horizontal_vent(board: List[List[int]], vent: List[List[int]]) -> List[List[int]]:
    x_start, x_end = vent[0][0], vent[1][0]
    if x_start > x_end:
        x_start, x_end = x_end, x_start
    for x_position in range(x_start,x_end + 1):
        board[x_position][vent[0][1]] += 1

    return board

def map_vertical_vent(board: List[List[int]], vent: List[List[int]]) -> List[List[int]]:
    y_start, y_end = vent[0][1], vent[1][1]
    if y_start > y_end:
        y_start, y_end = y_end, y_start
    for y_position in range(y_start,y_end + 1):
        board[vent[0][0]][y_position] += 1

    return board

def map_diagonal_vent(board: List[List[int]], vent: List[List[int]]) -> List[List[int]]:
    x_start, y_start, x_end, y_end = vent[0][0], vent[0][1], vent[1][0], vent[1][1]
    if x_start > x_end:
        x_start, y_start, x_end, y_end = x_end, y_end, x_start, y_start
    vent_length = x_end - x_start + 1
    # Vent goes from bottom left to top right
    if y_start > y_end:
        for i in range(vent_length):
            board[x_start + i][y_start - i] += 1
    # Vent goes from top left to bottom right
    elif y_start < y_end:
        for i in range(vent_length):
            board[x_start + i][y_start + i] += 1
    else:
        raise Exception(f"The vent with coordinates {x_start, y_start, x_end, y_end} can not be mapped")

    return board

def map_vents_on_board(board: List[List[int]], vents: List[List[List[int]]]) -> List[List[int]]:
    for vent in vents:
        if vent[2] == 0:
            board = map_horizontal_vent(board, vent)
        elif vent[2] == 1:
            board = map_vertical_vent(board, vent)
        elif vent[2] == -1:
            board = map_diagonal_vent(board, vent)
    return board


def count_overlapping_vents(board: List[List[int]]) -> int:
    return sum([1 for column in board for row in column if row >= 2])


def part_one() -> int:
    input = read_data(False)
    vents = trim_diagonal_vents(input)

    board = [[0 for i in range(1000)] for j in range(1000)]
    board = map_vents_on_board(board, vents)
    return count_overlapping_vents(board)

def part_two() -> int:
    vents = read_data(False)

    board = [[0 for i in range(1000)] for j in range(1000)]
    board = map_vents_on_board(board, vents)
    return count_overlapping_vents(board)


print(part_one())
print(part_two())
