import re
from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Translations for written numbers
NUMBERS = {"one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9"}

# Open and prepare input
def get_input() -> List[str]:
    with open(path.join(data_folder, "day1.txt"), "r") as file:
        content = file.readlines()
    return content

def part1() -> int:
    # Part 1 of the puzzle
    input = get_input()
    output = 0
    for line in input:
        digits = re.findall("[0-9]", line)
        calibration_value = int(digits[0] + digits[-1])
        output += calibration_value
    
    return output

def part2() -> int:
    # Part 2 of the puzzle
    # Solution finds the index of the first or last digit and saves the number found at this position
    input = get_input()
    output = 0

    for line in input:
        # Initialize the current lowest and highest position of a found number to the max (end of string for low; 0 for high); initialize the digit that is found at the lowest or highest position to 0
        low, high = len(line),0
        low_digit, high_digit = 0,0

        for w_digit, digit in NUMBERS.items():
            # Search for e.g. 1 and "one" and mark the first position, if not found save the highest position possible as throwaway value
            w_digit_index = len(line) if line.find(w_digit) < 0 else line.find(w_digit)
            digit_index = len(line) if line.find(digit) < 0 else line.find(digit)

            # If the found position is lower than the current lowest position, save the digit as the new lowest digit
            if w_digit_index < low or digit_index < low:
                low = min(w_digit_index, digit_index)
                low_digit = int(digit)

            # Search for e.g. 1 and "one" and mark the last position, if not found save 0 as throwaway value
            w_digit_index = line.rfind(w_digit)
            digit_index = line.rfind(digit)

            # If the found position is higher than the current highest position, save the digit as the new highest digit 
            if w_digit_index > high or digit_index > high:
                high = max(w_digit_index, digit_index)
                high_digit = int(digit)

        # If there is only one digit found, the highest value will still be zero; to circumvent mistakes, use the low_digit double in this case (as it is also found as the highest then)
        if high == 0:
            high_digit = low_digit
            
        calibration_value = int(str(low_digit) + str(high_digit))
        output += calibration_value
    return output

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")

# As I did not find the error in my code, I needed a positive control for error finding
# Found help from Reddit-User 4bHQ using this code (from https://www.reddit.com/r/adventofcode/comments/1883ibu/comment/kbigj6k/)

# r = '1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine'

# def f(line):
#     x = [*map({n: i%9+1 for i, n in enumerate(r.split('|'))}.get,
#         re.findall(rf'(?=({r}))', line))]
#     return 10*x[0] + x[-1]

# print(sum(map(f, open('Inputs/day1.txt'))))