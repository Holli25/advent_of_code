from os import path
import re
from typing import Dict, List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

PART1 = {"red":12, "green":13, "blue":14}

# Open and prepare input
def get_input() -> List[str]:
    with open(path.join(data_folder, "day2.txt"), "r") as file:
        content = file.readlines()
    return content

def part1() -> int:
    # Part 1 of the puzzle
    games = get_input()
    output = 0

    for game in games:
        possible = True

        # Game ID is at beginning of string in format "Game xxx", all the cube pulls come after in format x color, y color; a color, b color
        game_id = int(re.match("Game (\d{1,3})", game)[1])
        game_info = game.split(": ")[1]

        for pull in game_info.split("; "):
            cubes = re.findall("(\d+) (red|green|blue)", pull)
            for cube in cubes:
                if int(cube[0]) > PART1.get(cube[1]):
                    possible = False
                    break
            if not possible:
                break
        
        if possible:
            output += game_id
        
    return output


def part2() -> int:
    # Part 2 of the puzzle
    games = get_input()
    output = 0

    for game in games:
        minimal_cubes:Dict[str, int] = {"red":0, "green":0, "blue":0}

        game_info = game.split(": ")[1]

        for pull in game_info.split(";"):
            cubes = re.findall("(\d+) (red|green|blue)", pull)
            for cube in cubes:
                minimal_cubes[cube[1]] = max(minimal_cubes[cube[1]], int(cube[0]))
        
        output += (minimal_cubes.get("red") * minimal_cubes.get("green") * minimal_cubes.get("blue"))

    return output

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")