from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day13.txt"), "r") as file:
        content = file.read().split("\n\n")

    return content

def is_mirrored(rows1:List[str], rows2:List[str]) -> bool:
    for i, j in zip(rows1[::-1], rows2):
        if i != j:
            return False
    return True

def part1() -> int:
    # Part 1 of the puzzle
    fields = get_input()
    col_values = 0
    row_values = 0

    for field in fields:
        new_field = field.replace("#", "1")
        new_field = new_field.replace(".", "0")

        # Find horizontal mirrors
        new_field = new_field.split("\n")
        for row_i in range(1, len(new_field)):
            end = row_i * 2 if row_i * 2 <= len(new_field) else len(new_field)
            if is_mirrored(new_field[:row_i], new_field[row_i:end]):
                row_values += row_i
        
        # Find vertical mirrors
        for col_i in range(1, len(new_field[0])):
            left = ["".join([new_field[r][c] for r in range(len(new_field))]) for c in range(col_i)]
            right = ["".join([new_field[r][c] for r in range(len(new_field))]) for c in range(col_i, min(col_i*2, len(new_field[0])))]
            if is_mirrored(left, right):
                col_values += col_i

    return 100 * row_values + col_values
            


def part2() -> int:
    # Part 2 of the puzzle
    pass

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")