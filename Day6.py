from typing import List, Tuple

def read_data(testing: bool = False) -> List[int]:
    if testing:
        inputfile_name = "Test_inputs/Day6.txt"
    else:
        inputfile_name = "Inputs/Day6.txt"
    with open(inputfile_name) as file:
        inputs = file.readline()
        fish_counters = [int(fish_counter) for fish_counter in inputs.split(",")]
    return fish_counters


def advance_one_generation(old_generation: List[int]) -> List[int]:
    next_generation = []
    new_fish = 0
    for fish_timer in old_generation:
        if fish_timer == 0:
            new_fish += 1
            next_generation.append(6)
        else:
            next_generation.append(fish_timer - 1)
    for i in range(new_fish):
        next_generation.append(8)
    return next_generation

def spawning(remaining_time: int, called: int, spawn_time: int = 8) -> int:
    out = 1
    print(f"I was in iteration {called}, start with {spawn_time} and {remaining_time} rounds remaining")
    for remain_time in range(remaining_time - spawn_time, 0, -6):
        print(f"Spawning new fish with {remain_time} rounds remaining")
        out += spawning(remain_time, called+1)
        print(f"Generation {called} with output {out}")
    return out
    # return 1 + sum([spawning(remain_time) for remain_time in range(remaining_time - spawn_time, 0, -6)])

def part_one():
    current_generation = read_data()
    print(f"Intitial stage: {current_generation}")
    for i in range(80):
        current_generation = advance_one_generation(current_generation)
        print(f"After {i + 1} days: {current_generation}")
    return len(current_generation)

def part_two():
    current_generation = read_data()
    print(f"Intitial stage: {current_generation}")
    out = 0
    for fish in current_generation:
        print(f"Starting with count of {fish}.")
        a = spawning(80, fish)
        out += a
        print(f"Got {a} fish for this one.")
    # for i in range(256):
    #     current_generation = advance_one_generation(current_generation)
    #     print(f"After {i + 1} days")
    return out #len(current_generation)

# print(part_one())
# print(part_two())
print(spawning(36, 1, 1))
