"""
    Tic Tac Toe Game
    Student Name: Atul Adhikari
    Student ID: 2408982
"""

import random
import os.path
import json
random.seed()

ENCODING = "utf-8"

def draw_board(board):
    """
    Prints the tic-tac-toe board

            Parameters:
                    board (list)

            Returns:
                    None
    """
    print('-------------')
    print('|', board[0][0], '|', board[0][1], '|', board[0][2], '|')
    print('-------------')
    print('|', board[1][0], '|', board[1][1], '|', board[1][2], '|')
    print('-------------')
    print('|', board[2][0], '|', board[2][1], '|', board[2][2], '|')
    print('-------------')


def welcome(board):
    """
    Prints the welcome message as well as the  tic-tac-toe board

            Parameters:
                    board (list)

            Returns:
                    None
    """
    print('Welcome to the "Unbeatable Noughts and Crosses" game.')
    print('The board layout is shown below : ')
    draw_board(board)
    print('When prompted, enter the number corresponding to the square you want.')


def initialise_board(board):
    """
    Assigns a space character to each cell of the board.

            Parameters:
                    board (list)

            Returns:
                    board (list)
    """
    for index_of_row, row in enumerate(board):
        for index_of_column, _ in enumerate(row):
            board[index_of_row][index_of_column] = ' '

    return board


def get_player_move(board):
    """
    Gets players move as input and converts it to row and col

            Parameters:
                    board (list)

            Returns:
                    row, col (tuple)
    """
    while True:
        print("\n")
        print("\t\t    1  2  3 ")
        print("\t\t    4  5  6 ")
        square = input("Choose your square: 7  8  9 : ")
        # Try except to handle value error
        try:
            square=int(square)
        except ValueError:
            print("Invalid cell.Please select valid one.")
            continue
        if square not in [1,2,3,4,5,6,7,8,9]:
            print("\nInvalid cell! Please enter a valid one.")
            continue

        # Determine the row index based on square number
        if square in [1,2,3]:
            row = 0
        elif square in [4,5,6]:
            row = 1
        elif square in [7,8,9]:
            row = 2

        #Determine the column index based on the square number
        if square in [1,4,7]:
            col = 0
        elif square in [2,5,8]:
            col = 1
        elif square in [3,6,9]:
            col = 2

        if board[row][col] != ' ' or square == 0:
            print("\nInvalid cell! Please enter a valid one.")
        else:
            break

    return row, col


def choose_computer_move(board):
    """
    Gets computers move in row and col

            Parameters:
                    board (list)

            Returns:
                    row, col (tuple)
    """
    # Looks for empty cells and stores indexes of that cell row and col as a tuple
    empty_cells = [
        (i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == ' '
    ]

    if empty_cells:
        row, col = random.choice(empty_cells)
    else:
        row, col = None, None

    return row, col


def check_for_win(board, mark):
    """
    Checks for winning of game

            Parameters:
                    board (list)
                    mark (str)

            Returns:
                    Boolean
    """
    # Check rows
    for row in board:
        win = True

        for cell in row:
            if cell != mark:
                win = False

        if win:
            return True

    # Check columns
    for col in range(3):
        win = True

        for row in range(3):
            if board[row][col] != mark:
                win = False

        if win:
            return True

    # Check diagonals
    if (board[0][0] == board[1][1] == board[2][2] == mark or
        board[0][2] == board[1][1] == board[2][0] == mark):
        return True

    return False


def check_for_draw(board):
    """
    Checks if it is a draw

            Parameters:
                    board (list)

            Returns:
                    Boolean
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False

    return True


def play_game(board):
    """
    Starts the game

            Parameters:
                    board (list)

            Returns:
                    (int)
    """
    print("Let's start")
    initialise_board(board)
    draw_board(board)

    while 1:
        row, col = get_player_move(board)
        board[row][col] = 'X'
        draw_board(board)

        if check_for_win(board, 'X'):
            print("You won!")
            return 1

        if check_for_draw(board):
            print("It's draw.")
            return 0

        print('Its computers turn...')
        row, col = choose_computer_move(board)
        board[row][col] = '0'
        draw_board(board)

        if check_for_win(board, '0'):
            print("Computer Won!")
            return -1

        if check_for_draw(board):
            print("It's Draw!")
            return 0

    return 0


def menu():
    """
    Prints the menu and takes input from user

            Parameters:
                    None

            Returns:
                    choice (str)
    """
    print('\nEnter one of the following options:')
    print('\t\t 1 - Play the game')
    print('\t\t 2 - Save your score in the leaderboard')
    print('\t\t 3 - Load and display the leaderboard')
    print('\t\t q - End the program')
    choice = input('\n1, 2, 3 or q? ')

    return choice

def load_scores():
    """
    Opens the leaderboard.txt file and retrieves the data as a dictionary

            Parameters:
                    None

            Returns:
                    leaders (dictionary)
    """
    filename = 'leaderboard.txt'

    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding = ENCODING) as file:
                leaders = json.load(file)
                #JSON formatted string into Python data(dictionary in this case)
        except json.JSONDecodeError:
            leaders = {}
    else:
        leaders = {}

    return leaders


def save_score(score):
    """
    Opens the leaderboard.txt file and saves players score

            Parameters:
                    score (int)

            Returns:
                    None
    """
    if not score:
        score = 0

    name = input("Enter your name: ")
    filename = 'leaderboard.txt'

    # Check if the 'leaderboard.txt' file exists
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding = ENCODING) as file:
                #deserialises JSON formatted string into Python data(dictionary in this case)
                leaders = json.load(file)

        except json.JSONDecodeError:
            leaders = {}
    else:
        leaders = {}

    # Check if player's name is  already  in the  leaderboard
    if name in leaders:
        # Check if players previous score was lower than current score
        if leaders[name] < score:
            leaders[name] = score
    else:
        leaders[name] = score

    # Write the updated leaderboard data back to the file
    with open(filename, 'w', encoding = ENCODING) as file:
        json.dump(leaders, file)
        print('Leaderboard updated.')


def display_leaderboard(leaders):
    """
    Prints the leaderboard from the leaderboard.txt file

            Parameters:
                    leaders (dict)

            Returns:
                    None
    """
    list_of_leaders = list(leaders.items())
    leaders_after_sorted = []

    while list_of_leaders:
        high_score = list_of_leaders[0]

        for each_item in list_of_leaders:
            if each_item[1] > high_score[1]:
                high_score = each_item

        list_of_leaders.remove(high_score)
        leaders_after_sorted.append(high_score)

    for each_item in leaders_after_sorted:
        print(f"{each_item[0]}: {each_item[1]}")
        