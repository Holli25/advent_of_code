from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

CARD_VALUES_PART1 = {"2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "8":7, "9":8, "T":9, "J":10, "Q":11, "K":12, "A":13}
CARD_VALUES_PART2 = {"2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "8":7, "9":8, "T":9, "J":0, "Q":11, "K":12, "A":13}

# Open and prepare input
def get_input(part:int) -> List[Tuple[str, List[int], int]]:
    with open(path.join(data_folder, "day7.txt"), "r") as file:
        content = file.readlines()
    
    hands = []
    for line in content:
        hand, bet = line.strip().split(" ")

        # Part 1 does not care about Jokers
        if part == 1:
            distribution = sorted([hand.count(card) for card in set(hand)])

        # Part 2 will let Jokers add to the highest possible option
        # As 4ofakind is higher than full house and 3ofakind is higher than two pair, we can add the amount of Jokers to the most often found card
        else:
            distribution = sorted([hand.count(card) for card in set(hand) if card != "J"])

            if distribution:
                distribution[-1] += hand.count("J")

            # For a hand full of jokers, there is not distribution
            else:
                distribution = [5]

        hands.append((hand, distribution, int(bet)))

    return hands

def get_hand_value(distribution:List[int]) -> int:
    if distribution == [1,1,1,1,1]: # High card
        return 1
    elif distribution == [1,1,1,2]: # One pair
        return 2
    elif distribution == [1,2,2]: # Two pair
        return 3
    elif distribution == [1,1,3]: # Three of a kind
        return 4
    elif distribution == [2,3]: # Full house
        return 5
    elif distribution == [1,4]: # Four of a kind
        return 6
    elif distribution == [5]: # Five of a kind
        return 7
    else:
        return 0
    
def get_card_values(hand:str, part:int) -> List[int]:
    if part == 1:
        return [CARD_VALUES_PART1.get(card) for card in hand]
    else:
        return [CARD_VALUES_PART2.get(card) for card in hand]

def part1() -> int:
    # Part 1 of the puzzle
    hands = get_input(part = 1)
    sortable_hands = []
    for cards, distribution, bet in hands:
        value = get_hand_value(distribution)
        card_values = get_card_values(cards, part = 1)
        sortable_hands.append([cards, value, card_values, bet])
    return sum([(i+1) * hand[3] for i, hand in enumerate(sorted(sortable_hands, key = lambda x:(x[1], x[2])))]) # Sort first by hand value and then by distribution

def part2() -> int:
    # Part 2 of the puzzle
    hands = get_input(part = 2)
    sortable_hands = []
    for cards, distribution, bet in hands:
        value = get_hand_value(distribution)
        card_values = get_card_values(cards, part = 2)
        sortable_hands.append([cards, value, card_values, bet])
    return sum([(i+1) * hand[3] for i, hand in enumerate(sorted(sortable_hands, key = lambda x:(x[1], x[2])))]) # Sort first by hand value and then by distribution

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")