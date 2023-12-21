from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day20.txt"), "r") as file:
        content = file.readlines()

    modules = dict()
    conjunctions = list()
    all_receivers = list()
    for module in content:
        receivers = [receiver for receiver in module.strip().split("-> ")[1].split(", ")]
        all_receivers.append(receivers)
        module_name = module.split(" ")[0]
        if module_name == "broadcaster":
            modules[module_name] = Broadcaster(receivers)
        elif module_name.startswith("%"):
            modules[module_name[1:]] = FlipFlop(receivers)
        elif module_name.startswith("&"):
            conjunctions.append((module_name[1:], receivers))

    for conjunction, receivers in conjunctions:
        input_modules = list()
        for module in content:
            if conjunction in module.strip().split("-> ")[1]:
                input_modules.append(module.split(" ")[0][1:])
        modules[conjunction] = Conjunction(receivers, input_modules)
    
    all_receivers = set([receiver for l in all_receivers for receiver in l])
    for receiver in all_receivers:
        if receiver not in modules:
            modules[receiver] = Module(None)

    return modules


class Module():
    def __init__(self, receivers:List[str]):
        self.status = False
        self.receivers = receivers

    def receive_pulse(self, pulse:int, input_module:str) -> None:
        return None

    def send_pulse(self, pulse:int):
        return [(receiver, pulse) for receiver in self.receivers]

class FlipFlop(Module):
    def __init__(self, receivers:List[str]):
        super().__init__(receivers)
        self.status = False
    
    def receive_pulse(self, pulse:int, input_module:str) -> None:
        # Input_module does not matter here, only there so function signatures are the same
        # Low pulse changes state
        if pulse == -1:
            self.status = not self.status
            # On state sends a high pulse, off state sends a low pulse
            if self.status:
                return self.send_pulse(0)
            else:
                return self.send_pulse(-1)
        # High pulse does nothing
        return None

class Conjunction(Module):
    def __init__(self, receivers:List[str], input_modules:List[str]):
        super().__init__(receivers)
        self.last_pulses = {input_module:-1 for input_module in input_modules}

    def receive_pulse(self, pulse:int, input_module:str):
        self.last_pulses[input_module] = pulse
        # If all previous pulses are high, send a low pulse
        if sum([pulse for pulse in self.last_pulses.values()]) == 0:
            return self.send_pulse(-1)
        # Otherwise send high pulse
        return self.send_pulse(0)
    
class Broadcaster(Module):
    def __init__(self, receivers:List[str]):
        super().__init__(receivers)

    def receive_pulse(self, pulse:int, input_module:str):
        return self.send_pulse(pulse)

def push_button(modules):
    todo = [("broadcaster", -1, "button")]
    lows, highs = 1,0

    while todo:
        module, pulse, sender = todo.pop(0)
        # print(f"{sender} - {'low' if pulse == -1 else 'high'} -> {module}")
        if next_signals := modules.get(module).receive_pulse(pulse, sender):
            for receiver, next_pulse in next_signals:
                todo.append((receiver, next_pulse, module))
                if next_pulse == -1:
                    lows += 1
                else:
                    highs += 1
        # print(todo)
    return modules, (lows, highs)

def push_button_part2(modules):
    todo = [("broadcaster", -1, "button")]

    while todo:
        rx_lows = 0
        module, pulse, sender = todo.pop(0)
        if next_signals := modules.get(module).receive_pulse(pulse, sender):
            for receiver, next_pulse in next_signals:
                if receiver == "rx" and next_pulse == -1:
                    rx_lows += 1
                todo.append((receiver, next_pulse, module))
    # print(rx_lows)
    if rx_lows == 1:
        return modules, True
    return modules, False

def part1() -> int:
    # Part 1 of the puzzle
    modules = get_input()
    lows, highs = 0,0
    
    for i in range(1000):
        if i % 100 == 0:
            print("New cycle")
        modules, presses = push_button(modules)
        emitted_lows, emitted_highs = presses
        lows += emitted_lows
        highs += emitted_highs

    return lows * highs
    
def get_module_state(modules):
    output = []
    for module in modules.values():
        if type(module) == type(Conjunction([], [])):
            output.append(",".join([str(i) for i in module.last_pulses.values()]))
        else:
            continue
    return " | ".join([j for j in output]) + "\n"

def part2() -> int:
    # Part 2 of the puzzle
    modules = get_input()
    presses = 0
    base = [i for i in modules.get('cs').last_pulses.values()]

    for presses in range(2000000):
        if presses %1000 == 0:
            print(presses)
            # print([i for i in modules.get('jh').last_pulses.values()])
        modules, found = push_button_part2(modules)
        if found:
            break
        if [i for i in modules.get('cs').last_pulses.values()] == base:
            return presses
        # open("log20.txt", "a").write(get_module_state(modules))
        # open("log20.txt", "a").write("\n")
        # if sum([i for i in modules.get('qt').last_pulses.values()]) or sum([i for i in modules.get('qb').last_pulses.values()]) or sum([i for i in modules.get('mp').last_pulses.values()]):
        #     open("log20.txt", "a").write(f"{presses}: qt: {sum([i for i in modules.get('qt').last_pulses.values()])}, qb: {sum([i for i in modules.get('qb').last_pulses.values()])}, mp: {sum([i for i in modules.get('mp').last_pulses.values()])}, ng: {sum([i for i in modules.get('ng').last_pulses.values()])}\n")
    
    return 0

if __name__ == "__main__":
    # print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")