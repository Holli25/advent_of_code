from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> List[int]:
    if testing:
        filename = "Test_inputs/Day11.txt"
    else:
        filename = "Inputs/Day11.txt"

    with open(filename) as file:
        return [[Octopus(column, line_number, energy) for column, energy in enumerate(line.strip())] for line_number, line in enumerate(file)]

class Octopus:
    def __init__(self, x, y, energy):
        self.x: int = x
        self.y: int = y
        self.energy: int = int(energy)
        self.is_resting: bool = False
        self.is_flashing: bool = self._is_flashing()
        # self.last_flash: int = 0
        self.flash_times: int = 0

    def increase_energy(self):
        if not self.is_resting:
            self.energy += 1
            self.is_flashing = self._is_flashing()

    def flash(self):
        self.flash_times += 1
        self.is_resting = True
        self.is_flashing = False
        self.energy = 0

    def reset(self):
        self.is_flashing = False
        self.is_resting = False

    def _is_flashing(self):
        return self.energy > 9

class OctopusField:
    def __init__(self, octopi):
        self.octopi: List[List[Octopus]] = octopi
        self.round: int = 1
        self.flashing_octopi: int = 0

    def count_flashes(self) -> int:
        return sum([octopus.flash_times for row in self.octopi for octopus in row])

    def count_flashing_octopi(self) -> int:
        return sum([octopus.is_flashing for row in self.octopi for octopus in row])

    def flashes_are_synchronized(self):
        return sum([octopus.energy for row in self.octopi for octopus in row]) == 0

    def find_first_synchronized_flash(self) -> int:
        round:int = 0
        while not self.flashes_are_synchronized():
            self.one_round()
            round += 1
        return round

    def one_round(self) -> None:
        self.increase_energy_for_all_octopi()
        self.flashing_octopi = self.count_flashing_octopi()
        self.flash_octopi()
        self.reset()

    def play_multiple_rounds(self, times:int) -> None:
        for round in range(times):
            self.one_round()

    def increase_energy_for_all_octopi(self) -> None:
        for line in self.octopi:
            for o in line:
                o.increase_energy()

    def flash_octopi(self) -> None:
        while self.flashing_octopi > 0:
            for row in self.octopi:
                for octopus in row:
                    if octopus.is_flashing:
                        octopus.flash()
                        self.increase_energy_of_nearby_octopi(octopus.x, octopus.y)
            self.flashing_octopi = self.count_flashing_octopi()

    def increase_energy_of_nearby_octopi(self, x, y):
        # Set up x-range
        if x == 0:
            x_start = 0
            x_end = 1
        elif x == 9:
            x_start = 8
            x_end = 9
        else:
            x_start = x - 1
            x_end = x + 1

        # Set up y-range
        if y == 0:
            y_start = 0
            y_end = 1
        elif y == 9:
            y_start = 8
            y_end = 9
        else:
            y_start = y -1
            y_end = y + 1

        for column in range(x_start, x_end + 1):
            for row in range(y_start, y_end + 1):
                if x == column and y == row:
                    pass
                self.octopi[row][column].increase_energy()

    def reset(self):
        for row in self.octopi:
            for octopus in row:
                octopus.reset()

    def print_energy_board(self):
        for line in self.octopi:
            print([o.energy for o in line])

def part_one() -> int:
    inputs = read_data()
    field = OctopusField(inputs)
    field.play_multiple_rounds(100)
    return field.count_flashes()

def part_two() -> int:
    inputs = read_data(False)
    field = OctopusField(inputs)
    return field.find_first_synchronized_flash()

print(part_one())
print(part_two())
