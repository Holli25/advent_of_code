from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> List[int]:
    if testing:
        filename = "Test_inputs/Day11.txt"
    else:
        filename = "Inputs/Day11.txt"

    # octopi: List[List[Octopus]] = []
    # current_line: List[Octopus] = []
    with open(filename) as file:
        # for line_number, line in enumerate(file):
        #     for column, energy in enumerate(line.rstrip()):
        #         current_line.append(Octopus(column, line_number, energy))
        #     octopi.append(current_line)
        #     current_line = []

        return [[Octopus(column, line_number, energy) for column, energy in enumerate(line.strip())] for line_number, line in enumerate(file)]

class Octopus:
    def __init__(self, x, y, energy):
        self.x: int = x
        self.y: int = y
        self.energy: int = int(energy)
        self.flashing: bool = self._is_flashing()
        self.last_flash: int = 0
        self.flash_times: int = 0

    def increase_energy(self):
        if self.energy > 0:
            self.energy += 1
            self.flashing = self._is_flashing()

    def flash(self):
        self.flash_times += 1
        self.energy = -1
        self.flashing = self._is_flashing()

    def reset_energy(self):
        self.energy = 0

    def _is_flashing(self):
        return self.energy > 9

class OctopusField:
    def __init__(self, octopi):
        self.octopi: List[List[Octopus]] = octopi
        self.round: int = 1

    def one_round(self):
        self.increase_energy_for_all_octopi()
        self.flash_octopi()
        self.reset()

    def increase_energy_for_all_octopi(self):
        for line in self.octopi:
            for o in line:
                o.increase_energy()

    def flash_octopi(self):
        for row in self.octopi:
            for octopus in row:
                if octopus.flashing:
                    octopus.flash()
                    self.increase_energy_of_nearby_octopi(octopus.x, octopus.y)

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
                if octopus.energy == -1:
                    octopus.reset_energy()


    def print_energy_board(self):
        for line in self.octopi:
            print([o.energy for o in line])

a = read_data(True)
O = OctopusField(a)
O.print_energy_board()
print("\n")
O.one_round()
O.print_energy_board()
print("\n")
O.one_round()
O.print_energy_board()
