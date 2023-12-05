from os import path
import re
from typing import Dict, List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = False
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> Tuple[List[int], Dict[str, List[List[int]]]]:
    with open(path.join(data_folder, "day5.txt"), "r") as file:
        content = file.read()
    seed_line = re.search("seeds:[ \d]+", content).group(0)
    seeds = [int(seed.group(0)) for seed in re.finditer("\d+", seed_line)]

    seed_soil_line = re.search("seed-to-soil map:\n[\d+ \d+ \d+\n]+", content)
    seed_to_soil = [[int(i.group(0)) for i in re.finditer("\d+", line)] for line in seed_soil_line.group(0).splitlines() if line][1:] # if line get rids of empty list at the end, [1:] gets rid of empty List due to "seed-to-soil map:" at the start
    
    soil_fertilizer_line = re.search("soil-to-fertilizer map:\n[\d+ \d+ \d+\n]+", content)
    soil_to_fertilizer = [[int(i.group(0)) for i in re.finditer("\d+", line)] for line in soil_fertilizer_line.group(0).splitlines() if line][1:] # if line get rids of empty list at the end, [1:] gets rid of empty List due to "seed-to-soil map:" at the start
    
    fertilizer_water_line = re.search("fertilizer-to-water map:\n[\d+ \d+ \d+\n]+", content)
    fertilizer_to_water = [[int(i.group(0)) for i in re.finditer("\d+", line)] for line in fertilizer_water_line.group(0).splitlines() if line][1:] # if line get rids of empty list at the end, [1:] gets rid of empty List due to "seed-to-soil map:" at the start
    
    water_light_line = re.search("water-to-light map:\n[\d+ \d+ \d+\n]+", content)
    water_to_light = [[int(i.group(0)) for i in re.finditer("\d+", line)] for line in water_light_line.group(0).splitlines() if line][1:] # if line get rids of empty list at the end, [1:] gets rid of empty List due to "seed-to-soil map:" at the start
    
    light_temperature_line = re.search("light-to-temperature map:\n[\d+ \d+ \d+\n]+", content)
    light_to_temperature = [[int(i.group(0)) for i in re.finditer("\d+", line)] for line in light_temperature_line.group(0).splitlines() if line][1:] # if line get rids of empty list at the end, [1:] gets rid of empty List due to "seed-to-soil map:" at the start
    
    temperature_humidity_line = re.search("temperature-to-humidity map:\n[\d+ \d+ \d+\n]+", content)
    temperature_to_humidity = [[int(i.group(0)) for i in re.finditer("\d+", line)] for line in temperature_humidity_line.group(0).splitlines() if line][1:] # if line get rids of empty list at the end, [1:] gets rid of empty List due to "seed-to-soil map:" at the start
    
    humidity_location_line = re.search("humidity-to-location map:\n[\d+ \d+ \d+\n]+", content)
    humidity_to_location = [[int(i.group(0)) for i in re.finditer("\d+", line)] for line in humidity_location_line.group(0).splitlines() if line][1:] # if line get rids of empty list at the end, [1:] gets rid of empty List due to "seed-to-soil map:" at the start
    
    return (seeds, {"seed-to-soil":seed_to_soil, "soil-to-fertilizer":soil_to_fertilizer, "fertilizer-to-water":fertilizer_to_water, "water-to-light":water_to_light, "light-to-temperature":light_to_temperature, "temperature-to-humidity":temperature_to_humidity, "humidity-to-location":humidity_to_location})
    


def part1() -> int:
    # Part 1 of the puzzle
    seeds, maps = get_input()
    locations = []

    for seed in seeds:
        translation = seed
        for name, m in maps.items():
            for row in m:
                if translation >= row[1] and translation < row[1] + row[2]:
                    translation = row[0] + (translation - row[1])
                    # print(f"Seed: {seed} was translated in {name} in row {row} to {translation}")
                    break
            # print(f"Seed {seed} is: {translation}")
        locations.append(translation)
    return min(locations)

def part2() -> int:
    # Part 2 of the puzzle
    seeds, maps = get_input()
    print(sorted(maps.get("humidity-to-location")))
    

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")