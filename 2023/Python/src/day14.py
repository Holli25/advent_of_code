from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> List[str]:
    with open(path.join(data_folder, "day14.txt"), "r") as file:
        content = file.readlines()
    return [line.strip() for line in content]

def tilt_north(field:List[str]) -> List[str]:
    new_field = [[field[row][col] for row in range(len(field))] for col in range(len(field[0]))]
    tilted_field = []
    for line in new_field:
        new_line = []
        for part in "".join(line).split("#"):
            o = part.count("O")
            new_part = f"{'O' * o}{'.' * (len(part) - o)}#" # Each part is connected to the next by a #, add this at the end
            new_line.append(new_part)
        tilted_field.append(("".join(new_line)[:-1])) # The last # has to be taken away, as the last part is not connected to another part
    new_field = ["".join([tilted_field[row][col] for row in range(len(field))]) for col in range(len(field[0]))]
    return new_field

def tilt_west(field):
    tilted_field = []
    for line in field:
        new_line = []
        for part in "".join(line).split("#"):
            o = part.count("O")
            new_part = f"{'O' * o}{'.' * (len(part) - o)}#" # Each part is connected to the next by a #, add this at the end
            new_line.append(new_part)
        tilted_field.append(("".join(new_line)[:-1])) # The last # has to be taken away, as the last part is not connected to another part
    return tilted_field

def tilt_south(field):
    new_field = [[field[row][col] for row in range(len(field) - 1, -1, -1)] for col in range(len(field[0]))]
    tilted_field = []
    for line in new_field:
        new_line = []
        for part in "".join(line).split("#"):
            o = part.count("O")
            new_part = f"{'O' * o}{'.' * (len(part) - o)}#" # Each part is connected to the next by a #, add this at the end
            new_line.append(new_part)
        tilted_field.append(("".join(new_line)[:-1])) # The last # has to be taken away, as the last part is not connected to another part
    new_field = ["".join([tilted_field[row][col] for row in range(len(field))]) for col in range(len(field[0]) - 1, -1, -1)]
    return new_field

def tilt_east(field):
    new_field = [[field[row][col] for col in range(len(field) -1, -1, -1)] for row in range(len(field[0]))]
    tilted_field = []
    for line in new_field:
        new_line = []
        for part in "".join(line).split("#"):
            o = part.count("O")
            new_part = f"{'O' * o}{'.' * (len(part) - o)}#" # Each part is connected to the next by a #, add this at the end
            new_line.append(new_part)
        tilted_field.append(("".join(new_line)[:-1])) # The last # has to be taken away, as the last part is not connected to another part
    new_field = ["".join([tilted_field[row][col] for col in range(len(field) -1, -1, -1)]) for row in range(len(field[0]))]
    return new_field

def one_cycle(field):
    f = tilt_north(field)
    f = tilt_west(f)
    f = tilt_south(f)
    f = tilt_east(f)

    return f

def calculate_load(field):
    output = 0
    output = sum([len(field) - row_i for row_i, row in enumerate(field) for symbol in row if symbol == "O"])
    return output

def part1() -> int:
    # Part 1 of the puzzle
    lines = get_input()

    tilted_north = tilt_north(lines)

    output = 0
    for col_i in range(len(tilted_north[0])):
        for row in tilted_north:
            if row[col_i] == "O":
                output += (len(tilted_north[0]) - col_i)
    return output



def part2() -> int:
    # Part 2 of the puzzle
    lines = get_input()
    c = lines

    seen = [c]
    
    for i in range(1, 1000):
        if i % 100 == 0:
            print(i)
        c = one_cycle(c)

        if c in seen:
            print(f"Yay, found it in {i} at {seen.index(c)}")
            break
        else:
            seen.append(c)

    a = (1000000000 - i) % (i - seen.index(c))
    print(a)

    for i in range(a):
        c = one_cycle(c)

    return calculate_load(c)


if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")