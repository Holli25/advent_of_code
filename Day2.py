from typing import List

def part_one():
    commands = read_data()
    horizontal = 0
    depth = 0

    for command in commands:
        direction, amount = command
        if direction == "forward":
            horizontal += amount
        elif direction == "up":
            depth -= amount
        elif direction == "down":
            depth += amount

    print(f"We are at {horizontal} with depth {depth} and the distance is {horizontal * depth}")

def part_two():
    commands = read_data()
    horizontal = 0
    depth = 0
    aim = 0

    for command in commands:
        direction, amount = command
        if direction == "forward":
            horizontal += amount
            depth += aim * amount
        elif direction == "up":
            aim -= amount
        elif direction == "down":
            aim += amount

    print(f"We are at {horizontal} with depth {depth} and the distance is {horizontal * depth}")

def read_data() -> List[List]:
    commands = []
    with open("Inputs/Day2.txt") as file:
        for line in file:
            prepared_line = line.rstrip().split(" ")
            commands.append([prepared_line[0], int(prepared_line[1])])
    return commands

part_one()
part_two()
