from os import path
from typing import Dict, List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day21.txt"), "r") as file:
        content = file.readlines()
    open_tiles = [complex(col_i, row_i) for row_i, row in enumerate(content) for col_i, symbol in enumerate(row.strip()) if symbol in ".S"]
    for i, row in enumerate(content):
        if "S" in row:
            start = complex(row.index("S"), i)
    return start, {tile:[tile + move for move in [complex(1,0), complex(-1,0), complex(0,1), complex(0,-1)] if tile + move in open_tiles] for tile in open_tiles}

def step(tiles:Dict[complex, List[complex]], positions:List[complex]) -> List[complex]:
    return list(set([tile for position in positions for tile in tiles.get(position)]))

def part1() -> int:
    # Part 1 of the puzzle
    start, tiles = get_input()
    print(start)
    s = [start]
    for i in range(64):
        print(i)
        s = step(tiles, s)
    return len(s)

def part2() -> int:
    # Part 2 of the puzzle
    pass

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")