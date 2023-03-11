"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xCount = 0
    oCount = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                xCount += 1
            elif board[row][col] == O:
                oCount += 1
    
    if xCount > oCount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Checking if the action is possible is possible
    if action not in actions(board):
        raise Exception('This action is not possible!')
    
    row, col = action
    current_board_copy = copy.deepcopy(board)

    # This action belongs to the current player
    current_board_copy[row][col] = player(board)

    return current_board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checking every row of the board
    if all(row == board[0][0] for row in board[0]):
        return board[0][0]
    elif all(row == board[1][0] for row in board[1]):
        return board[1][0]
    elif all(row == board[2][0] for row in board[2]):
        return board[2][0]

    # Checking columns
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]

    # Checking diagonals
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return board[2][0]
    else:
        return None
        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Checking if there is a winner, if not, we check if all the position are taken to make sure the game is over
    if winner(board) is not None or winner(board) is None and noEmptyPosition(board) is True:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    max(possible_moves, key=lambda value: value[0]) returns a sublist in possible_moves that has the greatest value at index 0
    """
    # Check if the game is not over first
    if not terminal(board):

        possible_moves = []

        if player(board) == X:
            # If the game just began, pick a random position
            if isBeginningOfGame(board):
                return random.choice(tuple(actions(board)))     
            else:
                for action in actions(board):
                    possible_moves.append([minValue(result(board, action)), action])
                return max(possible_moves, key=lambda value: value[0])[1]


        elif player(board) == O:
            for action in actions(board):
                possible_moves.append([maxValue(result(board, action)), action])
            return min(possible_moves, key=lambda value: value[0])[1]
    else:
        return None
    

# Pseudo-code from the lecture
def maxValue(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v


# Check if everyposition are taken or not
def noEmptyPosition(board):
    if not any(EMPTY in row for row in board):
        return True
    else:
        return False

def isBeginningOfGame(board):
    # if the number of possibilties is 9, that means that the board is empty and the game just began.
    if len(actions(board)) == 9:
        return True
    else:
        return False




