from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> int:
    if testing:
        filename = "Test_inputs/Day13.txt"
    else:
        filename = "Inputs/Day13.txt"

    coordinates: List[List[int]] = []
    instructions: List[List[int]] = []
    with open(filename) as file:
        for line in file:
            if not line.startswith("fold") and len(line) > 1:
                coordinates.append([int(i) for i in line.rstrip().split(",")])
            elif len(line) > 1:
                instructions.append(decrypt_folding_instructions(line))

    return coordinates, instructions

def decrypt_folding_instructions(line: str) -> List[int]:
    if "x" in line:
        return [0, int(line.rstrip().split("=")[1])]
    elif "y" in line:
        return [1, int(line.rstrip().split("=")[1])]
    else:
        return None

class Paper():
    def __init__(self, starting_coordinates, instructions):
        self.coordinates: List[List[int]] = starting_coordinates
        self.instructions: List[List[int]] = instructions
        self.width, self.height = self.get_size_of_paper(self.coordinates)

    def fold(self, point_list: List[List[int]], direction: int, fold_position: int) -> List[List[int]]:
        new: List[List[int]] = []
        if direction == 1:
            for point in point_list:
                if point[1] > fold_position:
                    x = point[0]
                    new_y = point[1] - (2 * (point[1] - fold_position))
                    new.append([x, new_y])
                elif point[1] == fold_position:
                    pass
                else:
                    new.append(point)
        elif direction == 0:
            for point in point_list:
                if point[0] > fold_position:
                    y = point[1]
                    new_x = point[0] - (2 * (point[0] - fold_position))
                    new.append([new_x, y])
                elif point[0] == fold_position:
                    pass
                else:
                    new.append(point)
        return new

    def get_size_of_paper(self, paper: List[List[int]]) -> Tuple[int, int]:
        x = max(paper, key = lambda x: x[0])[0]
        y = max(paper, key = lambda y: y[1])[1]
        return x, y

    def count_points(self) -> int:
        unique_coordinates = []
        for coordinate in self.coordinates:
            if coordinate not in unique_coordinates:
                unique_coordinates.append(coordinate)
        return len(unique_coordinates)

    def fold_once(self) -> None:
        direction, fold_position = self.instructions[0]
        self.coordinates = self.fold(self.coordinates, direction, fold_position)

    def fold_all(self) -> None:
        for direction, fold_position in self.instructions:
            self.coordinates = self.fold(self.coordinates, direction, fold_position)

    def print_list_view(self) -> None:
        x, y = self.get_size_of_paper(self.coordinates)
        for row in range(y + 1):
            row_content = []
            for column in range(x + 1):
                if [column, row] in self.coordinates:
                    row_content.append("#")
                else:
                    row_content.append(".")
            print("".join(row_content))

def part_one() -> int:
    coordinates, instructions = read_data()
    folding_paper = Paper(coordinates, instructions)
    folding_paper.fold_once()
    return folding_paper.count_points()

def part_two():
    coordinates, instructions = read_data()
    folding_paper = Paper(coordinates, instructions)
    folding_paper.fold_all()
    folding_paper.print_list_view()

print(part_one())
part_two()
