from typing import List, Tuple, Dict


def read_data(testing: bool = False) -> Dict[int, List[int]]:
    if testing:
        filename = "Test_inputs/Day19.txt"
    else:
        filename = "Inputs/Day19.txt"

    with open(filename) as file:
        scanners: Dict[int:List[List[str]]] = {}
        beacons: List[str] = []
        for line in file:
            if line.strip().startswith("--"):
                scanner_number = int(line.split("scanner ")[1].split(" ")[0])
            elif not line.strip():
                scanners[scanner_number] = beacons
                beacons = []
            else:
                beacon_coordinates = [int(coordinate)
                                      for coordinate in line.strip().split(",")]
                beacons.append(beacon_coordinates)
        scanners[scanner_number] = beacons
        return scanners


class Scanner():
    def __init__(self, number, beacon_coordinates):
        self.number = number
        self.seen_beacons = beacon_coordinates
        self.distances = self.create_distance_dictionary("normal")
        self.sum_distances = self.create_distance_dictionary("sum")
        self.position = [0, 0, 0]

    def create_distance_dictionary(self, variant: str) -> Dict[str, int]:
        distances = {}
        for i in range(len(self.seen_beacons)):
            for j in range(i + 1, len(self.seen_beacons)):
                key = f"{i}-{j}"
                if variant == "normal":
                    distances[key] = self.calculate_distance(self.seen_beacons[i], self.seen_beacons[j])
                elif variant == "sum":
                    distances[key] = self.calculate_sum_distance(self.seen_beacons[i], self.seen_beacons[j])
        return distances

    def calculate_distance(self, beacon1, beacon2) -> List[int]:
        return [abs(beacon1[0] - beacon2[0]), abs(beacon1[1] - beacon2[1]), abs(beacon1[2] - beacon2[2])]

    def calculate_sum_distance(self, beacon1, beacon2) -> int:
        return ((beacon1[0] - beacon2[0])**2 + (beacon1[1] - beacon2[1])**2 + (beacon1[2] - beacon2[2])**2)

    def count_beacon_overlap_to_other_scanner(self, other_scanner: "Scanner") -> int:
        return sum([1 for beacon in self.sum_distances.values() if beacon in other_scanner.sum_distances.values()])

    def get_shared_beacon_numbers_with_other_scanner(self, other_scanner: "Scanner") -> List[int]:
        shared_beacons = [[beacon_combination, coordinates] for beacon_combination, coordinates in self.sum_distances.items() if coordinates in other_scanner.sum_distances.values()]
        return self.get_beacon_numbers_from_combinations(shared_beacons)

    def get_beacon_numbers_from_combinations(self, beacon_combinations: List[str]) -> List[int]:
        beacon_numbers: List[int] = []
        for beacon_combination in beacon_combinations:
            beacon1, beacon2 = beacon_combination[0].split("-")
            beacon_numbers.append(int(beacon1))
            beacon_numbers.append(int(beacon2))
        return list(set(beacon_numbers))

    def find_corresponding_beacons(self, other_scanner: "Scanner") -> Dict[int, int]:
        my_distance_list = self.generate_distance_list_for_beacons(other_scanner)
        other_distance_list = other_scanner.generate_distance_list_for_beacons(self)

        matching_beacons = {}
        for my_beacon, my_beacon_distances in my_distance_list.items():
            for other_beacon, other_beacon_distances in other_distance_list.items():
                if my_beacon_distances == other_beacon_distances:
                    matching_beacons[my_beacon] = other_beacon

        return matching_beacons

    def generate_distance_list_for_beacons(self, other_scanner: "Scanner") -> Dict[List[int], int]:
        matching_beacons = self.get_shared_beacon_numbers_with_other_scanner(other_scanner)
        beacons_with_distances = [[[int(beacon) for beacon in beacon_combination.split("-")], coordinates] for beacon_combination, coordinates in self.sum_distances.items() if coordinates in other_scanner.sum_distances.values()]
        distance_list = {}
        for beacon_number in matching_beacons:
            distances = [distance for measured_beacons, distance in beacons_with_distances if beacon_number in measured_beacons]
            distances.sort()
            distance_list[beacon_number] = distances
        return distance_list

    def print_matching_beacons(self, other_scanner: "Scanner") -> None:
        matching_beacons = self.find_corresponding_beacons(other_scanner)
        for beacon1, beacon2 in matching_beacons.items():
            print(f"{self.seen_beacons[beacon1]} corresponds to {other_scanner.seen_beacons[beacon2]}")

    def find_relative_scanner_position(self, other_scanner):
        corresponding_beacons = self.find_corresponding_beacons(other_scanner)
        changes = [self.get_polarity(other_scanner, corresponding_beacons, pol) for pol in range(3)]
        return changes

    def get_polarity(self, other_scanner, corresponding_beacons, axis):
        for index, beacon_number in enumerate(corresponding_beacons.keys()):
            if index == 0:
                beacon_1_1 = self.seen_beacons[beacon_number][axis]
                beacon_2_1 = other_scanner.seen_beacons[corresponding_beacons[beacon_number]][axis]
            elif index == 1:
                beacon_1_2 = self.seen_beacons[beacon_number][axis]
                beacon_2_2 = other_scanner.seen_beacons[corresponding_beacons[beacon_number]][axis]

        polarity = (beacon_1_1 > 0 and beacon_2_1 > 0) or (beacon_1_1 < 0 and beacon_2_1 < 0)
        same_direction = (abs(beacon_1_1) > abs(beacon_1_2) and abs(beacon_2_1) > abs(beacon_2_2)) or (abs(beacon_1_1) < abs(beacon_1_2) and abs(beacon_2_1) < abs(beacon_2_2))
        if same_direction:
            return [beacon_1_1 + beacon_2_1, int(polarity)]
        return [beacon_1_1 - beacon_2_1, -1]

    def readjust_beacon_coordinates(self, changes):
        new_beacons = []
        for beacon_coordinates in self.seen_beacons:
            new_coordinates = []
            for axis, change in enumerate(changes):
                amount, polarity = change
                if polarity == 1:
                    new_coord = beacon_coordinates[axis] - amount
                elif polarity == 0:
                    new_coord = beacon_coordinates[axis] - 2 * beacon_coordinates[axis] + amount
                else:
                    new_coord = beacon_coordinates[axis] + amount
                new_coordinates.append(new_coord)
            new_beacons.append(new_coordinates)
        self.seen_beacons = new_beacons

    def sort_beacon_coordinates_to_other_scanner(self, other_scanner):
        corresponding_beacons = self.find_corresponding_beacons(other_scanner)
        for index, beacon_number in enumerate(corresponding_beacons.keys()):
            if index == 0:
                beacon_1_1 = self.seen_beacons[beacon_number]
                beacon_2_1 = other_scanner.seen_beacons[corresponding_beacons[beacon_number]]
            elif index == 1:
                beacon_1_2 = self.seen_beacons[beacon_number]
                beacon_2_2 = other_scanner.seen_beacons[corresponding_beacons[beacon_number]]

        x_difference = (beacon_1_1[0] - beacon_1_2[0]) ** 2
        y_difference = (beacon_1_1[1] - beacon_1_2[1]) ** 2
        z_difference = (beacon_1_1[2] - beacon_1_2[2]) ** 2

        original_x = (beacon_2_1[0] - beacon_2_2[0]) ** 2
        original_y = (beacon_2_1[1] - beacon_2_2[1]) ** 2
        original_z = (beacon_2_1[2] - beacon_2_2[2]) ** 2

        for index, new_coordinate in enumerate([original_x, original_y, original_z]):
            if new_coordinate == x_difference:
                x = index
            elif new_coordinate == y_difference:
                y = index
            elif new_coordinate == z_difference:
                z = index
            else:
                print("Something went horribly wrong...")

        new_beacons = [[beacon[x], beacon[y], beacon[z]] for beacon in self.seen_beacons]
        self.seen_beacons = new_beacons


a = read_data(True)
scanners = [Scanner(numbers, beacons) for numbers, beacons in a.items()]
b = scanners[0]
c = scanners[1]
d = scanners[4]
# b.get_shared_beacon_numbers_with_other_scanner(c)
c_changes = b.find_relative_scanner_position(c)
c.readjust_beacon_coordinates(c_changes)
d.sort_beacon_coordinates_to_other_scanner(c)
d_changes = c.find_relative_scanner_position(d)

c.print_matching_beacons(d)
print()
print(d_changes)



# for i1, scanner in enumerate(scanners):
#     for i2, other_scanner in enumerate(scanners):
#         if scanner.number == 1 and other_scanner.number == 4:
#             for beacon_number in scanner.get_shared_beacon_numbers_with_other_scanner(other_scanner):
#                 print(scanner.seen_beacons[beacon_number])
        # if scanner != other_scanner and len(scanner.get_shared_beacon_numbers_with_other_scanner(other_scanner)) >= 12:
        #     print(f"Overlap from {scanner.number} to {other_scanner.number} is: {len(scanner.get_shared_beacon_numbers_with_other_scanner(other_scanner))}")

# 423,-701,434
# -355,545,-477
#
# declare other scanners coords as x, y and z
# find polarity difference
