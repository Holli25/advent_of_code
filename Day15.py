from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> Tuple[List[int], int]:
    if testing:
        filename = "Test_inputs/Day15.txt"
    else:
        filename = "Inputs/Day15.txt"

    with open(filename) as file:
        lines = file.readlines()
        row_length = len(lines[0].strip())
        return [int(i) for line in lines for i in line.strip()], row_length

class MazeAStar():
    def __init__(self, risk_levels: List[int], row_size: int, part_two: bool = False):
        self.risk_levels: List[int] = risk_levels
        self.row_size: int = row_size
        self.rows: int = int(len(self.risk_levels) / row_size)
        self.size: int = len(self.risk_levels)
        self.openlist: Dict[int, int] = {0:0}
        self.closedlist: Dict[int, int] = {}

        if part_two:
            self.expand_risk_levels()
            self.row_size *= 5
            self.rows = int(len(self.risk_levels) / self.row_size)
            self.size: int = len(self.risk_levels)

    def expand_risk_levels(self):
        basic_field = [[self.risk_levels[j * self.row_size + i] for i in range(self.row_size)] for j in range(self.rows)]
        r2 = self.expand_one_iteration(basic_field)
        r3 = self.expand_one_iteration(r2)
        r4 = self.expand_one_iteration(r3)
        r5 = self.expand_one_iteration(r4)
        r6 = self.expand_one_iteration(r5)
        r7 = self.expand_one_iteration(r6)
        r8 = self.expand_one_iteration(r7)
        r9 = self.expand_one_iteration(r8)
        new_row1 = [a+b+c+d+e for a,b,c,d,e in zip(basic_field, r2, r3, r4, r5)]
        new_row2 = [a+b+c+d+e for a,b,c,d,e in zip(r2, r3, r4, r5, r6)]
        new_row3 = [a+b+c+d+e for a,b,c,d,e in zip(r3, r4, r5, r6, r7)]
        new_row4 = [a+b+c+d+e for a,b,c,d,e in zip(r4, r5, r6, r7, r8)]
        new_row5 = [a+b+c+d+e for a,b,c,d,e in zip(r5, r6, r7, r8, r9)]
        final = new_row1 + new_row2 + new_row3 + new_row4 + new_row5
        self.risk_levels = [i for row in final for i in row]

    def expand_one_iteration(self, field):
        return [[i + 1 if i < 9 else 1 for i in row] for row in field]

    def find_shortest_path(self):
        while True:
            current = self.get_index_of_smallest_value_of_openlist()
            current_value = self.openlist[current]
            self.openlist.pop(current, None)

            if current == len(self.risk_levels) - 1:
                print("Found it!!")
                return current_value
            self.closedlist[current] = current_value
            self.expand_node(current, current_value)
            if not self.openlist:
                print("Did not work!!")
                self.print_path()

    def get_index_of_smallest_value_of_openlist(self) -> int:
        return min(self.openlist, key = self.openlist.get)

    def expand_node(self, current_node: int, current_value: int):
        # print(self.openlist)
        for connected_node in self.get_indices(current_node):
            if not connected_node or connected_node in self.closedlist:
                continue
            new_value = current_value + self.risk_levels[connected_node]
            if connected_node in self.openlist.keys() and new_value >= self.openlist[connected_node]:
                continue
            self.openlist[connected_node] = new_value


    def get_indices(self, start_index):
        if start_index > self.row_size:
            upper_index = start_index - self.row_size
        else:
            upper_index = None
        if start_index < self.size - self.row_size:
            lower_index = start_index + self.row_size
        else:
            lower_index = None
        if (start_index + 1)%self.row_size == 0:
            right_index = None
        else:
            right_index = start_index + 1
        if start_index % self.row_size == 0:
            left_index = None
        else:
            left_index = start_index - 1
        return (upper_index, right_index, lower_index, left_index)

    def print_path(self):
        for row in range(self.rows):
            # print([row * self.row_size + col for col in range(self.row_size)])
            row_data = ["O" if (row * self.row_size + col) in self.closedlist.keys() else "." for col in range(self.row_size)]
            print(row_data)

def part_one() -> int:
    risk_levels, row_size = read_data()
    maze = MazeAStar(risk_levels, row_size)
    return(maze.find_shortest_path())

def part_two() -> int:
    risk_levels, row_size = read_data()
    maze = MazeAStar(risk_levels, row_size, True)
    return(maze.find_shortest_path())

print(part_one())
print(part_two())
