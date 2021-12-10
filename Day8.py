from typing import List, Tuple, Dict

UNIQUE_LENGTHS = [2,3,4,7]

def read_data(testing: bool = False) -> Dict[str, str]:
        inputs: Dict[str, str] = dict()

        if testing:
            filename = "Test_inputs/Day8.txt"
        else:
            filename = "Inputs/Day8.txt"

        with open(filename) as file:
            for line in file:
                input_values, output_values = line.split(" | ")
                inputs[input_values] = output_values.rstrip()
        return inputs

def count_unique_numbers_in_string(input: str) -> int:
    input_split = input.split(" ")
    return sum([1 for i in input_split if len(i) in UNIQUE_LENGTHS])

def count_unique_numbers(input: Dict[str, str]) -> int:
    return sum([count_unique_numbers_in_string(line) for line in input.values()])

def decode(inputs: List[str]) -> List[str]:
    # Get 1, 4, 7 and 8 and sort the rest
    six_counts: List[str] = list()
    five_counts: List[str] = list()

    for number in inputs:
        if len(number) == 2:
            one = sort_number(number)
        elif len(number) == 3:
            seven = sort_number(number)
        elif len(number) == 4:
            four = sort_number(number)
        elif len(number) == 5:
            five_counts.append(sort_number(number))
        elif len(number) == 6:
            six_counts.append(sort_number(number))
        elif len(number) == 7:
            eight = sort_number(number)
        else:
            raise Exception("Number does not make sense!")

    # Sort the six-counts
    for number in six_counts:
        if len(list(set(number).intersection(four))) == 4:
            nine = number
        elif len(list(set(number).intersection(one))) == 2:
            zero = number
        elif len(list(set(number).intersection(one))) == 1:
            six = number
        else:
            raise Exception("Number from six-counts does not make sense!")

    # Sort the five-counts
    for number in five_counts:
        if len(list(set(number).intersection(one))) == 2:
            three = number
        elif len(list(set(number).intersection(four))) == 3:
            five = number
        elif len(list(set(number).intersection(four))) == 2:
            two = number
        else:
            raise Exception("Number from six-counts does not make sense!")

    return [zero, one, two, three, four, five, six, seven, eight, nine]

def sort_number(unsorted_number: str) -> str:
    return "".join(sorted([letter for letter in unsorted_number]))

def prepare_numbers(numbers: str) -> List[str]:
    return [sort_number(number) for number in numbers.split(" ")]

def get_output_value(input: str, output: str) -> int:
    decoded_input = decode(input)
    return int("".join([str(decoded_input.index(i)) for i in output]))

def part_one() -> int:
    inputs = read_data()
    return count_unique_numbers(inputs)

def part_two() -> int:
    inputs = read_data()
    out: int = 0
    for input, output in inputs.items():
        input = prepare_numbers(input)
        output = prepare_numbers(output)
        out += get_output_value(input, output)
    return out



print(part_one())
print(part_two())
