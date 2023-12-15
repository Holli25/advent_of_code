from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> List[List[int]]:
    with open(path.join(data_folder, "day9.txt"), "r") as file:
        content = file.readlines()
    return [[int(i) for i in line.split(" ")] for line in content]

def find_differences(history:List[int]) -> List[int]:
    return [second - first for first, second in zip(history[:-1], history[1:])]


def part1() -> int:
    # Part 1 of the puzzle
    histories = get_input()
    output = 0

    for history in histories:
        print(f"Starting with {history}")
        # Find the differences between each number, until the differences are all 0
        steps = [history]
        while set(history) != set([0]):
            history = find_differences(history)
            steps.append(history)
        
        # find the last value by going up the chain again
        output += sum([step[-1] for step in steps])

    return output

def part2() -> int:
    # Part 2 of the puzzle
    histories = get_input()
    output = 0

    for history in histories:
        # Find the differences between each number, until the differences are all 0
        steps = [history]
        while set(history) != set([0]):
            history = find_differences(history)
            steps.append(history)

        # Extrapolate backwards, for each row the first new value is its original first value - first value from row below it
        for i in range(len(steps) - 2, -1, -1):
            steps[i].insert(0, steps[i][0] - steps[i+1][0])
        
        # Add the first value of the first row to the result
        output += steps[0][0]

    return output

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")