from os import path
import re
import math
from typing import Dict, List, Tuple
from copy import deepcopy

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day19.txt"), "r") as file:
        content = file.read()
    w = dict()
    p = list()
    workflows, parts = content.split("\n\n")

    for workflow in workflows.splitlines():
        name, rest = workflow.split("{")
        test_cases = rest[:-1].split(",")
        tests = []
        final:str = None

        for i, test in enumerate(test_cases):
            if i < len(test_cases) - 1:
                t = re.match("(\w+)([<>])(\d+):(\w+)", test)
                tests.append((t[1], t[2], int(t[3]), t[4]))
            else:
                final = test
        
        w[name] = (tests, final)

    for part in parts.splitlines():
        m = re.match("{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", part)
        p.append({"x":int(m[1]), "m":int(m[2]), "a":int(m[3]), "s":int(m[4])})
    return w, p

def part1() -> int:
    # Part 1 of the puzzle
    workflows, parts = get_input()
    A = []
    R = []

    for part in parts:
        todo = "in"

        while not todo in "AR":
            workflow, final = workflows.get(todo)
            todo = ""
            for category, comparator, amount, new_workflow in workflow:
                if comparator == ">":
                    if part.get(category) > amount:
                        todo = new_workflow
                        break
                else:
                    if part.get(category) < amount:
                        todo = new_workflow
                        break

            if not todo:
                todo = final
            # print(f"Next step for {part} is {todo}")
        
        if todo == "A":
            A.append(part)
        else:
            R.append(part)

    return sum([i for part in A for i in part.values()])

def find_possible_combination(workflows:Dict[str, Tuple[List[str], str]], part:Dict[str, Dict[str, int]], workflow:str):
    output = 0
    w, final = workflows.get(workflow)

    for category, comparator, amount, new_workflow in w:
        if comparator == "<":
            new_part = deepcopy(part) # deepcopy needed so I can modify the new part and do the opposite the the current part
            new_part[category]["upper"] = amount - 1
            if new_workflow == "A":
                # print(f"Found working combination in {workflow}: {new_part}")
                output += math.prod([cat.get("upper") - cat.get("lower") for cat in new_part.values()])
            # Catch the rejected cases, just do nothing to the output; pass instead of continue as we still want to modify the original part
            elif new_workflow == "R":
                pass
            else:
                output += find_possible_combination(workflows, new_part, new_workflow)
            part[category]["lower"] = amount - 1
        else:
            new_part = deepcopy(part)
            new_part[category]["lower"] = amount
            if new_workflow == "A":
                # print(f"Found working combination in {workflow}: {new_part}")
                output += math.prod([cat.get("upper") - cat.get("lower") for cat in new_part.values()])
            # Catch the rejected cases, just do nothing to the output; pass instead of continue as we still want to modify the original part
            elif new_workflow == "R":
                pass
            # If it is a new workflow, calculate the output for that worklow and add it to the current one
            else:
                output += find_possible_combination(workflows, new_part, new_workflow)
            # Do the opposite that was done to the new part to the original part, as these are the remaining boundaries
            part[category]["upper"] = amount

    if final == "A":
        # print(f"Found working combination in {workflow}: {part}")
        return output + math.prod([cat.get("upper") - cat.get("lower") for cat in part.values()])
    elif final == "R":
        return output
    else:
        return output + find_possible_combination(workflows, part, final)

def part2() -> int:
    # Part 2 of the puzzle
    workflows, parts = get_input()

    part = {"x":{"lower":0, "upper":4000}, "m":{"lower":0, "upper":4000}, "a":{"lower":0, "upper":4000}, "s":{"lower":0, "upper":4000}}
    return find_possible_combination(workflows, part, "in")

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")