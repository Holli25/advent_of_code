from os import path
from typing import Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day11.txt"), "r") as file:
        content = file.readlines()
    return content

def calculate_distance(coord1:Tuple[int, int], coord2:Tuple[int, int]) -> int:
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def get_result(expansion_factor:int) -> int:
    image = get_input()
    width, height = len(image[0].strip()), len(image)

    galaxies = []
    expandable_rows = []
    expandable_cols = []

    for row_i, row in enumerate(image):
        for col_i, position in enumerate(row.strip()):
            if position == "#":
                galaxies.append((row_i, col_i))
        if len(set(row.strip())) == 1:
            expandable_rows.append(row_i)

    for column in range(width):
        if len(set([image[row][column] for row in range(height)])) == 1:
            expandable_cols.append(column)

    # Expand the rows
    new_galaxies = []
    previous_e_row = -1
    for amount, e_row in enumerate(expandable_rows):
        galaxies_to_expand = [galaxy for galaxy in galaxies if galaxy[0] < e_row and galaxy[0] > previous_e_row]
        for galaxy in galaxies_to_expand:
            new_galaxies.append((galaxy[0] + amount * expansion_factor, galaxy[1]))
        previous_e_row = e_row
    galaxies_to_expand = [galaxy for galaxy in galaxies if galaxy[0] > previous_e_row]
    for galaxy in galaxies_to_expand:
        new_galaxies.append((galaxy[0] + len(expandable_rows) * expansion_factor, galaxy[1]))

    galaxies = new_galaxies

    # Expand the cols
    new_galaxies = []
    previous_e_col = -1
    for amount, e_col in enumerate(expandable_cols):
        galaxies_to_expand = [galaxy for galaxy in galaxies if galaxy[1] < e_col and galaxy[1] > previous_e_col]
        for galaxy in galaxies_to_expand:
            new_galaxies.append((galaxy[0], galaxy[1] + amount * expansion_factor))
        previous_e_col = e_col
    galaxies_to_expand = [galaxy for galaxy in galaxies if galaxy[1] > previous_e_col]
    for galaxy in galaxies_to_expand:
        new_galaxies.append((galaxy[0], galaxy[1] + len(expandable_cols) * expansion_factor))

    galaxies = new_galaxies

    # Calculate result
    result = 0
    for index, galaxy in enumerate(galaxies):
        distances = [calculate_distance(galaxy, other_galaxy) for other_galaxy in galaxies[index + 1:]]
        result += sum(distances)
    
    return result

def part1() -> int:
    # Part 1 of the puzzle
    return get_result(1)

def part2() -> int:
    # Part 2 of the puzzle
    return get_result(999999)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")