from os import path
import re
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

class Card():
    def __init__(self, card_id:int, winning_numbers:List[int], card_numbers:List[int]):
        self.card_id = card_id
        self.winning_numbers = winning_numbers
        self.card_numbers = card_numbers
        self.won_cards = self.calculate_won_cards()

    def calculate_score(self):
        score = 0
        for cn in self.card_numbers:
            if cn in self.winning_numbers:
                if not score:
                    score = 1
                else:
                    score *= 2
        
        return score
    
    def calculate_won_cards(self):
        return sum([1 for number in self.card_numbers if number in self.winning_numbers])

# Open and prepare input
def get_input() -> List[Card]:
    with open(path.join(data_folder, "day4.txt"), "r") as file:
        content = file.readlines()

    cards:List[Card] = []

    for line in content:
        card_number = int(re.match("Card\s+(\d+)", line.strip()).group(1))
        winning_numbers = [int(i.group(0)) for i in re.finditer("\d+", line.split(": ")[1].split(" | ")[0])]
        card_numbers = [int(i.group(0)) for i in re.finditer("\d+", line.split(": ")[1].split(" | ")[1])]
        cards.append(Card(card_number, winning_numbers, card_numbers))
    
    return cards
        

def part1() -> int:
    # Part 1 of the puzzle
    cards = get_input()
    return sum([card.calculate_score() for card in cards])

def part2() -> int:
    # Part 2 of the puzzle
    # As I can only win cards that are higher than the current one, we can iterate once over all cards
    # Just keep track of the total amount I have of each card and then win the amount I own * cards I win by this card
    
    cards = get_input()
    total_cards = {card.card_id:1 for card in cards}

    for card in cards:
        for i in range(card.won_cards + 1):
            if i:
                total_cards[card.card_id + i] += 1 * total_cards[card.card_id]
    
    return sum([i for i in total_cards.values()])

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")