from typing import List

def read_data() -> List[List]:
    with open("Inputs/Day3.txt") as file:
        lines = file.readlines()
        input = [[int(string) for string in line.rstrip()] for line in lines]

    return input

def get_position_count(input: List[List], position: int) -> int:
    # Function that returns whether 1 or 0 is more often found at a specified position
    position_count = sum(list(map(lambda x: x[position], input)))
    return int(position_count >= len(input) / 2)

def get_lower_position_count(input: List[List], position: int) -> int:
    # Function that returns whether 1 or 0 is more often found at a specified position
    position_count = sum(list(map(lambda x: x[position], input)))
    return int(position_count < len(input) / 2)

def part_one() -> int:
    input = read_data()
    binary_length = len(input[0])

    gamma = [get_position_count(input, position) for position in range(binary_length)]
    gamma_string = "".join([str(i) for i in gamma])
    gamma_int = int(gamma_string, base = 2)

    # Binary can be inverted by using XOR with a binary of the same length full of 1s
    inverter = int("".join(["1" for i in range(binary_length)]), base = 2)
    epsilon_int = gamma_int ^ inverter

    print(gamma_int, epsilon_int)

    return(gamma_int * epsilon_int)

def filter_by_position(input: List[List], position: int, reverse: bool) -> List[List]:
    position_count = get_position_count(input, position)
    if reverse:
        position_count = get_lower_position_count(input, position)
    comparisons = list(map(lambda x: x[position] == position_count, input))
    input = [code for (code, b) in zip(input, comparisons) if b]
    return input

def get_letter_value(input: List[List], letter: str) -> int:
    if letter == "gamma":
        reverse = False
    elif letter == "epsilon":
        reverse = True

    binary_length = len(input[0])
    for position in range(binary_length):
        print(f"Doing position {position} for letter {letter}. Input is {len(input)} long")
        if len(input) == 1:
            return input[0]
        input = filter_by_position(input, position, reverse)

    if len(input) == 1:
        return input[0]
    else:
        return input

def convert_list_to_binary(letter_list: List[int]) -> int:
    print(letter_list)
    return int("".join([str(i) for i in letter_list]), base = 2)

def part_two() -> List[int]:
    input = read_data()

    gamma_list = get_letter_value(input, "gamma")
    gamma = convert_list_to_binary(gamma_list)

    epsilon_list = get_letter_value(input, "epsilon")
    epsilon = convert_list_to_binary(epsilon_list)

    return gamma*epsilon


print(part_one())
print(part_two())
