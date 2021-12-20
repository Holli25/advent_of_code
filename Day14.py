from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> int:
    if testing:
        filename = "Test_inputs/Day14.txt"
    else:
        filename = "Inputs/Day14.txt"

    polymer: List[str] = []
    instructions: Dict[str, str] = {}

    with open(filename) as file:
        polymer = [element for element in file.readline().rstrip()]
        file.readline() # read empty line between polymer
        for line in file:
            combination, new_element = line.rstrip().split(" -> ")
            instructions[combination] = new_element

    return polymer, instructions

class Polymer():
    def __init__(self, starting_polymer, instructions):
        self._sequence = starting_polymer
        self._length = len(self._sequence)
        self.instructions = instructions
        self.elements = self.get_elements_from_polymer()

    def get_elements_from_polymer(self):
        return set(self._sequence)

    def _update_length(self):
        self._length = len(self._sequence)

    @property
    def sequence(self):
        return self._sequence

    @property
    def length(self):
        return self._length

    def get_new_element_from_instructions(self, element1: str, element2: str) -> str:
        return self.instructions["".join([element1, element2])]

    def elongate_polymer(self) -> None:
        new_polymer_sequence: List[str] = []
        for element1, element2 in zip(self._sequence[:-1], self._sequence[1:]):
            new_polymer_sequence.append(element1)
            new_element:str = self.get_new_element_from_instructions(element1, element2)
            new_polymer_sequence.append(new_element)
        new_polymer_sequence.append(self._sequence[-1])
        self._sequence = new_polymer_sequence
        self._update_length()



    def get_result(self) -> int:
        self.elements = self.get_elements_from_polymer()
        results = {self._sequence.count(element):element for element in self.elements}
        return max(results) - min(results)

class DictPolymer():
    def __init__(self, starting_polymer, instructions: Dict[str, str]):
        self.sequence: Dict[str, int] = {}
        self.fill_sequence(starting_polymer)
        self.instructions: Dict[str, str] = instructions

    def fill_sequence(self, starting_sequence) -> None:
        for element1, element2 in zip(starting_sequence[:-1], starting_sequence[1:]):
            combined = f"{element1}{element2}"
            if combined in self.sequence:
                self.sequence[combined] += 1
            else:
                self.sequence[combined] = 1

    def update_sequence(self) -> None:
        new_sequence = {}
        for combination, amount in self.sequence.items():
            new_element = self.instructions[combination]
            new1 = f"{combination[0]}{new_element}"
            new2 = f"{new_element}{combination[1]}"
            if new1 in new_sequence:
                new_sequence[new1] += amount
            else:
                new_sequence[new1] = amount
            if new2 in new_sequence:
                new_sequence[new2] += amount
            else:
                new_sequence[new2] = amount
        self.sequence = new_sequence

    def get_result(self) -> int:
        output = {}
        for combination, amount in self.sequence.items():
            for element in combination:
                if element in output:
                    output[element] += amount
                else:
                    output[element] = amount
        for element, amount in output.items():
            if amount % 2 == 0:
                output[element] = int(amount / 2)
            else:
                output[element] = int(amount / 2 + 0.5)

        return max(output.values()) - min(output.values())


def part_one() -> int:
    polymer_sequence, instructions = read_data()
    polymer = Polymer(polymer_sequence, instructions)
    for n in range(10):
        polymer.elongate_polymer()
    return polymer.get_result()

def part_two() -> int:
    polymer_sequence, instructions = read_data()
    polymer = DictPolymer(polymer_sequence, instructions)
    for n in range(40):
        print(f"Starting run {n}")
        polymer.update_sequence()
    return polymer.get_result()

# print(part_one())
print(part_two())
