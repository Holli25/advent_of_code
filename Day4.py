from typing import List, Tuple

def read_data() -> Tuple[List[List], List[int]]:
    with open("Inputs/Day4.txt") as file:
        number_order = [int(number) for number in file.readline().rstrip().split(",")]
        _ = file.readline() # removes first line without any inputs in it
        lines = file.readlines()

    boards = generate_boards(lines)
    return boards, number_order

def generate_boards(lines: List[str]) -> List[List[int]]:
    current_board = []
    boards = []

    for line in lines:
        # Numbers per line are seperated by a space, but a singular digit has a space in front it, so we need to take double spaces away
        newline = line.lstrip().rstrip().replace("  ", " ").split(" ")
        if len(current_board) <= 5 and len(newline) > 1:
            current_board.append([int(number) for number in newline if number])
        else:
            newboard = Board(current_board)
            boards.append(newboard)
            current_board = []
            newboard = None

    return boards


class Board():
    def __init__(self, numbers: List[List[int]]):
        self.rows = [row for row in numbers]
        self.cols = [[numbers[row][col] for row in range(5)] for col in range(5)]

    def enter_number(self, bingo_number: int) -> None:
        for row_index, row in enumerate(self.rows):
            for number_index, number in enumerate(row):
                if number == bingo_number:
                    self.rows[row_index][number_index] = -1
        for col_index, col in enumerate(self.cols):
            for number_index, number in enumerate(col):
                if number == bingo_number:
                    self.cols[col_index][number_index] = -1

    def has_won(self) -> bool:
        for row in self.rows:
            if sum(row) <= -5:
                return True
        for col in self.cols:
            if sum(col) <= -5:
                return True
        return False

    def get_sum_of_remaining_values(self) -> int:
        return sum([number for row in self.rows for number in row if number > 0])

def get_winner_combination(boards: List[Board], number_order: List[int]) -> Tuple[Board, int]:
    for bingo_number in number_order:
        for board in boards:
            board.enter_number(bingo_number)
            if board.has_won():
                return board, bingo_number

def get_loser_combination(boards: List[Board], number_order: List[int]) -> Tuple[Board, int]:
    remove_list = []
    for bingo_number in number_order:
        for board in boards:
            board.enter_number(bingo_number)
            if board.has_won() and len(boards) > 1:
                remove_list.append(board)
            elif board.has_won() and len(boards) == 1:
                return board, bingo_number

        for b in remove_list:
            boards.remove(b)
        remove_list = []

def part_one() -> int:
    boards, number_order = read_data()
    winner, number = get_winner_combination(boards, number_order)
    out = winner.get_sum_of_remaining_values()
    return out * number

def part_two() -> int:
    boards, number_order = read_data()
    loser, number = get_loser_combination(boards, number_order)
    out = loser.get_sum_of_remaining_values()
    return out * number

if __name__ == "__main__":
    print(part_one())
    print(part_two())
