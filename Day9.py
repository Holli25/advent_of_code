from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> List[List[int]]:
    if testing:
        filename = "Test_inputs/Day9.txt"
    else:
        filename = "Inputs/Day9.txt"

    heights: List[List[int]] = []
    with open(filename) as file:
        for line in file:
            heights.append([int(i) for i in line.rstrip()])

    return heights

def find_candidates_in_row(row: List[int]) -> List[int]:
    # Function tests if neighboring points in a row are higher than the current point
    candidate_indices: List[int] = []
    for index, height in enumerate(row):
        if index == 0:
            if height < row[index + 1]:
                candidate_indices.append(index)
        elif index == len(row) - 1:
            if height < row[index - 1]:
                candidate_indices.append(index)
        else:
            if height < row[index + 1] and height < row[index - 1]:
                candidate_indices.append(index)

    return candidate_indices

def position_is_local_low(heights: List[List[int]], row_number: int, index: int) -> bool:
    # Function tests if neighboring points in height list are also higher than the current point
    current_value: int = heights[row_number][index]
    if row_number == 0:
        return current_value < heights[row_number + 1][index]
    elif row_number == len(heights) - 1:
        return current_value < heights[row_number - 1][index]
    else:
        return current_value < heights[row_number + 1][index] and current_value < heights[row_number - 1][index]

def find_candidates_in_field(heights: List[List[int]]) -> Dict[int, List[int]]:
    return {row_number:find_candidates_in_row(row) for row_number, row in enumerate(heights) if find_candidates_in_row(row)}

def find_local_lows(heights: List[List[int]], candidates: Dict[int, List[int]]) -> List[List[int]]:
    return [[row_number, candidate_index] for row_number, candidate_list in candidates.items() for candidate_index in candidate_list if position_is_local_low(heights, row_number, candidate_index)]


def part_one() -> int:
    inputs = read_data(False)
    candidates: Dict[int, List[int]] = find_candidates_in_field(inputs)
    local_lows = find_local_lows(inputs, candidates)
    return sum([inputs[row_number][candidate_index] + 1 for row_number, candidate_index in local_lows])

i = read_data(True)
c = find_candidates_in_field(i)
l = find_local_lows(i, c)

print(l)



# print(part_one())
