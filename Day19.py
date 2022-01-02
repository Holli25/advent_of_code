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
        self.distances = self.create_distance_dictionary()

    def create_distance_dictionary(self) -> Dict[str, int]:
        distances = {}
        for i in range(len(self.seen_beacons)):
            for j in range(i + 1, len(self.seen_beacons)):
                key = f"{i}-{j}"
                distances[key] = self.calculate_distance(self.seen_beacons[i], self.seen_beacons[j])
        return distances

    def calculate_distance(self, beacon1, beacon2):
        return [abs(beacon1[0] - beacon2[0]), abs(beacon1[1] - beacon2[1]), abs(beacon1[2] - beacon2[2])]

    def count_beacon_overlap_to_other_scanner(self, other_scanner: "Scanner") -> int:
        return sum([1 for beacon in self.distances.values() if beacon in other_scanner.distances.values()])

    def get_shared_beacon_numbers_with_other_scanner(self, other_scanner: "Scanner") -> List[int]:
        shared_beacons = [beacon_combination for beacon_combination, coordinates in self.distances.items() if coordinates in other_scanner.distances.values()]
        return self.get_beacon_numbers_from_combinations(shared_beacons)

    def get_beacon_numbers_from_combinations(self, beacon_combinations: List[str]) -> List[int]:
        beacon_numbers: List[int] = []
        for beacon_combination in beacon_combinations:
            beacon1, beacon2 = beacon_combination.split("-")
            beacon_numbers.append(int(beacon1))
            beacon_numbers.append(int(beacon2))
        return list(set(beacon_numbers))

a = read_data()
scanners = [Scanner(numbers, beacons) for numbers, beacons in a.items()]
for i1, scanner in enumerate(scanners):
    for i2, other_scanner in enumerate(scanners):
        if scanner != other_scanner and scanner.count_beacon_overlap_to_other_scanner(other_scanner) == 66:
            print(f"Overlap from {scanner.number} to {other_scanner.number} is: {scanner.count_beacon_overlap_to_other_scanner(other_scanner)}")
