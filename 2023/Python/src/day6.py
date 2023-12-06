from os import path
import re

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day6.txt"), "r") as file:
        content = file.readlines()
    
    for line in content:
        if line.startswith("Time:"):
            times = re.findall("\d+", line)
        elif line.startswith("Distance:"):
            distances = re.findall("\d+", line)
    
    return zip(times, distances)

def part1() -> int:
    # Part 1 of the puzzle
    output = 1

    for time, distance in get_input():
        time, distance = int(time), int(distance)
        # Even time means that the middle is one value; the next values can be tested with the formula: middle_value - x^2 > distance
        if time % 2 == 0:
            middle_value = (time / 2) **2
            if middle_value > distance: 
                better_options = 1
                for i in range(1, time):
                    if middle_value - i**2 > distance:
                        better_options += 2
                    else:
                        break
            else:
                better_options = 0

        # Uneven time means that there are two middle values; the next values can be tested with the formula: middle_value - (x^2 + x) > distance
        else:
            middle_value = (time // 2) * (time // 2 + 1 )
            if middle_value > distance:
                better_options = 2
                for i in range(1, time):
                    if middle_value - i**2 - i > distance:
                        better_options += 2
                    else:
                        break
            else:
                better_options = 0
        
        output *= better_options

    return output


def part2() -> int:
    # Part 2 of the puzzle
    information = [[time, distance] for time, distance in get_input()]
    time = int("".join([i[0] for i in information]))
    distance = int("".join([i[1] for i in information]))

    # Even time means that the middle is one value; the next values can be tested with the formula: middle_value - x^2 > distance
    if time % 2 == 0:
        middle_value = (time / 2) **2
        if middle_value > distance: 
            better_options = 1
            for i in range(1, time):
                if middle_value - i**2 > distance:
                    better_options += 2
                else:
                    break
        else:
            better_options = 0

    # Uneven time means that there are two middle values; the next values can be tested with the formula: middle_value - (x^2 + x) > distance
    else:
        middle_value = (time // 2) * (time // 2 + 1 )
        if middle_value > distance:
            better_options = 2
            for i in range(1, time):
                if middle_value - i**2 - i > distance:
                    better_options += 2
                else:
                    break
        else:
            better_options = 0

    return better_options

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")