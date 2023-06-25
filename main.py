from random import randint, shuffle

from typing import Tuple

with open("wordlist.txt") as file:
    word_list = file.readlines()

# format word_list
word_list = [s.strip('\n') for s in word_list]
shuffle(word_list)

board = []
answer_key = []
alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet = list(alphabet)
word_dict = {}
tries = 50

# board_len = input("Please input how big the board should be: ")
board_len = 10
flag = True

# Make sure input is a string
while flag:
    try:
        board_len = int(board_len)
        flag = False
    except ValueError:
        board_len = input("Please input a number. Try again: ")

# Randomly add letters into the board
for i in range(board_len):
    row = []
    answer_row = []
    for j in range(board_len):
        row.append(alphabet[randint(0, len(alphabet)-1)])
        answer_row.append("*")
    board.append(row)
    answer_key.append(answer_row)


def add_words():
    global board
    for word in word_list:
        attempts = 50
        # horizontal, vertical or diagonal
        orientation = randint(0, 3)

        place_x, place_y = random_placement(word)

        # reverse
        if randint(0, 4) == 0 or (orientation == 3 and randint(0, 4) <= 3):
            word = word[::-1]

        # horizontal
        if orientation == 0:
            place_x = bound(word, True, False)

            conflict = False
            while True:
                for j in range(len(word)):
                    if word_dict.get((place_y, place_x+j)) is not None and board[place_y][place_x+j] != word[j]:
                        place_x, place_y = random_placement(word)
                        place_x = bound(word, True, False)
                        conflict = True
                        if attempts <= 0:
                            print(f"failed to add {word} after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if conflict:
                    conflict = False
                    continue

                break

            # add word
            for j, chars in enumerate(word):
                board[place_y][place_x+j] = chars
                answer_key[place_y][place_x+j] = chars
                word_dict[(place_y, place_x+j)] = word
        # vertical
        elif orientation == 1:
            place_y = bound(word, False, True)

            conflict = False
            while True:
                for j in range(len(word)):
                    if word_dict.get((place_y+j, place_x)) is not None and board[place_y+j][place_x] != word[j]:
                        place_x, place_y = random_placement(word)
                        place_y = bound(word, False, True)
                        conflict = True
                        if attempts <= 0:
                            print(f"failed to add {word} after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if conflict:
                    conflict = False
                    continue
                break

            # add word
            for j, chars in enumerate(word):
                board[place_y + j][place_x] = chars
                answer_key[place_y + j][place_x] = chars
                word_dict[(place_y + j, place_x)] = word
        # diagonal top-left
        elif orientation == 2:
            place_x, place_y = bound(word, True, True)

            conflict = False
            while True:
                for j in range(len(word)):
                    if word_dict.get((place_y+j, place_x+j)) is not None and board[place_y+j][place_x+j] != word[j]:
                        place_y, place_x = bound(word, True, True)
                        conflict = True
                        if attempts <= 0:
                            print(f"failed to add {word} after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if conflict:
                    conflict = False
                    continue
                break

            # add word
            for j, chars in enumerate(word):
                board[place_y + j][place_x + j] = chars
                answer_key[place_y + j][place_x + j] = chars
                word_dict[(place_y + j, place_x + j)] = word
        # diagonal bot-left
        else:
            place_x = bound(word, True)
            place_y = randint(len(word)-1, board_len - 1)


            conflict = False
            while True:
                for j in range(len(word)):
                    if word_dict.get((place_y-j, place_x+j)) is not None and board[place_y-j][place_x+j] != word[j]:
                        place_x = bound(word, True)
                        place_y = randint(len(word) - 1, board_len - 1)
                        conflict = True
                        if attempts <= 0:
                            print(f"failed to add {word} after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if conflict:
                    conflict = False
                    continue
                break

            # add word
            for j, chars in enumerate(word):
                board[place_y-j][place_x + j] = chars
                answer_key[place_y-j][place_x + j] = chars
                word_dict[(place_y-j, place_x + j)] = word
    return 0


# randomly select a spot to place word
def random_placement(word: str) -> Tuple[int, int]:
    # pick an x and y value
    placement_x = randint(0, board_len - 1)
    placement_y = randint(0, board_len - 1)
    while placement_x + (len(word) - 1) > board_len:
        placement_x = randint(0, board_len - 1)
    while placement_y + (len(word) - 1) > board_len:
        placement_y = randint(0, board_len - 1)
    return placement_x, placement_y


# Make sure words stay in the bounds of the grid
def bound(word, x=False, y=False):
    place_x = randint(0, board_len - len(word) - 1)
    place_y = randint(0, board_len - len(word) - 1)
    if x and y:
        return (place_x, place_y)
    elif x:
        return place_x
    return place_y


while tries > 0:
    if add_words() != 0:
        tries -= 1
        print(f"failed to add words... trying again")
    else:
        break

if tries == 0:
    print(f"exit with 0 tries")
    exit(-1)

# Export to a different file
with open("output.txt", "w") as file:
    out_str = ""
    for row in board:
        out_str += " ".join(row) + "\n"
    file.write(out_str)

with open("answer_key.txt", "w") as file:
    out_str = ""
    for row in answer_key:
        out_str += " ".join(row) + "\n"
    file.write(out_str)
