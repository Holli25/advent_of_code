from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> int:
    if testing:
        filename = "Test_inputs/Day12.txt"
    else:
        filename = "Inputs/Day12.txt"
    with open(filename) as file:
        for line in file:
            start, end = line.rstrip().split("-")

class Cave():
    def __init__(self):
        self.connections = []

    def add_connection(self, cave: Cave):
        self.connections.append(cave)

class smallCave(Cave):
    def __init__(self):
        pass

class bigCave(Cave):
    def __init__(self):
        pass
