from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> int:
    if testing:
        filename = "Test_inputs/Day12.txt"
    else:
        filename = "Inputs/Day12.txt"

    with open(filename) as file:
        return [line.rstrip().split("-") for line in file]

class Cave():
    def __init__(self, name:str):
        self.connections = []
        self._name: str = name
        self._is_small: bool = self._get_size_status(self.name)
        self._is_dead_end: bool = self._check_dead_end()

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_small(self) -> bool:
        return self._is_small

    @property
    def is_dead_end(self) -> bool:
        return self._is_dead_end

    def _get_size_status(self, name:str) -> bool:
        return self._name.islower()

    def _check_dead_end(self) -> bool:
        return self._is_small and len(self.connections) == 1

    def add_connection(self, cave) -> None:
        self.connections.append(cave)

    def prune_connections(self) -> None:
        connections_to_prune = []
        for connected_cave in self.connections:
            if self.is_small and connected_cave.is_small and len(connected_cave.connections) == 1:
                connections_to_prune.append(connected_cave)
        for cave in connections_to_prune:
            self.connections.remove(cave)

class CaveSytem():
    def __init__(self, input: List[List[str]], part: int):
        self.caves: Dict[str, Cave] = self.create_caves(input)
        self.path_list: List[List[str]] = []

        if part == 1:
            for cave in self.caves.values():
                cave.prune_connections()
            self.elongate_path_one([], self.caves["start"])
        elif part == 2:
            self.elongate_path_two([], self.caves["start"])

        self.path_count: int = self.count_paths()

    def create_caves(self, input: List[List[str]]) -> Dict[str, Cave]:
        caves: Dict[str, Cave] = {}
        for pair in input:
            start, end = pair
            if not start in caves:
                caves[start] = Cave(start)
            if not end in caves:
                caves[end] = Cave(end)

            caves[start].add_connection(caves[end])
            caves[end].add_connection(caves[start])
        return caves

    def elongate_path_one(self, previous_path: List[str], current_cave: Cave) -> None:
        previous_path.append(current_cave.name)

        if current_cave.name == "end":
            self.path_list.append(previous_path)
        else:
            for cave in current_cave.connections:
                if cave.is_small and cave.name not in previous_path or not cave.is_small:
                    new = previous_path.copy()
                    self.elongate_path_one(new, cave)

    def elongate_path_two(self, previous_path: List[str], current_cave: Cave) -> None:
        previous_path.append(current_cave.name)

        if current_cave.name == "end":
            self.path_list.append(previous_path)
        else:
            for cave in current_cave.connections:
                if (cave.is_small and previous_path.count(cave.name) < 2 or not cave.is_small) and cave.name != "start":
                    if self.check_path_validity(previous_path):
                        new = previous_path.copy()
                        self.elongate_path_two(new, cave)

    def check_path_validity(self, path: List[str]) -> bool:
        small_caves_visited_twice: int = 0
        for cave in set(path):
            if path.count(cave) > 1 and cave.islower():
                small_caves_visited_twice += 1
        return small_caves_visited_twice <= 1

    def count_paths(self) -> int:
        return len(self.path_list)

def part_one() -> int:
    input = read_data()
    cave_system = CaveSytem(input, 1)
    return cave_system.path_count

def part_two() -> int:
    input = read_data()
    cave_system = CaveSytem(input, 2)
    return cave_system.path_count

print(part_one())
print(part_two())
