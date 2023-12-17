from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> List[str]:
    with open(path.join(data_folder, "day16.txt"), "r") as file:
        content = file.readlines()
    return [line.strip() for line in content]

def move(coord1:Tuple[int, int], coord2:Tuple[int, int]) -> Tuple[int, int]:
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def position_in_bounds(position:Tuple[int, int], cavern:List[str]) -> bool:
    return position[0] >= 0 and position[0] < len(cavern) and position[1] >= 0 and position[1] < len(cavern[0])

def get_direction(symbol:str, direction:Tuple[int, int]) -> Tuple[int, int]:
    if symbol == ".":
        return direction
    
    elif symbol == "/":
        if direction in [(1,0), (-1,0)]:
            return (0, -direction[0])
        else:
            return (-direction[1], 0)
        
    elif symbol == "\\":
        if direction in [(1,0), (-1,0)]:
            return (0, direction[0])
        else:
            return (direction[1], 0)

    elif symbol == "-":
        if direction in [(0,1), (0,-1)]:
            return direction
        else:
            return (0,1)
    
    elif symbol == "|":
        if direction in [(1,0), (-1,0)]:
            return direction
        else:
            return (1,0)

def follow_light(todo):
    seen = []

    while todo:
        current, direction = todo.pop()
        while position_in_bounds(current, CAVERN) and (current, direction) not in seen:
            seen.append((current, direction))
            current_symbol = CAVERN[current[0]][current[1]]
            direction = get_direction(current_symbol, direction)
            if current_symbol in "|-":
                inverse_direction = (-direction[0], -direction[1])
                inverse_field = move(current, inverse_direction)
                todo.append((inverse_field, inverse_direction))

            current = move(current, direction)
    return len(set(pos for pos, _ in seen))

# def follow_light(current: Tuple[int, int], seen_fields:Tuple[Tuple[int, int]], direction:Tuple[int, int]) -> List[Tuple[int, int]]:
#     next_field = move(current, direction)
#     next_direction = direction
#     my_seen = seen_fields
#     while [next_field, next_direction] not in my_seen and position_in_bounds(next_field, cavern):
#         current = next_field
#         # open("log16_2.txt", "a").write(f"{current}\n")
#         current_symbol = cavern[current[0]][current[1]]
#         my_seen.append((current, next_direction))
#         next_direction = get_direction(current_symbol, next_direction)
#         if current_symbol in "|-":
#             inverse_direction = (-next_direction[0], -next_direction[1])
#             print(f"Splitting at {current} because {current_symbol}, now going {inverse_direction}, originally {next_direction} coming from {next_field}")
#             return follow_light(current, cavern, my_seen, next_direction) + follow_light(current, cavern, my_seen, inverse_direction)
#         else:
#             next_field = move(current, next_direction)
#     return my_seen

def part1() -> int:
    # Part 1 of the puzzle
    global CAVERN

    CAVERN = get_input()

    all_seen = follow_light([((0,0), (0,1))])
    return all_seen


def part2() -> int:
    # Part 2 of the puzzle
    g = {complex(i,j): c for j, r in enumerate(open(path.join(data_folder, "day16.txt")))
                     for i, c in enumerate(r.strip())}

    def fn(todo):
        done = set()
        while todo:
            pos, dir = todo.pop()
            while not (pos, dir) in done:
                done.add((pos, dir))
                pos += dir
                match g.get(pos):
                    case '|': dir = 1j; todo.append((pos, -dir))
                    case '-': dir = -1; todo.append((pos, -dir))
                    case '/': dir = -complex(dir.imag, dir.real)
                    case '\\': dir = complex(dir.imag, dir.real)
                    case None: break

        return len(set(pos for pos, _ in done)) - 1

    return max(map(fn, ([(pos-dir, dir)] for dir in (1,1j,-1,-1j)
                            for pos in g if pos-dir not in g)))

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")