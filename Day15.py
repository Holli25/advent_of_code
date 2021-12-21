from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> int:
    if testing:
        filename = "Test_inputs/Day15.txt"
    else:
        filename = "Inputs/Day15.txt"

    with open(filename) as file:
        lines = file.readlines()
        row_length = len(lines[0].strip())
        return [int(i) for line in lines for i in line.strip()], row_length

class Maze():
    def __init__(self, input, row_size):
        self.risk_levels = input
        self.size = len(self.risk_levels)
        self.row_size = row_size
        self.used_tiles = [False for _ in self.risk_levels]

    def find_next_step(self, start_index):
        indices = self.get_indices(start_index)
        minimum = 10
        go_to_index = -1
        for index in indices:
            if index and not self.used_tiles[index] and self.risk_levels[index] < minimum:
                minimum = self.risk_levels[index]
                go_to_index = index
        self.used_tiles[go_to_index] = True
        # print(f"Went from {self.risk_levels[start_index]} at index {start_index} to {self.risk_levels[go_to_index]} at index {go_to_index}")

        return go_to_index

    def get_indices(self, start_index):
        if start_index > self.row_size:
            upper_index = start_index - self.row_size
        else:
            upper_index = None
        if start_index < self.size - self.row_size:
            lower_index = start_index + self.row_size
        else:
            lower_index = None
        if (start_index + 1)%10 == 0:
            right_index = None
        else:
            right_index = start_index + 1
        if start_index % 10 == 0:
            left_index = None
        else:
            left_index = start_index - 1
        return (upper_index, right_index, lower_index, left_index)

    def go_next(self):
        start = 0
        for _ in range(10):
            start = self.find_next_step(start)
            # print(start)

    def print_path(self):
        for row in range(int(self.size / self.row_size)):
            # print([row * self.row_size + col for col in range(self.row_size)])
            row_data = [self.used_tiles[row * self.row_size + col] for col in range(self.row_size)]
            print(row_data)

a, b = read_data(True)
m = Maze(a,b)
m.go_next()
m.print_path()
