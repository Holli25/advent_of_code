from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> List[str]:
    with open(path.join(data_folder, "day15.txt"), "r") as file:
        content = file.read().strip()
    return [s for s in content.split(",")]

def hash_algorithm(word:str) -> int:
    value = 0
    for letter in word:
        value += ord(letter)
        value *=17
        value = value %256
    return value

def get_lens_information(lens:str) -> Tuple[str, str, int]:
    if "-" in lens:
        return (lens[:-1], lens[-1], -1)
    else:
        return (lens[:-2], lens[-2], int(lens[-1]))


def part1() -> int:
    # Part 1 of the puzzle
    return sum([hash_algorithm(s) for s in get_input()])


def part2() -> int:
    # Part 2 of the puzzle
    boxes = {}
    focal_lengths = {}
    
    for lens in get_input():
        name, operator, focal_length = get_lens_information(lens)
        box = hash_algorithm(name)
        
        if operator == "=":
            if name in focal_lengths: # If the lens is already present, only update the focal length
                focal_lengths[name] = focal_length
            elif box in boxes: # If the box already exists, add the new lens at the back and save the focal_length
                boxes[box].append(name)
                focal_lengths[name] = focal_length
            else: # Otherwise create the box with only the current lens
                boxes[box] = [name]
                focal_lengths[name] = focal_length
        else:
            if box in boxes and name in boxes[box]:
                boxes[box].remove(name)
                del focal_lengths[name]
    
    output = sum([(box + 1) * (i + 1) * focal_lengths[lens] for box, lenses in boxes.items() for i, lens in enumerate(lenses)])
    return output

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")