from os import path
import re
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

class Number():
    def __init__(self, value:int, row:int, start:int, length:int):
        self.value = value
        self.row = row
        self.start = start
        self.length = length
        self.positions = [i for i in range(self.start, self.length)]
        self.valid = False

    def validate(self):
        self.valid = True
    
    def __repr__(self):
        return f"Number: {self.value} in row {self.row}, at positions {self.positions}"

class Sign():
    def __init__(self, row:int, col:int):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"Sign: {self.row} at position {self.col}"

# Open and prepare input
def get_input() -> List[str]:
    with open(path.join(data_folder, "day3.txt"), "r") as file:
        content = file.readlines()
    return content

def part1() -> int:
    # Part 1 of the puzzle
    lines = get_input()
    numbers = []
    signs = []

    for row, line in enumerate(lines):
        # Get all numbers first
        for number in re.finditer("\d+", line):
            start, length = number.span()
            numbers.append(Number(int(number.group(0)), row, start, length))
        
        # Next, get all the signs (#-*+@/%$&=); characters # and * have to be at the end of the pattern, otherwise it did not find the symbol right after
        for sign in re.finditer("[-+@/%$&=*#]", line):
            start, _ = sign.span()
            signs.append(Sign(row, start))
            print(f"{sign}; Row: {row}, Col: {start}")
    
    for sign in signs:
        possible_rows = [row for row in range(sign.row - 1, sign.row + 2)]
        possible_cols = [col for col in range(sign.col - 1, sign.col + 2)]

        for number in numbers:
            if number.row in possible_rows:
                for position in number.positions:
                    if position in possible_cols:
                        number.validate()

    final = sum([number.value for number in numbers if number.valid])
    return final


def part2() -> int:
    # Part 2 of the puzzle
    lines = get_input()
    numbers = []
    signs = []
    gear_ratios = []

    for row, line in enumerate(lines):
        # Get all numbers first
        for number in re.finditer("\d+", line):
            start, length = number.span()
            numbers.append(Number(int(number.group(0)), row, start, length))
        
        # Only the gearboxes (*) count
        for sign in re.finditer("\*", line):
            start, _ = sign.span()
            signs.append(Sign(row, start))
            print(f"{sign}; Row: {row}, Col: {start}")
    
    for sign in signs:
        possible_rows = [row for row in range(sign.row - 1, sign.row + 2)]
        possible_cols = [col for col in range(sign.col - 1, sign.col + 2)]
        neighbors = 0
        neighbor_values = []

        for number in numbers:
            if number.row in possible_rows:
                for position in number.positions:
                    if position in possible_cols:
                        neighbors += 1
                        neighbor_values.append(number.value)
                        break # break is needed should number have more than one position that is in the gear reach
        if neighbors == 2:
            gear_ratios.append(neighbor_values[0] * neighbor_values[1])

    return sum(gear_ratios)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")