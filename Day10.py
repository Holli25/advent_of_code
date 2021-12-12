from typing import List, Tuple, Dict

BRACKETS_REVERSE = {")":"(", "]":"[", "}":"{", ">":"<"}
BRACKETS_FORWARD = {"(":")", "[":"]", "{":"}", "<":">"}
OPENING = ["(", "[", "{", "<"]
CLOSING = [")", "]", "}", ">"]
POINTS = {")":3, "]":57, "}":1197, ">":25137}
POINTS_TWO = {")":1, "]":2, "}":3, ">":4}

def read_data(testing: bool = False) -> List[str]:
    if testing:
        filename = "Test_inputs/Day10.txt"
    else:
        filename = "Inputs/Day10.txt"

    with open(filename) as file:
        lines = file.readlines()

    return lines

def find_first_false_in_line(line: str) -> str:
    open: List[str] = []
    for symbol in line:
        if symbol in OPENING:
            open.append(symbol)
        elif symbol in CLOSING:
            if BRACKETS_REVERSE[symbol] == open[-1]:
                open.pop(-1)
            else:
                return symbol

    return None

def get_wrong_symbols(lines: List[str]) -> List[str]:
    return [find_first_false_in_line(line.rstrip()) for line in lines if find_first_false_in_line(line)]

def get_mistake_score(wrong_symbol: str) -> int:
    return POINTS[wrong_symbol]

def get_score_part_one(wrong_symbols: List[str]) -> int:
    return sum([get_mistake_score(ws) for ws in wrong_symbols])

def get_incomplete_lines(lines: List[str]) -> List[str]:
    return [line.rstrip() for line in lines if not find_first_false_in_line(line.strip())]

def get_missing_brackets(line: str) -> List[str]:
    open: List[str] = []
    for symbol in line:
        if symbol in OPENING:
            open.append(symbol)
        elif symbol in CLOSING:
            if BRACKETS_REVERSE[symbol] == open[-1]:
                open.pop(-1)

    return [BRACKETS_FORWARD[open_bracket] for open_bracket in open[::-1]]

def get_line_score_part_two(line: List[str]) -> int:
    missing_brackets: List[str] = get_missing_brackets(line)
    output: int = 0
    for bracket in missing_brackets:
        output = output * 5 + POINTS_TWO[bracket]
    return output

def get_score_part_two(incomplete_lines: List[str]) -> int:
    line_scores = [get_line_score_part_two(line) for line in incomplete_lines]
    line_scores.sort()
    return line_scores[int((len(line_scores) - 1) / 2)]


def part_one() -> int:
    inputs = read_data()
    wrong_symbols = get_wrong_symbols(inputs)
    return get_score_part_one(wrong_symbols)

def part_two() -> int:
    inputs = read_data()
    incomplete_lines = get_incomplete_lines(inputs)
    return get_score_part_two(incomplete_lines)


print(part_one())
print(part_two())
