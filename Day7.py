from typing import List, Tuple, Dict

def read_data(testing: bool = False) -> List[int]:
    if testing:
        filename = "Test_inputs/Day7.txt"
    else:
        filename = "Inputs/Day7.txt"
    with open(filename) as file:
        inputs = file.readline()
        crab_positions = [int(crab_position) for crab_position in inputs.split(",")]
    return crab_positions

def get_median(crab_positions: List[int]) -> int:
    crab_positions.sort()
    return crab_positions[len(crab_positions)//2]

def calculate_fuel(crab_positions: List[int]) -> int:
    median: int = get_median(crab_positions)
    return sum([abs(position - median) for position in crab_positions])

def calculate_fuel_with_crab_logic(crab_positions: List[int], reference_position: int) ->int:
    output: int = 0
    for position in crab_positions:
        difference: int = abs(position - reference_position) + 1
        output += ((difference * (difference - 1)) / 2)
    return output

def get_smallest_fuel_consumption(crab_positions: List[int]) -> Tuple[int, int]:
    mean: int = get_mean(crab_positions)
    fuel_consumptions: Dict = dict()

    for possible_position in range(mean - 20, mean + 20):
        fuel_consumptions[possible_position] = calculate_fuel_with_crab_logic(crab_positions, possible_position)

    smallest_consumption_position: int = min(fuel_consumptions, key = fuel_consumptions.get)
    return smallest_consumption_position, fuel_consumptions[smallest_consumption_position]

def get_mean(crab_positions: List[int]) -> int:
    return sum(crab_positions)//len(crab_positions)

def part_one() -> int:
    crab_positions = read_data()
    return calculate_fuel(crab_positions)

def part_two() -> int:
    crab_positions = read_data(False)
    position, fuel = get_smallest_fuel_consumption(crab_positions)
    print(f"Found position {position} with {fuel} needed.")
    return fuel

print(part_one())
print(part_two())
