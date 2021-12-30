from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> List[str]:
    if testing:
        filename = "Test_inputs/Day18.txt"
    else:
        filename = "Inputs/Day18.txt"

    with open(filename) as file:
        return [line.strip() for line in file]

class Sequence():
    def __init__(self, input_string: str):
        self.content = self.create_content(input_string)

    def create_content(self, input:str) -> List[Tuple[int, int]]:
        output = []
        index = 0
        for letter in input:
            if letter == "[":
                index += 1
            elif letter == "]":
                index -= 1
            elif letter == ",":
                pass
            else:
                output.append([int(letter), index])
        return output

    def should_explode(self) -> Tuple[bool, int]:
        for index, part in enumerate(self.content):
            if part[1] >= 5:
                return True, index
        return False, None

    def should_split(self) -> Tuple[bool, int]:
        for index, part in enumerate(self.content):
            if part[0] > 9:
                return True, index
        return False, None

    def explode(self, index) -> None:
        if index > 0:
            self.content[index - 1][0] += self.content[index][0]
        if index + 3 <= len(self.content):
            self.content[index + 2][0] += self.content[index + 1][0]
        self.content[index] = [0, self.content[index][1] - 1]
        self.content.pop(index + 1)

    def split(self, index) -> None:
        number_to_split, current_index = self.content[index]
        left_number = number_to_split // 2
        right_number = number_to_split - left_number

        self.content[index] = [left_number, current_index + 1]
        self.content.insert(index + 1, [right_number, current_index + 1])

    def reduce(self) -> None:
        can_explode, explode_index = self.should_explode()
        can_split, split_index = self.should_split()
        while can_explode or can_split:
            if can_explode:
                self.explode(explode_index)
            else:
                self.split(split_index)

            can_explode, explode_index = self.should_explode()
            can_split, split_index = self.should_split()

    def add_sequence(self, new_sequence: str) -> None:
        for position in self.content:
            position[1] += 1

        prepared_new_sequence = self.create_content(new_sequence)
        for position in prepared_new_sequence:
            position[1] += 1

        self.content += prepared_new_sequence
        self.reduce()

    def count(self) -> int:
        counting_content = self.content.copy()
        while len(counting_content) > 1:
            indices_for_deletion = []
            for index, element in enumerate(counting_content):
                if index in indices_for_deletion:
                    pass
                elif index + 1 < len(counting_content) and element[1] == counting_content[index + 1][1]:
                    # indices_for_deletion.append(index + 1)
                    counting_content[index] = [3 * element[0] + 2 * counting_content[index + 1][0], element[1] - 1]
                    counting_content.pop(index + 1)
                    break
            for i in indices_for_deletion[::-1]:
                counting_content.pop(i)
        return counting_content[0][0]

def part_one() -> int:
    input = read_data()
    sequence = Sequence(input[0])
    for addition in input[1:]:
        sequence.add_sequence(addition)
    return(sequence.count())

def part_two() -> int:
    input = read_data()
    highest_sum = 0
    for first_sequence in range(len(input)):
        for second_sequence in range(len(input)):
            if first_sequence == second_sequence:
                pass
            else:
                sequence = Sequence(input[first_sequence])
                sequence.add_sequence(input[second_sequence])
                sequence_count = sequence.count()
                if sequence_count > highest_sum:
                    highest_sum = sequence_count
    return highest_sum

print(part_one())
print(part_two())
