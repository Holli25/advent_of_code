from os import path
from typing import Dict, List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = False
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

DIRECTIONS = {"R":complex(1,0), "L":complex(-1,0), "D":complex(0,1), "U":complex(0,-1)}

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day18.txt"), "r") as file:
        content = file.readlines()
    output = []
    for line in content:
        direction, amount, color = line.strip().split()
        output.append((DIRECTIONS.get(direction), int(amount)))
    return output

def flood_recursive(field:Dict[complex, str], walls:List[complex], width:int, height:int):
    o = [complex(143, 1)]

    while o:
        pos = o.pop(0)
        print(pos)
        field[pos] = "O"
        for neighbor in map(lambda x:pos + x, [complex(1,0), complex(-1,0), complex(0,1), complex(0,-1)]):
            if field.get(neighbor) and not neighbor in walls and not field.get(neighbor) == "O" and not neighbor in o:
                o.append(neighbor)
    return field

def part1() -> int:
    # Part 1 of the puzzle
    digs = get_input()
    start = complex(0,0)
    
    vertices = [start]
    current = start

    for direction, amount in digs:
        current = current + (direction * amount)
        vertices.append(current)

    output = 0
    for a, b in zip(vertices[:-1], vertices[1:]):
        output += (a.real * b.imag)
        output -= (a.imag * b.real)
        print(output)
    return output
    # walls = []
    # current = complex(0,0)
    # for direction, amount in digs:
    #     for _ in range(amount):
    #         current += direction
    #         walls.append(current)

    # left = min([int(pos.real) for pos in walls])
    # right = max([int(pos.real) for pos in walls])
    # top = min([int(pos.imag) for pos in walls])
    # bottom = max([int(pos.imag) for pos in walls])

    # field = {complex(j, i):"#" if complex(j, i) in walls else "." for i in range(top, bottom + 1) for j in range(left, right + 1)}
    # width = right + 1 - left
    # height = bottom + 1 - top


    # flooded = flood_recursive(field, walls, width, height)
    # a_f = sum([1 for i, j in flooded.items() if j == "O" or j == "#"])
    # return a_f # 49061 for my dataset


def part2() -> int:
    # Part 2 of the puzzle
    pass

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")